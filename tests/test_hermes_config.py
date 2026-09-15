from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from scripts import configure_hermes


@pytest.mark.parametrize("context", [8192, 32768, 65536])
def test_hermes_context_matches_authenticated_endpoint(tmp_path, monkeypatch, capsys, context):
    config = tmp_path / ".hermes/config.yaml"
    config.parent.mkdir()
    original = "model:\n  default: previous\n"
    config.write_text(original)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "test-private-key")
    monkeypatch.setattr(configure_hermes, "resolve_guide_root", lambda: tmp_path / "GUIDE")
    response = SimpleNamespace(
        raise_for_status=lambda: None,
        json=lambda: {"data": [{"id": "test-model", "max_model_len": context}]},
    )
    monkeypatch.setattr(
        configure_hermes,
        "InferenceClient",
        lambda: SimpleNamespace(
            model="test-model",
            http=SimpleNamespace(get=lambda path: response),
            close=lambda: None,
        ),
    )
    if context < 64000:
        with pytest.raises(SystemExit, match="refusing metadata override"):
            configure_hermes.main()
        assert config.read_text() == original
    else:
        configure_hermes.main()
        saved = yaml.safe_load(config.read_text())
        assert saved["model"]["context_length"] == context
        assert saved["model"]["api_key"] == "test-private-key"
        assert config.stat().st_mode & 0o777 == 0o600
        assert saved["platform_toolsets"]["cli"] == ["guide-eda-mcp"]
        assert "test-private-key" not in capsys.readouterr().out
