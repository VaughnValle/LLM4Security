import json
import os
import shutil
import subprocess

import pytest

from guide_mcp.eda_server.tools import EdaTools
from runner.sandbox import Execution, Sandbox, SandboxSpec, capture


@pytest.fixture
def guide(tmp_path):
    root = tmp_path / "GUIDE"
    root.mkdir()
    (root / ".gitmodules").write_text("")
    (root / "tb.sv").write_text("""module tb;
initial begin
  $dumpfile("waveform.vcd"); $dumpvars(0, tb);
  $display("PASS"); #1; $finish;
end
endmodule
""")
    return root


class NativeTestSandbox:
    """Test-only adapter for tiny trusted fixtures, never selectable in production."""

    def __init__(self, spec):
        self.spec = spec

    def run(self, argv, outputs=()):
        work = self.spec.workdir
        if "iverilog" in argv:
            argv = argv[argv.index("iverilog") :]
            argv = [
                a.replace("/inputs/", str(work) + "/").replace("/work/", str(work) + "/")
                for a in argv
            ]
        else:
            argv = ["vvp", str(work / "input.vvp")]
        try:
            result = subprocess.run(
                argv, cwd=work, capture_output=True, text=True, timeout=self.spec.timeout_seconds
            )
            return Execution(
                result.returncode, result.stdout + result.stderr, image_id="native-test-only"
            )
        except subprocess.TimeoutExpired:
            return Execution(-9, "timeout", timed_out=True)


@pytest.fixture
def eda(guide, tmp_path):
    if not shutil.which("iverilog"):
        pytest.skip("Icarus required for real compiler tests")
    return EdaTools(guide, tmp_path / "runs", sandbox_factory=NativeTestSandbox)


def test_real_compile_simulate_and_provenance(eda, guide):
    original = (guide / "tb.sv").read_bytes()
    compiled = eda.compile_rtl(["tb.sv"], top="tb")
    assert compiled.ok
    manifest = json.loads((eda.artifact_root / compiled.run_id / "result.json").read_text())
    assert manifest["sources"]["tb.sv"]
    assert manifest["binary_sha256"]
    simulated = eda.simulate(compiled.run_id)
    assert simulated.ok and "PASS" in simulated.output
    assert any(p.endswith("waveform.vcd") for p in simulated.artifact_paths)
    assert (guide / "tb.sv").read_bytes() == original
    assert not (guide / "design.vvp").exists()


def test_real_compile_error_blocks_simulation(eda, guide):
    (guide / "tb.sv").write_text("module tb; this is not valid; endmodule")
    result = eda.compile_rtl(["tb.sv"], top="tb")
    assert not result.ok and result.returncode != 0
    with pytest.raises(ValueError, match="successful compilation"):
        eda.simulate(result.run_id)


def test_real_fatal_and_timeout(eda, guide):
    (guide / "tb.sv").write_text('module tb; initial $fatal(1, "FAIL"); endmodule')
    result = eda.simulate(eda.compile_rtl(["tb.sv"], "tb").run_id)
    assert not result.ok and "FAIL" in result.output
    (guide / "tb.sv").write_text("module tb; initial forever #1; endmodule")
    result = eda.simulate(eda.compile_rtl(["tb.sv"], "tb").run_id, timeout_seconds=1)
    assert not result.ok and result.timed_out


def test_snapshot_headers_and_hash_tampering(eda, guide):
    (guide / "value.vh").write_text("`define VALUE 7\n")
    (guide / "tb.sv").write_text('`include "value.vh"\nmodule tb; initial $finish; endmodule')
    compiled = eda.compile_rtl(["tb.sv", "value.vh"], "tb")
    assert compiled.ok
    (eda.artifact_root / compiled.run_id / "design.vvp").write_text("tampered")
    with pytest.raises(ValueError, match="hash mismatch"):
        eda.simulate(compiled.run_id)


@pytest.mark.parametrize(
    "source", ["../outside.sv", "/tmp/outside.sv", "missing.sv", ".gitmodules"]
)
def test_reject_invalid_sources(guide, tmp_path, source):
    eda = EdaTools(guide, tmp_path / "runs")
    with pytest.raises(ValueError):
        eda.compile_rtl([source])
    assert not eda.artifact_root.exists()


def test_reject_symlink_and_bad_top(guide, tmp_path):
    outside = tmp_path / "outside.sv"
    outside.write_text("module tb; endmodule")
    (guide / "link.sv").symlink_to(outside)
    eda = EdaTools(guide, tmp_path / "runs")
    with pytest.raises(ValueError):
        eda.compile_rtl(["link.sv"])
    with pytest.raises(ValueError):
        eda.compile_rtl(["tb.sv"], "tb; touch /tmp/pwn")
    with pytest.raises(ValueError):
        eda.simulate("../../bad")
    with pytest.raises(ValueError):
        EdaTools(guide, guide / "results")


def test_sandbox_constraints_and_bounded_capture(tmp_path):
    argv = Sandbox(SandboxSpec(tmp_path)).create_command("test", ["iverilog", "-V"])
    for value in (
        "none",
        "--read-only",
        "ALL",
        "no-new-privileges",
        "--pids-limit",
        "--memory",
        "--memory-swap",
        "--cpus",
        "--ulimit",
    ):
        assert value in argv
    assert "--privileged" not in argv and "--device" not in argv
    assert any("readonly" in a for a in argv)
    result = capture(["python3", "-c", 'print("x" * 100000)'], 5)
    assert len(result.output) < 66000 and "truncated" in result.output
    result = capture(["python3", "-c", "import time; time.sleep(10)"], 0.05)
    assert result.timed_out


def test_docker_cleanup_after_timeout(tmp_path, monkeypatch):
    calls = []

    def fake_capture(argv, timeout):
        calls.append(argv)
        if argv[1] == "exec":
            return Execution(-9, "timeout", timed_out=True)
        return Execution(0, "sha256:test")

    monkeypatch.setattr("runner.sandbox.capture", fake_capture)
    result = Sandbox(SandboxSpec(tmp_path)).run(["vvp", "/inputs/input.vvp"])
    assert result.timed_out
    assert any(c[1] == "kill" for c in calls)
    assert calls[-1][1:3] == ["rm", "--force"]
    assert not any(c[1] == "cp" for c in calls)


@pytest.mark.skipif(
    os.getenv("RUN_DOCKER_TESTS") != "1", reason="Set RUN_DOCKER_TESTS=1 with EDA image built"
)
def test_real_docker_loop(guide, tmp_path):
    eda = EdaTools(guide, tmp_path / "runs")
    compiled = eda.compile_rtl(["tb.sv"], "tb")
    assert compiled.ok, compiled.output
    result = eda.simulate(compiled.run_id)
    assert result.ok and "PASS" in result.output, result.output
    assert any(p.endswith("waveform.vcd") for p in result.artifact_paths)
