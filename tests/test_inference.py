import json

import httpx
import pytest

from integrations.inference.client import InferenceClient
from integrations.inference.serve import command
from integrations.inference.smoke import probe


def test_single_gpu_command_does_not_leak_key():
    argv = command({"VLLM_MODEL_REVISION": "a" * 40, "VLLM_API_KEY": "secret"})
    assert "secret" not in argv
    assert argv[argv.index("--tensor-parallel-size") + 1] == "1"
    assert argv[argv.index("--max-model-len") + 1] == "8192"
    assert "--enable-auto-tool-choice" in argv
    assert "--trust-remote-code" not in argv


@pytest.mark.parametrize(
    "overrides",
    [
        {"VLLM_MODEL_REVISION": ""},
        {"VLLM_MODEL_REVISION": "main"},
        {"VLLM_MAX_NUM_SEQS": "3"},
        {"VLLM_MAX_MODEL_LEN": "1000000"},
        {"VLLM_GPU_MEMORY_UTILIZATION": "nan"},
        {"VLLM_API_KEY": ""},
    ],
)
def test_invalid_launch_settings(overrides):
    with pytest.raises(ValueError):
        command({"VLLM_MODEL_REVISION": "a" * 40, "VLLM_API_KEY": "secret", **overrides})


def test_openai_tool_round_trip():
    seen = []

    def handle(request):
        assert request.headers["Authorization"] == "Bearer secret"
        assert request.url.path.startswith("/v1/")
        if request.method == "GET":
            return httpx.Response(200, json={"data": [{"id": "Qwen3.8-27B"}]})
        body = json.loads(request.content)
        seen.append(body)
        if body.get("tools"):
            assert body["tool_choice"] == "auto"
            message = {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": "call1",
                        "type": "function",
                        "function": {"name": "endpoint_probe", "arguments": '{"value":7}'},
                    }
                ],
            }
        else:
            message = {"role": "assistant", "content": "PROBE_OK_7"}
        return httpx.Response(
            200, json={"choices": [{"message": message, "finish_reason": "stop"}]}
        )

    client = InferenceClient(api_key="secret", transport=httpx.MockTransport(handle))
    try:
        assert probe(client)["models"] == ["Qwen3.8-27B"]
        assert seen[-1]["messages"][-2]["tool_call_id"] == "call1"
    finally:
        client.close()


def test_model_mismatch_and_http_failure():
    client = InferenceClient(
        transport=httpx.MockTransport(
            lambda r: httpx.Response(200, json={"data": [{"id": "wrong"}]})
        )
    )
    with pytest.raises(ValueError, match="Expected served model"):
        client.models()
    client.close()
    client = InferenceClient(transport=httpx.MockTransport(lambda r: httpx.Response(401)))
    with pytest.raises(httpx.HTTPStatusError):
        client.models()
    client.close()


def test_truncated_generation_is_rejected():
    client = InferenceClient(
        transport=httpx.MockTransport(
            lambda r: httpx.Response(
                200,
                json={"choices": [{"finish_reason": "length", "message": {"content": "partial"}}]},
            )
        )
    )
    try:
        with pytest.raises(ValueError, match="truncated"):
            client.chat([{"role": "user", "content": "hello"}])
    finally:
        client.close()
