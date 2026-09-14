import json

import pytest

from runner.baseline import evaluate, stage


def trace(returncode, output, *, timed_out=False, input_run="compiled"):
    return {
        "messages": [{"content": json.dumps({"verdict": "property_violated"})}],
        "events": [
            {
                "type": "tool",
                "name": "compile_rtl",
                "arguments": {"sources": ["design.sv", "tb.sv"], "top": "tb"},
                "result": {"structuredContent": {"ok": True, "run_id": "compiled"}},
            },
            {
                "type": "tool",
                "name": "simulate",
                "arguments": {"run_id": input_run},
                "result": {
                    "structuredContent": {
                        "returncode": returncode,
                        "output": output,
                        "timed_out": timed_out,
                    }
                },
            },
        ],
    }


@pytest.mark.parametrize(
    "code,output,timeout,run_id,passed",
    [
        (1, "FATAL AUTHORIZATION_VIOLATION", False, "compiled", True),
        (125, "AUTHORIZATION_VIOLATION", False, "compiled", False),
        (1, "AUTHORIZATION_VIOLATION", True, "compiled", False),
        (1, "syntax error", False, "compiled", False),
        (1, "AUTHORIZATION_VIOLATION", False, "unrelated", False),
    ],
)
def test_detection_requires_linked_assertion_evidence(code, output, timeout, run_id, passed):
    result = evaluate(
        trace(code, output, timed_out=timeout, input_run=run_id),
        ["design.sv", "tb.sv"],
        "property_violated",
    )
    assert result["passed"] is passed


def test_staging_preserves_changed_external_files(tmp_path):
    from pathlib import Path

    root = tmp_path / "GUIDE"
    root.mkdir()
    fixtures = Path("examples/eda/authorization")
    hashes = stage(root, fixtures)
    assert len(hashes) == 3
    dest = root / ".llm4security-baseline/authorization/case_a.sv"
    dest.write_text("user change")
    with pytest.raises(ValueError, match="Refusing to overwrite"):
        stage(root, fixtures)
    assert dest.read_text() == "user change"


def test_repeated_calls_do_not_satisfy_fixed_experiment_budget():
    data = trace(1, "AUTHORIZATION_VIOLATION")
    data["events"].append(data["events"][-1])
    assert not evaluate(data, ["design.sv", "tb.sv"], "property_violated")["passed"]
