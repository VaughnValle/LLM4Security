from pathlib import Path

import pytest

from integrations.guide.paths import resolve_guide_root


def test_resolve_explicit_guide_root(tmp_path: Path):
    guide = tmp_path / "GUIDE"
    guide.mkdir()
    (guide / ".gitmodules").write_text("")
    assert resolve_guide_root(guide) == guide.resolve()


def test_missing_guide_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("GUIDE_ROOT", raising=False)
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        resolve_guide_root(tmp_path / "missing")


def test_explicit_invalid_path_does_not_fall_back(tmp_path, monkeypatch):
    valid = tmp_path / "GUIDE"
    valid.mkdir()
    (valid / ".gitmodules").write_text("")
    monkeypatch.setenv("GUIDE_ROOT", str(valid))
    with pytest.raises(FileNotFoundError):
        resolve_guide_root(tmp_path / "missing")
