"""GUIDE source snapshots and Icarus compile/simulate operations."""

import hashlib
import json
import os
import re
import shutil
import subprocess
import uuid
from dataclasses import asdict
from pathlib import Path

from pydantic import BaseModel, Field

from integrations.guide.paths import guide_file, resolve_guide_root
from runner.sandbox import Sandbox, SandboxSpec


class ToolResult(BaseModel):
    ok: bool
    summary: str
    artifact_paths: list[str] = Field(default_factory=list)
    run_id: str | None = None
    returncode: int | None = None
    timed_out: bool = False
    output: str = ""


class EdaTools:
    def __init__(self, guide_root=None, artifact_root=None, image=None, sandbox_factory=Sandbox):
        self.guide_root = resolve_guide_root(guide_root)
        self.artifact_root = Path(
            artifact_root or os.getenv("EDA_ARTIFACT_ROOT", "results/eda")
        ).resolve()
        if self.artifact_root.is_relative_to(self.guide_root):
            raise ValueError("Artifacts must be outside GUIDE_ROOT")
        self.image = image or os.getenv("EDA_IMAGE", "llm4security-eda:phase1")
        self.sandbox_factory = sandbox_factory

    def _run(self, work, argv, outputs, timeout):
        if not 1 <= timeout <= 120:
            raise ValueError("timeout_seconds must be between 1 and 120")
        return self.sandbox_factory(SandboxSpec(work, self.image, timeout_seconds=timeout)).run(
            argv, outputs=outputs
        )

    def _record(self, work, operation, execution, argv, **metadata):
        ok = execution.returncode == 0 and not execution.timed_out
        result = ToolResult(
            ok=ok,
            summary=f"{operation} " + ("completed" if ok else "failed"),
            run_id=work.name,
            returncode=execution.returncode,
            timed_out=execution.timed_out,
            output=execution.output,
        )
        (work / "output.log").write_text(execution.output)
        result.artifact_paths = [str(p) for p in sorted(work.iterdir()) if p.is_file()]
        result.artifact_paths.append(str(work / "result.json"))
        (work / "result.json").write_text(
            json.dumps(
                {
                    **result.model_dump(),
                    "operation": operation,
                    "argv": argv,
                    "image": self.image,
                    "execution": asdict(execution),
                    **metadata,
                },
                indent=2,
            )
        )
        return result

    def compile_rtl(
        self, sources: list[str], top: str | None = None, timeout_seconds: int = 60
    ) -> ToolResult:
        """Compile explicit GUIDE-relative RTL and headers; return a run_id for simulate."""
        if not sources or len(sources) > 128:
            raise ValueError("Provide 1..128 source/header files")
        if top is not None and not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_$]*", top):
            raise ValueError("top must be a Verilog module identifier")
        if not 1 <= timeout_seconds <= 120:
            raise ValueError("timeout_seconds must be between 1 and 120")
        paths = [(name, guide_file(self.guide_root, name)) for name in dict.fromkeys(sources)]
        if sum(path.stat().st_size for _, path in paths) > 16 * 1024**2:
            raise ValueError("Source snapshot exceeds 16 MiB")
        work = self.artifact_root / uuid.uuid4().hex
        work.mkdir(parents=True)
        hashes = {}
        for name, path in paths:
            target = work / "sources" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            hashes[name] = hashlib.sha256(target.read_bytes()).hexdigest()
        argv = ["iverilog", "-g2012", "-o", "/work/design.vvp"]
        if top:
            argv += ["-s", top]
        includes = sorted({str(Path("/inputs/sources") / Path(name).parent) for name, _ in paths})
        for include in includes:
            argv += ["-I", include]
        argv += [f"/inputs/sources/{name}" for name, path in paths if path.suffix in (".v", ".sv")]
        # Static shell fragment records the compiler version; user values stay separate argv items.
        wrapped = ["/bin/sh", "-c", 'iverilog -V; exec "$@"', "eda", *argv]
        execution = self._run(work, wrapped, ("design.vvp",), timeout_seconds)
        compiled = work / "design.vvp"
        if execution.returncode == 0 and not compiled.is_file():
            execution.returncode = 125
            execution.output += "\nCompiler produced no design.vvp"
        try:
            commit = subprocess.run(
                ["git", "-C", str(self.guide_root), "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            commit = ""
        return self._record(
            work,
            "compile_rtl",
            execution,
            wrapped,
            sources=hashes,
            guide_commit=commit or None,
            binary_sha256=hashlib.sha256(compiled.read_bytes()).hexdigest()
            if compiled.is_file()
            else None,
        )

    def simulate(self, run_id: str, timeout_seconds: int = 30) -> ToolResult:
        """Run a successful compile_rtl run. Exit 0 means completion, not a security proof.

        Testbenches should use $fatal on failure and dump to waveform.vcd for waveform capture.
        """
        if not re.fullmatch(r"[0-9a-f]{32}", run_id):
            raise ValueError("run_id must be a compile_rtl run ID")
        if not 1 <= timeout_seconds <= 120:
            raise ValueError("timeout_seconds must be between 1 and 120")
        source = self.artifact_root / run_id
        manifest_path = source / "result.json"
        binary = source / "design.vvp"
        if source.is_symlink() or manifest_path.is_symlink() or binary.is_symlink():
            raise ValueError("Symlink compile artifacts are not accepted")
        try:
            manifest = json.loads(manifest_path.read_text())
            if manifest["operation"] != "compile_rtl" or not manifest["ok"]:
                raise ValueError("simulate requires a successful compilation")
            digest = hashlib.sha256(binary.read_bytes()).hexdigest()
            if digest != manifest["binary_sha256"]:
                raise ValueError("Compiled artifact hash mismatch")
        except (FileNotFoundError, KeyError, json.JSONDecodeError) as exc:
            raise ValueError("Unknown or incomplete compile run") from exc
        work = self.artifact_root / uuid.uuid4().hex
        work.mkdir(parents=True)
        shutil.copyfile(binary, work / "input.vvp")
        argv = ["/bin/sh", "-c", "vvp -V; exec vvp /inputs/input.vvp"]
        execution = self._run(work, argv, ("waveform.vcd",), timeout_seconds)
        return self._record(
            work, "simulate", execution, argv, compile_run_id=run_id, binary_sha256=digest
        )
