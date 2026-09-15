"""Versioned synthetic security suite: deterministic MCP checks or agent trials."""

import argparse
import asyncio
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from integrations.guide.paths import resolve_guide_root
from integrations.inference.client import InferenceClient
from runner.eda_loop import run_loop

FIXTURES = Path(__file__).resolve().parents[1] / "examples/eda/security_v1"
PREFIX = ".llm4security-suite/security-v1"
VERDICTS = {"property_held_for_test", "property_violated", "inconclusive"}


def stage(root, fixtures=FIXTURES):
    manifest = json.loads((fixtures / "manifest.json").read_text())
    hashes = {}
    for case in manifest["cases"]:
        if not re.fullmatch(r"case_[0-9]{2}", case["id"]):
            raise ValueError("Invalid case identifier")
        for name in ("design.sv", "tb.sv"):
            relative = f"{PREFIX}/{case['id']}/{name}"
            dest = root / relative
            if dest.is_symlink() or not dest.resolve().is_relative_to(root.resolve()):
                raise ValueError("Fixture destination escapes GUIDE_ROOT or is a symlink")
            data = (fixtures / case["id"] / name).read_bytes()
            if dest.exists() and dest.read_bytes() != data:
                raise ValueError(f"Refusing to overwrite changed fixture {relative}")
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                with dest.open("xb") as output:
                    output.write(data)
            hashes[relative] = hashlib.sha256(data).hexdigest()
    # The answer manifest is never staged into GUIDE or passed to the agent.
    return manifest, hashes


def parse_verdict(text):
    def valid(value):
        return (
            isinstance(value, dict)
            and isinstance(value.get("verdict"), str)
            and value.get("verdict") in VERDICTS
            and isinstance(value.get("explanation"), str)
            and bool(value["explanation"].strip())
        )

    try:
        value = json.loads(text)
        if valid(value):
            return value["verdict"], True
    except (ValueError, TypeError):
        pass
    # Diagnostic extraction only; never upgrades strict format compliance.
    candidates = []
    decoder = json.JSONDecoder()
    cursor = 0
    while cursor < len(text):
        start = text.find("{", cursor)
        if start < 0:
            break
        try:
            value, length = decoder.raw_decode(text[start:])
            cursor = start + length
            if valid(value):
                candidates.append(value["verdict"])
        except ValueError:
            cursor = start + 1
    return (candidates[0], False) if len(candidates) == 1 else (None, False)


def evaluate(trace, sources, expected, agent=False):
    compiled = set()
    observations = []
    calls = [e for e in trace["events"] if e.get("type") == "tool"]
    for event in calls:
        args = event.get("arguments") or {}
        payload = event.get("result") or {}
        result = payload.get("structuredContent") or {}
        if payload.get("isError") or result.get("timed_out"):
            continue
        if event["name"] == "compile_rtl":
            if (
                result.get("ok")
                and result.get("returncode") == 0
                and result.get("run_id")
                and sorted(args.get("sources", [])) == sorted(sources)
                and args.get("top") == "tb"
            ):
                compiled.add(result["run_id"])
        elif event["name"] == "simulate" and args.get("run_id") in compiled:
            output = result.get("output", "")
            if "FUNCTIONAL_FAILURE" in output or "[output truncated" in output:
                continue
            if result.get("returncode") == 0 and "SECURITY_TEST_PASS" in output:
                observations.append("property_held_for_test")
            elif result.get("returncode") == 1 and "SECURITY_VIOLATION:" in output:
                observations.append("property_violated")
    observed = observations[0] if len(observations) == 1 else "inconclusive"
    final = trace.get("messages", [{}])[-1]
    verdict, formatting = parse_verdict(final.get("content") or "")
    evidence_ok = observed == expected and len(calls) == 2
    correct = verdict == expected and evidence_ok if agent else None
    return {
        "expected": expected,
        "observed": observed,
        "tool_calls": len(calls),
        "evidence_passed": evidence_ok,
        "agent_verdict": verdict if agent else None,
        "verdict_correct": correct,
        "format_compliant": formatting if agent else None,
        "passed": bool(correct and formatting) if agent else evidence_ok,
    }


