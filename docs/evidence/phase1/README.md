# Phase 1 public evidence

These files are sanitized copies of the ignored execution records generated on
the research VM. They retain prompts, model responses, tool arguments/results,
source hashes, run identifiers, timings, token usage, and test output needed to
audit the reported Phase 1 results.

Machine-specific repository and GUIDE paths are represented by `<REPO_ROOT>` and
`<GUIDE_ROOT>`. The Hermes session identifier is redacted. No API credentials are
included. `manifest.json` records SHA-256 hashes of the four published evidence
files after sanitization.

Regenerate the copies from the corresponding local `results/` files with:

```bash
uv run --no-sync python scripts/publish_phase1_evidence.py
```

The raw compiler, simulator, and waveform directories remain ignored because
they are generated artifacts. The published JSON records contain their run IDs,
paths, command output, source hashes, and runtime provenance.
