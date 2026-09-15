# Security suite v1

This suite has ten synthetic designs and five requirement-based testbenches,
each applied unchanged to a safe/faulty pair. It extends, and does not replace,
the original two-case authorization baseline or its recorded failures.
See the [construction and per-case validation record](security-suite-validation-20260914.md).

| Cases | Requirement and checks | Intended fault |
| --- | --- | --- |
| 01 / 02: authorization | All eight request/privilege/bypass combinations; grant must equal request AND privilege | Bypass grants an unprivileged request |
| 03 / 04: register lock | Reset, successful preload, then all eight lock/write-port combinations; unlocked writes and idle hold must work | Alternate write port ignores lock |
| 05 / 06: debug access | All 256 bytes × four read/authorization combinations; authorized reads work and other outputs are zero | Unauthorized debug reads expose the byte |
| 07 / 08: reset clearing | Load and hold each nonzero byte, then reset with load both inactive and active; reset must dominate load | Load wins over reset, leaving nonzero data visible |
| 09 / 10: output isolation | All 256 bytes × both enable states; enabled output matches the byte and disabled output is zero | Least significant bit leaks while disabled |

Odd cases are safe, even cases contain the intended fault. This mapping and the
answer manifest are evaluator-only inputs: the runner does not put them in model
prompts or stage the manifest under GUIDE. Case IDs are not randomized or blinded
against a person familiar with the suite. Do not present these results as benchmark
accuracy or performance on unseen vulnerabilities.

## Run and retain evidence

From the guest repository, using a new output directory for every invocation:

```bash
# Deterministic compile/simulate acceptance through the production MCP server.
uv run --extra eda --env-file .env python -m runner.security_suite \
  --output results/security-v1-tools-trial-01

# Qwen tool-use evaluation, fresh conversation per case and trial.
uv run --extra eda --env-file .env python -m runner.security_suite \
  --agent --trials 3 --output results/security-v1-agent-trials-01
```

Default tool mode invokes each tool once without asking the LLM to select calls.
Agent mode uses the existing bounded OpenAI-to-MCP runner and the same local Qwen
endpoint as Hermes. It does **not** run the Hermes CLI harness. It provides the
requirement, both source paths, tool descriptions, and marker interpretation;
it withholds the expected verdict. The agent has four inference turns per case.
This measures tool use and evidence interpretation, not autonomous vulnerability
discovery, source inspection, testbench generation, or repair.

Only project-owned design/testbench files are staged in
`$GUIDE_ROOT/.llm4security-suite/security-v1/`. Changed files are not overwritten,
and upstream GUIDE is not vendored or modified. Runs use the existing disposable
Docker sandbox. Source filenames and case IDs are neutral in model prompts.

Each output directory contains:

- `report.json`: expected/observed outcomes, separate score fields, source hashes,
  repository commit and dirty status, model settings, per-case wall time, full
  tool arguments/results, and agent prompts/responses with token usage.
- `steps.md`: the actual compile/simulate calls, run IDs, exit codes, timeout flags,
  and every retained testbench `CHECK` line and assertion result for each case.
- Referenced EDA directories under `results/eda/<run_id>` contain compiler and
  simulator logs, exact invocation arguments, image/binary/source provenance,
  compiled artifacts, and waveforms. Preserve those alongside the report.

The runner writes progress after each case, continues after per-case errors, and
exits nonzero if any strict result fails. It refuses to reuse an output directory.
Faulty simulations stop at the first violated assertion; their logs do not imply
that later stimuli were executed. All testbenches use `1ns/1ps` timing.

## Scoring

- `evidence_passed`: exactly two tool calls, a successful compile of the specified
  sources/top, and a simulation linked to that compile with the expected marker
  and return code. Timeout, compiler failure, unrelated run IDs, functional
  failures, and truncated output cannot be accepted as a security detection.
- `verdict_correct`: the recognized agent verdict agrees with the expected outcome
  and the tool evidence passes. A unique JSON object embedded in prose may count
  here, but ambiguous or missing objects do not.
- `format_compliant`: the entire response is a valid JSON object containing an
  allowed verdict and a nonempty explanation. Prose before JSON fails this field.
- `passed`: tool mode requires evidence acceptance; agent mode additionally
  requires both correct verdict and strict format compliance.

Explanations and cited evidence are retained for review; the evaluator does not
automatically establish that every sentence in an explanation is correct. Report
the three dimensions separately rather than concealing format failures by changing
the scoring rule after a trial.

## Checks performed during construction

1. Defined each interface and security requirement before its testbench checks.
2. Applied the same testbench to both members of each pair.
3. Compiled and simulated all ten using real Icarus locally; safe cases passed and
   faulty cases failed with the intended assertion, not a compiler/runtime error.
4. Replaced every safe circuit with an always-zero output mutant and confirmed
   each testbench rejected the loss of normal functionality.
5. Tested evaluator rejection of unrelated simulation IDs, timeouts, failed
   compilation, functional failures, extra calls, and ambiguous verdicts.
6. Tested fixture staging refuses changed files and does not stage answer labels.
7. Ran all ten through the VM's Docker-backed MCP server: 10/10 expected outcomes.
   Per-case execution logs are in `results/security-v1-tools-20260914/steps.md`.

Sequential tests cover the documented sequences, not every possible history.
Combinational enumeration covers these small interfaces only. These tests are
not formal proofs, timing-side-channel analyses, Trojan benchmarks, or independent
external validation. Broader held-out designs, reviewed testbenches, randomized
case identities, repeated trials, and a source-reading interface are next work.
