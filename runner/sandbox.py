"""Bounded Docker execution. No host execution fallback is exposed to MCP."""

import os
import subprocess
import threading
import time
import uuid
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class SandboxSpec:
    workdir: Path
    image: str = "llm4security-eda:phase1"
    cpu_limit: float = 2.0
    memory_limit_gb: int = 2
    timeout_seconds: float = 60


@dataclass(slots=True)
class Execution:
    returncode: int
    output: str
    timed_out: bool = False
    duration_seconds: float = 0
    image_id: str = ""


def capture(argv, timeout):
    """Drain output continuously, retaining at most 64 KiB in memory."""
    retained = bytearray()
    with subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:

        def drain():
            while chunk := proc.stdout.read(8192):
                retained.extend(chunk[: max(0, 65536 - len(retained))])

        thread = threading.Thread(target=drain, daemon=True)
        thread.start()
        timed_out = False
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            proc.kill()
            proc.wait()
        thread.join(timeout=5)
        output = retained.decode(errors="replace")
        if timed_out:
            output += f"\nCommand timed out after {timeout} seconds"
        if len(retained) == 65536:
            output += "\n[output truncated at 64 KiB]"
        return Execution(proc.returncode, output, timed_out)


class Sandbox:
    def __init__(self, spec: SandboxSpec):
        self.spec = spec

    def create_command(self, name, argv):
        spec = self.spec
        return [
            "docker",
            "create",
            "--name",
            name,
            "--network",
            "none",
            "--read-only",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "--pids-limit",
            "64",
            "--cpus",
            str(spec.cpu_limit),
            "--memory",
            f"{spec.memory_limit_gb}g",
            "--memory-swap",
            f"{spec.memory_limit_gb}g",
            "--ulimit",
            "fsize=67108864:67108864",
            "--user",
            f"{os.getuid()}:{os.getgid()}",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,size=64m,mode=1777",
            "--tmpfs",
            "/work:rw,noexec,nosuid,size=128m,mode=1777",
            "--mount",
            f"type=bind,src={spec.workdir.resolve()},dst=/inputs,readonly",
            "--workdir",
            "/work",
            "--entrypoint",
            "/bin/sleep",
            spec.image,
            "infinity",
        ]

    def export_artifact(self, name: str, filename: str) -> Execution:
        """Read through exec: Docker's archive API cannot see tmpfs artifacts."""
        destination = self.spec.workdir / filename
        limit = 64 * 1024**2
        command = [
            "docker",
            "exec",
            name,
            "/bin/sh",
            "-c",
            'test -f "$1" && test ! -L "$1" && exec head -c 67108865 -- "$1"',
            "eda-export",
            f"/work/{filename}",
        ]
        try:
            with destination.open("xb") as output:
                result = subprocess.run(command, stdout=output, stderr=subprocess.PIPE, timeout=15)
            if result.returncode or destination.stat().st_size > limit:
                destination.unlink()
                return Execution(125, f"Could not export regular artifact {filename}")
            return Execution(0, "")
        except subprocess.TimeoutExpired:
            destination.unlink(missing_ok=True)
            return Execution(125, f"Timed out exporting {filename}", timed_out=True)

    def run(self, argv: list[str], outputs: tuple[str, ...] = ()) -> Execution:
        name = f"llm4security-{uuid.uuid4().hex}"
        start = time.monotonic()
        result = Execution(125, "")
        try:
            inspect = capture(
                ["docker", "image", "inspect", "--format", "{{.Id}}", self.spec.image], 60
            )
            if inspect.returncode:
                return inspect
            created = capture(self.create_command(name, argv), 60)
            if created.returncode:
                return created
            started = capture(["docker", "start", name], 60)
            if started.returncode:
                return started
            result = capture(["docker", "exec", name, *argv], self.spec.timeout_seconds)
            result.image_id = inspect.output.strip()
            if result.timed_out:
                capture(["docker", "kill", name], 10)
            if not result.timed_out:
                for filename in outputs:
                    if filename == "design.vvp" and result.returncode != 0:
                        continue
                    if filename not in ("design.vvp", "waveform.vcd"):
                        raise ValueError("Unsupported sandbox output")
                    copied = self.export_artifact(name, filename)
                    if filename == "design.vvp" and copied.returncode:
                        result.returncode = 125
                        result.output += copied.output
            return result
        except OSError as exc:
            return Execution(125, f"Docker unavailable: {exc}")
        finally:
            result.duration_seconds = time.monotonic() - start
            try:
                capture(["docker", "rm", "--force", name], 60)
            except OSError:
                pass
