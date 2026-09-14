"""Evaluate a tool-using agent on two synthetic authorization circuits.

Stages only project-owned fixtures into an explicit external GUIDE subdirectory.
Does not edit upstream sources or expose source editing to the agent.
"""

import argparse
import asyncio
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import timedelta
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from integrations.guide.paths import resolve_guide_root
from integrations.inference.client import InferenceClient
from runner.eda_loop import run_loop

PREFIX = ".llm4security-baseline/authorization"
EXPECTED = {"case_a": "property_held_for_test", "case_b": "property_violated"}


def stage(root, fixtures):
    target = root / PREFIX
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError("Fixture directory escapes GUIDE_ROOT")
    target.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for name in ("case_a.sv", "case_b.sv", "tb.sv"):
        data = (fixtures / name).read_bytes()
        dest = target / name
        if dest.is_symlink():
            raise ValueError("Fixture destination must not be a symlink")
        if dest.exists() and dest.read_bytes() != data:
            raise ValueError(f"Refusing to overwrite changed fixture {dest}")
        if not dest.exists():
            with dest.open("xb") as out:
                out.write(data)
        hashes[f"{PREFIX}/{name}"] = hashlib.sha256(data).hexdigest()
    return hashes


def evaluate(trace, sources, expected):
    """Require linked tool evidence; compiler/runtime errors are not detections."""
    compiled = set()
    observed = None
    tool_calls = sum(e.get("type") == "tool" for e in trace["events"])
    for event in trace["events"]:
        if event.get("type") != "tool":
            continue
        result = event.get("result") or {}
        evidence = result.get("structuredContent") or {}
        args = event.get("arguments") or {}
        if result.get("isError") or evidence.get("timed_out"):
            continue
        if event["name"] == "compile_rtl" and evidence.get("ok"):
            if args.get("sources") == sources and args.get("top") == "tb":
                compiled.add(evidence.get("run_id"))
        if event["name"] != "simulate" or args.get("run_id") not in compiled:
            continue
        output = evidence.get("output", "")
        if evidence.get("returncode") == 0 and "AUTHORIZATION_TEST_PASS" in output:
            observed = "property_held_for_test"
        elif evidence.get("returncode") == 1 and "AUTHORIZATION_VIOLATION" in output:
            observed = "property_violated"
    final = trace["messages"][-1].get("content") or ""
    try:
        verdict = json.loads(final)["verdict"]
    except (ValueError, KeyError, TypeError):
        verdict = None
    return {
        "expected": expected,
        "observed": observed,
        "agent_verdict": verdict,
        "tool_calls": tool_calls,
        "passed": observed == expected and verdict == expected and tool_calls == 2,
    }


async def execute(args):
    root = resolve_guide_root()
    hashes = stage(root, args.fixtures)
    client = InferenceClient()
    report = {
        "experiment": "synthetic-authorization-v1",
        "model": client.model,
        "source_sha256": hashes,
        "settings": {
            k: os.getenv(k)
            for k in ("VLLM_MODEL", "VLLM_MODEL_REVISION", "VLLM_IMAGE", "VLLM_MAX_MODEL_LEN")
        },
        "repository_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip(),
        "cases": {},
        "interpretation": "Two synthetic test cases; no benchmark accuracy or security-proof claim.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        client.models()
        params = StdioServerParameters(
            command=sys.executable, args=["-m", "guide_mcp.eda_server.server"], env=dict(os.environ)
        )
        async with stdio_client(params) as (read, write):
            async with ClientSession(
                read, write, read_timeout_seconds=timedelta(seconds=420)
            ) as session:
                await session.initialize()
                for case, expected in EXPECTED.items():
                    sources = [f"{PREFIX}/{case}.sv", f"{PREFIX}/tb.sv"]
                    prompt = (
                        f"Compile exactly {json.dumps(sources)} with top tb, then simulate its "
                        "successful run_id. The requirement is grant == (request & privileged), "
                        "regardless of bypass. Evaluate this case from the tool evidence. "
                        "Run each tool once; do not repair or retry a failing design. "
                        "AUTHORIZATION_VIOLATION with simulation returncode 1 is a property "
                        "violation; AUTHORIZATION_TEST_PASS with returncode 0 is a passing test. "
                        "Other failures are inconclusive. Finish with only a JSON object: "
                        '{"verdict":"property_held_for_test|property_violated|inconclusive",'
                        '"explanation":"evidence-based explanation"}.'
                    )
                    started = time.monotonic()
                    trace = await run_loop(client, session, prompt, max_turns=4)
                    report["cases"][case] = {
                        **evaluate(trace, sources, expected),
                        "elapsed_seconds": time.monotonic() - started,
                        "usage": [
                            e["response"].get("usage")
                            for e in trace["events"]
                            if e["type"] == "inference"
                        ],
                        "trace": trace,
                    }
                    args.output.write_text(json.dumps(report, indent=2))
        report["passed"] = all(c["passed"] for c in report["cases"].values())
        return report
    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=Path("examples/eda/authorization"))
    parser.add_argument("--output", type=Path, default=Path("results/authorization-baseline.json"))
    args = parser.parse_args()
    report = asyncio.run(execute(args))
    args.output.write_text(json.dumps(report, indent=2))
    print(
        json.dumps(
            {k: {n: v for n, v in c.items() if n != "trace"} for k, c in report["cases"].items()},
            indent=2,
        )
    )
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
