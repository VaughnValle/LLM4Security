"""Check model discovery, generation, auto tool calling and tool-result consumption."""

import argparse
import json
import os
import time
from pathlib import Path

from .client import InferenceClient


def probe(client, padding_repeats=0):
    start = time.monotonic()
    report = {
        "padding_repeats": padding_repeats,
        "models": client.models(),
        "deployment": {
            key: os.getenv(key)
            for key in (
                "VLLM_IMAGE",
                "VLLM_MODEL",
                "VLLM_MODEL_REVISION",
                "VLLM_MAX_MODEL_LEN",
                "VLLM_MAX_NUM_SEQS",
                "VLLM_TOOL_PARSER",
            )
        },
    }
    first = client.chat([{"role": "user", "content": "Reply with READY."}])
    if not first["choices"][0]["message"].get("content"):
        raise ValueError("Endpoint returned no assistant content")
    report["generation"] = first
    tools = [
        {
            "type": "function",
            "function": {
                "name": "endpoint_probe",
                "description": "Return the probe value for an integer input.",
                "parameters": {
                    "type": "object",
                    "properties": {"value": {"type": "integer"}},
                    "required": ["value"],
                    "additionalProperties": False,
                },
            },
        }
    ]
    messages = [
        {
            "role": "user",
            "content": "padding " * padding_repeats
            + "\nCall endpoint_probe with value 7. Do not answer without it.",
        }
    ]
    response = client.chat(messages, tools=tools)
    message = response["choices"][0]["message"]
    calls = message.get("tool_calls") or []
    if len(calls) != 1 or calls[0]["function"]["name"] != "endpoint_probe":
        raise ValueError("Auto tool calling did not produce exactly one endpoint_probe call")
    call = calls[0]
    if not call.get("id") or json.loads(call["function"]["arguments"]) != {"value": 7}:
        raise ValueError("Tool call ID or JSON arguments are invalid")
    messages += [
        message,
        {"role": "tool", "tool_call_id": call["id"], "content": '{"result":"PROBE_OK_7"}'},
        {"role": "user", "content": "Return the exact result string from the tool."},
    ]
    final = client.chat(messages)
    if "PROBE_OK_7" not in (final["choices"][0]["message"].get("content") or ""):
        raise ValueError("Endpoint failed to consume the tool result")
    report.update(tool_call=response, tool_result=final, elapsed_seconds=time.monotonic() - start)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--padding-repeats",
        type=int,
        default=0,
        help="Add repeated words; inspect usage.prompt_tokens for actual context size",
    )
    parser.add_argument("--output", type=Path, default=Path("results/inference-smoke.json"))
    parser.add_argument(
        "--min-prompt-tokens",
        type=int,
        default=0,
        help="Fail if the measured tool-call prompt is shorter than this acceptance target",
    )
    args = parser.parse_args()
    if not 0 <= args.padding_repeats <= 64000:
        parser.error("padding-repeats must be 0..64000")
    if not 0 <= args.min_prompt_tokens <= 65536:
        parser.error("min-prompt-tokens must be 0..65536")
    client = InferenceClient()
    try:
        report = {"ok": True, **probe(client, args.padding_repeats)}
        measured = report["tool_call"].get("usage", {}).get("prompt_tokens", 0)
        report["min_prompt_tokens"] = args.min_prompt_tokens
        if measured < args.min_prompt_tokens:
            report.update(
                ok=False,
                error=f"Measured {measured} prompt tokens; "
                f"required at least {args.min_prompt_tokens}",
            )
    except Exception as exc:
        report = {"ok": False, "error": str(exc)}
    finally:
        client.close()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    if not report["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
