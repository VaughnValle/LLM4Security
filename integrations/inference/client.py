"""OpenAI-wire client used by deployment probes and the minimal EDA loop."""

import os

import httpx


class InferenceClient:
    def __init__(self, *, base_url=None, api_key=None, model=None, transport=None):
        self.model = model or os.getenv("LLM_MODEL", "Qwen3.8-27B")
        self.http = httpx.Client(
            base_url=(base_url or os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:8000/v1")).rstrip(
                "/"
            )
            + "/",
            headers={"Authorization": f"Bearer {api_key or os.getenv('OPENAI_API_KEY', 'local')}"},
            timeout=httpx.Timeout(300, connect=10),
            transport=transport,
        )

    def close(self):
        self.http.close()

    def models(self):
        response = self.http.get("models")
        response.raise_for_status()
        ids = [model["id"] for model in response.json()["data"]]
        if self.model not in ids:
            raise ValueError(f"Expected served model {self.model!r}; endpoint returned {ids}")
        return ids

    def chat(self, messages, *, tools=None, tool_choice="auto", max_tokens=512):
        body = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0,
            "chat_template_kwargs": {"enable_thinking": False},
        }
        if tools:
            body.update(tools=tools, tool_choice=tool_choice, parallel_tool_calls=False)
        response = self.http.post("chat/completions", json=body)
        response.raise_for_status()
        data = response.json()
        choice = data["choices"][0]
        if choice.get("finish_reason") == "length":
            raise ValueError("Generation was truncated; increase the output budget")
        return data
