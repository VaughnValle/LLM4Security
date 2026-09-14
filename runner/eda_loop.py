"""A bounded single-agent OpenAI -> MCP -> tool-result feedback loop."""

import argparse
import asyncio
import json
import os
import sys
from datetime import timedelta
from pathlib import Path

import jsonschema
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from integrations.inference.client import InferenceClient


async def run_loop(client, session, prompt, max_turns=8):
    if not 1 <= max_turns <= 20:
        raise ValueError("max_turns must be between 1 and 20")
    discovered = (await session.list_tools()).tools
    allowed = {t.name: t for t in discovered if t.name in ("compile_rtl", "simulate")}
    if set(allowed) != {"compile_rtl", "simulate"}:
        raise ValueError("MCP server must expose compile_rtl and simulate")
    wire_tools = [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description or "",
                "parameters": t.inputSchema,
            },
        }
        for t in allowed.values()
    ]
    messages = [
        {
            "role": "system",
            "content": "Compile the provided GUIDE-relative sources, then simulate "
            "the successful run_id. Use tool evidence. On errors explain or retry within the budget. "
            "A simulation exit code alone does not prove a security property. Do not invent results.",
        },
        {"role": "user", "content": prompt},
    ]
    events = []
    compiled_ids = set()
    verified = False
    for _ in range(max_turns):
        response = await asyncio.to_thread(client.chat, messages, tools=wire_tools)
        message = response["choices"][0]["message"]
        messages.append(message)
        events.append({"type": "inference", "response": response})
        calls = message.get("tool_calls") or []
        if not calls:
            return {
                "status": "completed" if verified else "incomplete",
                "messages": messages,
                "events": events,
            }
        if len(calls) > 2:
            raise ValueError("Model exceeded the per-turn tool-call budget")
        for call in calls:
            name = call["function"]["name"]
            arguments = None
            try:
                if name not in allowed:
                    raise ValueError("Tool is not allowed")
                arguments = json.loads(call["function"]["arguments"])
                jsonschema.validate(arguments, allowed[name].inputSchema)
                result = await session.call_tool(name, arguments)
                payload = result.model_dump(mode="json")
                evidence = payload.get("structuredContent") or {}
                if not payload.get("isError") and evidence.get("ok"):
                    if name == "compile_rtl" and evidence.get("run_id"):
                        compiled_ids.add(evidence["run_id"])
                    elif name == "simulate" and arguments.get("run_id") in compiled_ids:
                        verified = True
            except (ValueError, jsonschema.ValidationError) as exc:
                payload = {"isError": True, "error": str(exc)[:2000]}
            events.append({"type": "tool", "name": name, "arguments": arguments, "result": payload})
            messages.append(
                {"role": "tool", "tool_call_id": call["id"], "content": json.dumps(payload)}
            )
    return {"status": "budget_exhausted", "messages": messages, "events": events}


async def execute(args):
    client = InferenceClient()
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
                prompt = f"Compile sources {json.dumps(args.sources)} with top {args.top}, then simulate."
                return await run_loop(client, session, prompt, args.max_turns)
    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", help="Paths relative to GUIDE_ROOT")
    parser.add_argument("--top", required=True)
    parser.add_argument("--max-turns", type=int, default=8)
    parser.add_argument("--output", type=Path, default=Path("results/eda-loop.json"))
    args = parser.parse_args()
    try:
        report = asyncio.run(execute(args))
    except Exception as exc:
        report = {"status": "error", "error": str(exc)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2))
    print(f"{report['status']}: {args.output}")
    if report["status"] != "completed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