def write_report(report, directory):
    report["summary"] = {
        "completed": len(report["runs"]),
        "evidence_passed": sum(item["evidence_passed"] for item in report["runs"]),
        "verdict_correct": sum(item["verdict_correct"] is True for item in report["runs"]),
        "format_compliant": sum(item["format_compliant"] is True for item in report["runs"]),
        "strict_passed": sum(item["passed"] for item in report["runs"]),
        "execution_errors": sum(bool(item.get("error")) for item in report["runs"]),
    }
    (directory / "report.json").write_text(json.dumps(report, indent=2))
    lines = [
        f"# {report['suite']} — {report['mode']}",
        "",
        "Actual execution steps; raw tool results and model responses are in report.json.",
        "",
    ]
    for item in report["runs"]:
        lines += [
            f"## {item['case_id']} / trial {item['trial']}",
            "",
            item["requirement"],
            "",
            "1. Staged and SHA-256 hashed design and testbench.",
        ]
        calls = [event for event in item["trace"]["events"] if event["type"] == "tool"]
        for index, event in enumerate(calls, 2):
            result = event["result"].get("structuredContent") or {}
            lines += [
                f"{index}. Called `{event['name']}` with `{json.dumps(event['arguments'])}`.",
                f"   Run `{result.get('run_id')}`; exit `{result.get('returncode')}`; "
                f"timeout `{result.get('timed_out')}`.",
            ]
            checks = [
                line
                for line in result.get("output", "").splitlines()
                if "CHECK " in line or "SECURITY_" in line or "FUNCTIONAL_FAILURE" in line
            ]
            if checks:
                lines += ["", "```text", *checks, "```", ""]
        lines += [
            f"Observed: `{item['observed']}`; expected: `{item['expected']}`; "
            f"evidence passed: `{item['evidence_passed']}`; "
            f"strict result: `{item['passed']}`.",
            "",
        ]
        if item.get("error"):
            lines += [f"Execution error: {item['error']}", ""]
    (directory / "steps.md").write_text("\n".join(lines))


async def execute(args):
    root = resolve_guide_root()
    manifest, hashes = stage(root)
    args.output.mkdir(parents=True, exist_ok=False)
    client = InferenceClient() if args.agent else None
    report = {
        "suite": manifest["version"],
        "mode": "agent" if args.agent else "tools",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "repository_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip(),
        "working_tree_dirty": bool(subprocess.check_output(["git", "status", "--porcelain"])),
        "source_sha256": hashes,
        "model": client.model if client else None,
        "settings": {
            key: os.getenv(key)
            for key in ("VLLM_MODEL", "VLLM_MODEL_REVISION", "VLLM_MAX_MODEL_LEN", "VLLM_IMAGE")
        },
        "runs": [],
    }
    params = StdioServerParameters(
        command=sys.executable, args=["-m", "guide_mcp.eda_server.server"], env=dict(os.environ)
    )
    try:
        if client:
            report["served_models"] = client.models()
        async with stdio_client(params) as (read, write):
            async with ClientSession(
                read, write, read_timeout_seconds=timedelta(seconds=420)
            ) as session:
                await session.initialize()
                for trial in range(1, args.trials + 1):
                    for case in manifest["cases"]:
                        sources = [
                            f"{PREFIX}/{case['id']}/{name}" for name in ("design.sv", "tb.sv")
                        ]
                        trace = {"events": [], "messages": []}
                        error = None
                        started = time.monotonic()
                        try:
                            if client:
                                prompt = (
                                    f"Requirement: {case['requirement']} Compile exactly {json.dumps(sources)} "
                                    "with top tb, then simulate the successful run_id. Call each tool once. "
                                    "SECURITY_TEST_PASS with exit 0 means property_held_for_test; "
                                    "SECURITY_VIOLATION with exit 1 means property_violated. "
                                    "Other errors are inconclusive. Do not repair or retry. "
                                    "Return only JSON, no surrounding prose or markdown: "
                                    '{"verdict":"property_held_for_test|property_violated|inconclusive",'
                                    '"explanation":"cite actual tool evidence"}.'
                                )
                                trace = await run_loop(
                                    client, session, prompt, max_turns=4, trace=trace
                                )
                            else:
                                result = {}
                                for name in ("compile_rtl", "simulate"):
                                    arguments = (
                                        {"sources": sources, "top": "tb"}
                                        if name == "compile_rtl"
                                        else {"run_id": result["structuredContent"]["run_id"]}
                                    )
                                    result = (await session.call_tool(name, arguments)).model_dump(
                                        mode="json"
                                    )
                                    trace["events"].append(
                                        {
                                            "type": "tool",
                                            "name": name,
                                            "arguments": arguments,
                                            "result": result,
                                        }
                                    )
                                    if name == "compile_rtl" and not (
                                        result.get("structuredContent") or {}
                                    ).get("ok"):
                                        break
                        except Exception as exc:
                            error = f"{type(exc).__name__}: {exc}"
                        if not trace["messages"]:
                            trace["messages"] = [{}]
                        item = {
                            "case_id": case["id"],
                            "family": case["family"],
                            "requirement": case["requirement"],
                            "trial": trial,
                            **evaluate(trace, sources, case["expected"], args.agent),
                            "elapsed_seconds": time.monotonic() - started,
                            "error": error,
                            "trace": trace,
                        }
                        if error:
                            item["passed"] = False
                        report["runs"].append(item)
                        write_report(report, args.output)
                        print(
                            f"{case['id']} trial={trial} observed={item['observed']} passed={item['passed']}",
                            flush=True,
                        )
        report["passed"] = all(item["passed"] for item in report["runs"])
        write_report(report, args.output)
        return report
    finally:
        if client:
            client.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--agent",
        action="store_true",
        help="Evaluate Qwen tool use; default is deterministic MCP validation",
    )
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="New result directory; existing results are never overwritten",
    )
    args = parser.parse_args()
    if not 1 <= args.trials <= 100:
        parser.error("trials must be 1..100")
    report = asyncio.run(execute(args))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
