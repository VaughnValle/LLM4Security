# Synthetic authorization baseline

This experiment tests whether one Qwen agent can use compiler/simulator evidence
to distinguish a passing circuit from an authorization bypass. It is a small
development baseline, not a GUIDE benchmark result or an estimate of detection accuracy.

Both circuits expose `request`, `privileged`, `bypass`, and `grant`. The requirement
is `grant == (request & privileged)` regardless of `bypass`. Case A implements that
requirement. Case B deliberately permits bypass. The testbench checks all eight
input combinations and calls `$fatal(1)` on the first mismatch. Its explicit
`timescale` makes simulation times unambiguous.

From the guest repository:

```bash
uv run --extra eda --env-file .env python -m runner.baseline
```

The runner stages only these project-owned fixtures into
`$GUIDE_ROOT/.llm4security-baseline/authorization`. Existing changed files are never
overwritten; upstream GUIDE sources remain untouched. Each case has a fresh agent
history and a four-turn limit with the same model and tool schemas. The agent sees
the requirement and paths, not the expected case label. It must compile, simulate,
and return a JSON verdict with an explanation. It has no source-writing tool.

The evaluator checks that the model selected the specified files and linked the
simulation to its successful compile. It recognizes a violation only from the
assertion marker plus return code 1; timeouts, compilation errors, or unrelated
run IDs cannot count as successful detections. The raw generic loop may report
`incomplete` for the deliberately failing design because that loop's ordinary
acceptance condition requires successful simulation. The baseline's separate
`passed` field evaluates the expected failure correctly.

`results/authorization-baseline.json` records prompts, responses, actual tool
arguments/results, model/checkpoint settings, source hashes, repository commit,
token usage, latency, expected outcomes, observed outcomes, and model verdicts.
Referenced EDA result files include source/binary hashes and container image IDs.
Preserve these together when exporting evidence. Run with a new `--output` path
to retain independent trials.

This validates evidence interpretation for a deliberately simple property. Next
research work should add larger labeled cases, independent testbenches, repeated
trials, and a controlled source inspection/edit interface before autonomous repair.
The current two-tool interface cannot autonomously revise RTL files.
