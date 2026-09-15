import json
import shutil
import subprocess

import pytest

from runner.security_suite import FIXTURES, evaluate, parse_verdict, stage

CASES = json.loads((FIXTURES / "manifest.json").read_text())["cases"]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_actual_circuit_against_requirement_testbench(case, tmp_path):
    if not shutil.which("iverilog") or not shutil.which("vvp"):
        pytest.skip("Icarus required")
    compiled = subprocess.run(
        [
            "iverilog",
            "-g2012",
            "-s",
            "tb",
            "-o",
            str(tmp_path / "design.vvp"),
            str(FIXTURES / case["id"] / "design.sv"),
            str(FIXTURES / case["id"] / "tb.sv"),
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert compiled.returncode == 0, compiled.stderr
    simulated = subprocess.run(
        ["vvp", str(tmp_path / "design.vvp")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if case["expected"] == "property_held_for_test":
        assert simulated.returncode == 0 and "SECURITY_TEST_PASS" in simulated.stdout
    else:
        assert simulated.returncode == 1 and "SECURITY_VIOLATION:" in simulated.stdout
    assert "CHECK " in simulated.stdout
    assert "FUNCTIONAL_FAILURE" not in simulated.stdout
    assert (tmp_path / "waveform.vcd").is_file()
    assert len(simulated.stdout.encode()) < 60000


def test_format_scored_separately_and_ambiguous_verdict_rejected():
    value = '{"verdict":"property_violated","explanation":"assertion failed"}'
    assert parse_verdict(value) == ("property_violated", True)
    assert parse_verdict("Explanation first. " + value) == ("property_violated", False)
    assert parse_verdict(value + value) == (None, False)
    assert parse_verdict('{"verdict":"unknown","explanation":"x"}') == (None, False)
    assert parse_verdict('prefix {"verdict":[],"explanation":"x"}') == (None, False)


@pytest.mark.parametrize("case", CASES[::2], ids=lambda case: case["family"])
def test_testbench_rejects_disabling_all_functionality(case, tmp_path):
    if not shutil.which("iverilog") or not shutil.which("vvp"):
        pytest.skip("Icarus required")
    header = (FIXTURES / case["id"] / "design.sv").read_text().splitlines()[0]
    port = {
        "authorization": "grant",
        "register_lock": "value",
        "debug_access": "data",
        "reset_clear": "value",
        "output_isolation": "data",
    }[case["family"]]
    mutant = tmp_path / "disabled.sv"
    mutant.write_text(header + f"\nassign {port} = 0;\nendmodule\n")
    compiled = subprocess.run(
        [
            "iverilog",
            "-g2012",
            "-s",
            "tb",
            "-o",
            str(tmp_path / "design.vvp"),
            str(mutant),
            str(FIXTURES / case["id"] / "tb.sv"),
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert compiled.returncode == 0, compiled.stderr
    simulated = subprocess.run(
        ["vvp", str(tmp_path / "design.vvp")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert simulated.returncode == 1
    assert "SECURITY_TEST_PASS" not in simulated.stdout


@pytest.mark.parametrize(
    "defect", ["unlinked", "timeout", "compile_error", "functional", "extra_call"]
)
def test_invalid_tool_evidence_cannot_pass(defect):
    compile_event = {
        "type": "tool",
        "name": "compile_rtl",
        "arguments": {"sources": ["d", "t"], "top": "tb"},
        "result": {"structuredContent": {"ok": True, "returncode": 0, "run_id": "compile"}},
    }
    simulate_event = {
        "type": "tool",
        "name": "simulate",
        "arguments": {"run_id": "compile"},
        "result": {"structuredContent": {"returncode": 1, "output": "SECURITY_VIOLATION: test"}},
    }
    trace = {"events": [compile_event, simulate_event], "messages": [{}]}
    assert evaluate(trace, ["d", "t"], "property_violated")["passed"]
    if defect == "unlinked":
        simulate_event["arguments"]["run_id"] = "other"
    elif defect == "timeout":
        simulate_event["result"]["structuredContent"]["timed_out"] = True
    elif defect == "compile_error":
        compile_event["result"]["structuredContent"]["ok"] = False
    elif defect == "functional":
        simulate_event["result"]["structuredContent"]["output"] += " FUNCTIONAL_FAILURE"
    else:
        trace["events"].append(simulate_event)
    assert not evaluate(trace, ["d", "t"], "property_violated")["passed"]


def test_stage_does_not_expose_answers_or_overwrite_changes(tmp_path):
    manifest, hashes = stage(tmp_path)
    assert len(manifest["cases"]) == 10 and len(hashes) == 20
    assert not list(tmp_path.rglob("manifest.json"))
    dest = tmp_path / next(iter(hashes))
    dest.write_text("user edit")
    with pytest.raises(ValueError, match="Refusing to overwrite"):
        stage(tmp_path)
