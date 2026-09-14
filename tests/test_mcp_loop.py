import asyncio
import json
import os
import sys
from types import SimpleNamespace

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from guide_mcp.eda_server.server import create_server
from guide_mcp.eda_server.tools import ToolResult
from runner.eda_loop import run_loop


class FakeBackend:
    def compile_rtl(self, sources: list[str], top: str | None = None) -> ToolResult:
        return ToolResult(ok=True, summary="compiled", run_id="a" * 32)

    def simulate(self, run_id: str) -> ToolResult:
        return ToolResult(ok=True, summary="simulated", run_id="b" * 32, output="PASS")


def test_mcp_schema_discovery():
    async def check():
        server = create_server(FakeBackend())
        tools = await server.list_tools()
        assert {t.name for t in tools} == {"compile_rtl", "simulate"}
        compile_tool = next(t for t in tools if t.name == "compile_rtl")
        assert compile_tool.inputSchema["properties"]["sources"]["type"] == "array"
        assert "sources" in compile_tool.inputSchema["required"]
        assert compile_tool.outputSchema["properties"]["ok"]["type"] == "boolean"
        _, structured = await server.call_tool("compile_rtl", {"sources": ["tb.sv"]})
        assert structured["ok"] is True

    asyncio.run(check())


def test_real_stdio_transport(tmp_path):
    guide = tmp_path / "GUIDE"
    guide.mkdir()
    (guide / ".gitmodules").write_text("")

    async def check():
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "guide_mcp.eda_server.server"],
            env={
                **os.environ,
                "GUIDE_ROOT": str(guide),
                "EDA_ARTIFACT_ROOT": str(tmp_path / "runs"),
            },
        )
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                assert {t.name for t in (await session.list_tools()).tools} == {
                    "compile_rtl",
                    "simulate",
                }
                response = await session.call_tool("compile_rtl", {"sources": ["../escape.sv"]})
                assert response.isError

    asyncio.run(check())


class FakeSession:
    def __init__(self):
        self.calls = []

    async def list_tools(self):
        return SimpleNamespace(tools=await create_server(FakeBackend()).list_tools())

    async def call_tool(self, name, arguments):
        self.calls.append((name, arguments))
        result = getattr(FakeBackend(), name)(**arguments).model_dump()
        return SimpleNamespace(
            model_dump=lambda **kwargs: {
                "isError": False,
                "structuredContent": result,
                "content": [{"type": "text", "text": json.dumps(result)}],
            }
        )


class FakeClient:
    def __init__(self, names):
        self.names = iter(names)

    def chat(self, messages, **kwargs):
        name = next(self.names, None)
        if name:
            arguments = (
                {"sources": ["tb.sv"], "top": "tb"}
                if name == "compile_rtl"
                else {"run_id": "a" * 32}
            )
            message = {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": name + "-id",
                        "function": {"name": name, "arguments": json.dumps(arguments)},
                    }
                ],
            }
        else:
            message = {"role": "assistant", "content": "The simulation returned PASS."}
        return {"choices": [{"message": message}]}


def test_loop_returns_tool_evidence_and_budget():
    session = FakeSession()
    report = asyncio.run(run_loop(FakeClient(["compile_rtl", "simulate"]), session, "test"))
    assert report["status"] == "completed"
    assert [name for name, _ in session.calls] == ["compile_rtl", "simulate"]
    assert len([m for m in report["messages"] if m["role"] == "tool"]) == 2
    report = asyncio.run(run_loop(FakeClient(["compile_rtl"] * 5), FakeSession(), "test", 2))
    assert report["status"] == "budget_exhausted"


def test_unknown_tool_is_not_executed():
    session = FakeSession()
    report = asyncio.run(run_loop(FakeClient(["shell"]), session, "test"))
    assert not session.calls
    assert report["events"][1]["result"]["isError"]


def test_early_answer_is_incomplete():
    report = asyncio.run(run_loop(FakeClient([]), FakeSession(), "test"))
    assert report["status"] == "incomplete"


def test_model_to_real_mcp_to_real_icarus(tmp_path):
    import shutil

    import pytest

    if not shutil.which("iverilog"):
        pytest.skip("Icarus required")
    guide = tmp_path / "GUIDE"
    guide.mkdir()
    (guide / ".gitmodules").write_text("")
    (guide / "tb.sv").write_text(
        'module tb; initial begin $display("PASS"); $finish; end endmodule'
    )

    class Model:
        turn = 0

        def chat(self, messages, **kwargs):
            self.turn += 1
            if self.turn == 1:
                name, arguments = "compile_rtl", {"sources": ["tb.sv"], "top": "tb"}
            elif self.turn == 2:
                result = json.loads(messages[-1]["content"])["structuredContent"]
                assert result["ok"], result
                name, arguments = "simulate", {"run_id": result["run_id"]}
            else:
                result = json.loads(messages[-1]["content"])["structuredContent"]
                assert result["ok"] and "PASS" in result["output"], result
                return {"choices": [{"message": {"role": "assistant", "content": "PASS"}}]}
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [
                                {
                                    "id": str(self.turn),
                                    "type": "function",
                                    "function": {"name": name, "arguments": json.dumps(arguments)},
                                }
                            ],
                        }
                    }
                ]
            }

    async def check():
        # The injected host adapter is test-only and executes this trusted fixture only.
        script = (
            "from guide_mcp.eda_server.server import create_server; "
            "from guide_mcp.eda_server.tools import EdaTools; "
            "from tests.test_eda import NativeTestSandbox; "
            "create_server(EdaTools(sandbox_factory=NativeTestSandbox)).run()"
        )
        params = StdioServerParameters(
            command=sys.executable,
            args=["-c", script],
            env={
                **os.environ,
                "GUIDE_ROOT": str(guide),
                "EDA_ARTIFACT_ROOT": str(tmp_path / "runs"),
            },
        )
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                report = await run_loop(Model(), session, "Compile tb.sv and simulate tb")
                assert report["status"] == "completed"

    asyncio.run(check())
