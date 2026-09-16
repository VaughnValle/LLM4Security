# LLM4Security: Phase 1 Progress Report

**Report date:** 15 September 2026  
**Scope:** Local inference, agent–tool integration, and initial security-test evaluation

## 1. Summary of progress

The local platform now allows an LLM to invoke hardware-design tools and interpret
their results. It runs Qwen3.8-27B with a validated
65,536-token context limit on a single AMD Radeon AI PRO R9700. Hermes can invoke
compilation and simulation through a structured tool interface, and a separate
evaluation runner records model responses, tool calls, execution evidence, and
performance measurements.

The initial evaluation comprises ten synthetic RTL designs: five safe designs
and five deliberately faulty counterparts. All ten produced the expected outcome
under deterministic compilation/simulation. In one Qwen-driven trial, all ten
also passed the requirements for correct tool use, evidence-supported verdicts,
and JSON response formatting. The final guest regression suite passed 67 tests.

This first evaluation covers tool use and interpretation of supplied test evidence.
Autonomous vulnerability discovery, formal verification, and comparisons between
single-agent and multi-agent workflows have not yet been tested.

## 2. Research objective and architectural setup

The research question is whether specialized LLM roles improve hardware-security
analysis compared with a single tool-using agent. The current implementation
provides the inference service, EDA tools, and initial evaluation procedure for
that comparison.

| Layer | Implemented configuration |
| --- | --- |
| Physical host | AMD Ryzen 9 3950X, 96 GB system RAM, Proxmox |
| Linux guest | Ubuntu VM, 16 virtual CPUs, 64 GB RAM, 300 GB thin-provisioned disk |
| Accelerator | One Radeon AI PRO R9700, nominal 32 GB VRAM, passed through to the VM; ROCm identifies `gfx1201` |
| Inference | Dockerized ROCm/vLLM service; authenticated OpenAI-compatible endpoint bound to guest loopback |
| Model | `amd/Qwen3.8-27B-Quark-AWQ-INT4-W4A16`; pinned checkpoint revision; 4-bit weight quantization |
| Serving policy | Text-only, one GPU, 65,536-token limit, one active generation, eager execution, 85% GPU-memory budget |
| Interactive agent | Hermes configured for the local endpoint and `guide-eda-mcp` |
| EDA execution | Icarus Verilog 12.0 compilation and simulation in disposable Docker containers |
| Benchmark integration | External GUIDE checkout selected through `GUIDE_ROOT`; GUIDE is not vendored into LLM4Security |
| Evidence storage | JSON traces, source/binary hashes, tool logs, run IDs, and VCD waveforms |

Inference uses the GPU; compilation and simulation use CPU resources. The EDA
containers have no network access, use read-only source inputs, and enforce
execution/resource limits. Generated artifacts are exported into separate result
directories. Project-owned test fixtures are staged under a dedicated subdirectory
of the external GUIDE checkout; existing changed fixtures are not overwritten.

The vLLM image includes a checksum-pinned upstream backport for the checkpoint's
Quark INT4 format. This is a reproducibility dependency: replacing the image or
runtime requires repeating acceptance tests. The deployed checkpoint revision is
`0f7ee2559e8dbc25879e1fe1677b2b10708b91a9`.

## 3. Agent setup and experimental protocol

There are two validated execution paths:

1. **Hermes integration test:** a fresh Hermes session discovered the MCP tools,
   compiled a NOT-gate design together with its testbench, and simulated the
   returned compilation run. The saved simulator output contained
   `GUIDE_NOTGATE_PASS` and a waveform artifact.
2. **Controlled Qwen evaluation:** a Python runner used the same local model
   endpoint and MCP tools for the ten-case suite. This path recorded complete
   prompts, responses, tool arguments/results, token counts, and case timings.
   The ten-case performance results below are from this runner, not the Hermes CLI.

The implemented tool interface contains:

- `compile_rtl(sources, top, timeout_seconds)`: compiles explicit GUIDE-relative
  sources and returns a compilation run ID and associated evidence.
- `simulate(run_id, timeout_seconds)`: simulates the compiled artifact identified
  by that run ID and returns a separate simulation record.

The Qwen runner used temperature 0, thinking disabled, a maximum of 512 generated
tokens per request, and a four-turn inference budget per case. Parallel tool calls
were disabled. Each case began with a fresh conversation. Every completed case
used three inference requests and two tool calls: compile, simulate, and a final
verdict after consuming both tool results.

The planned Supervisor, Hardware Security Analyst, Verification Agent, and Critic
remain logical role definitions rather than an implemented four-agent workflow.
They can eventually share the existing endpoint with separate histories and tool
permissions. A second GPU is not required for role separation or blind review;
it would provide additional serving capacity, subject to deployment testing.

## 4. Prompts and expected responses

### Hermes prompts: startup and tool integration

The following are user prompts submitted to Hermes, not its internally assembled
system prompt. They served different purposes from the ten-case evaluation.

**Initial responsiveness check:**

> Reply with READY.

Hermes returned `READY` in the recorded interactive exchange. This checked basic
agent initialization and response generation only; it did not establish tool use
or long-context capacity.

**Final compile/simulate acceptance prompt:**

```text
Use guide-eda-mcp. Make each tool call separately. Call compile_rtl exactly once with sources=["benchmark/VerilogEval/dataset_spec-to-rtl/Prob005_notgate_ref.sv",".llm4security-smoke/notgate_acceptance.sv"] and top="tb". Both files are required. Then call simulate with that successful compile run_id. Report the actual run IDs and testbench pass marker. Do not read files or batch calls.
```

This is the prompt supplied through the recorded Hermes CLI invocation. The run
used `hermes chat --oneshot --max-turns 12 --run-budget 300 --quiet -q` with that
prompt. Its session ID was `20260914_203319_f11a4f`.

The resulting evidence was:

- Compilation run `0d9f479e90874e34a00775e104b3d31f`: exit code 0.
- Simulation run `641dc175436840b0903373ebf2827621`: exit code 0 and the
  `GUIDE_NOTGATE_PASS` marker, with a saved waveform.

The prompt explicitly named both source files and required separate calls because
an earlier attempt omitted the testbench and attempted an unsupported batched
call. This successful run therefore demonstrates tool integration under explicit
instructions, not independent selection of source files or verification strategy.
The saved Hermes response misstated the simulation time; the pass result was
checked against the underlying EDA records, and that timing statement is not used
as a measurement in this report.

The [saved Hermes response](evidence/phase1/hermes-64k-acceptance-final.log) contains the
answer with its session identifier redacted; the input prompt above comes from the
recorded invocation, since the quiet-mode output file does not echo it.

### Evaluation-runner prompts: ten-case trial

The separate Qwen evaluation runner's system prompt was:

> Compile the provided GUIDE-relative sources, then simulate the successful run_id.
> Use tool evidence. On errors explain or retry within the budget. A simulation exit
> code alone does not prove a security property. Do not invent results.

The case-specific user prompt supplied the requirement and the two source paths.
For example, the authorization case used the following instructions, with the
literal file paths abbreviated here; the exact prompt is retained in the trace:

> Requirement: Access is granted exactly when request and privileged are both
> asserted, regardless of bypass. Compile exactly [design path, testbench path]
> with top tb, then simulate the successful run_id. Call each tool once.
> SECURITY_TEST_PASS with exit 0 means property_held_for_test;
> SECURITY_VIOLATION with exit 1 means property_violated. Other errors are
> inconclusive. Do not repair or retry. Return only JSON, no surrounding prose
> or markdown.

The requested response structure was:

```json
{"verdict":"property_held_for_test|property_violated|inconclusive",
 "explanation":"cite actual tool evidence"}
```

The case instruction narrowed the general retry allowance to one call per tool.
The expected safe/faulty label was withheld from the agent, but the testbench and
meaning of its result markers were supplied. Accordingly, this is a deliberately
constrained evidence-interpretation task, not an unaided security-analysis task.
The evaluator checks verdicts and format; explanations remain available for review
and are not automatically certified sentence by sentence.

## 5. Testbench construction and checks

The suite contains five requirement-based testbenches, each applied unchanged to
both members of a safe/faulty pair. RTL describes the circuit's behavior; the
testbench supplies inputs and checks outputs against the stated requirement.

| Family | Requirement and test coverage | Injected fault |
| --- | --- | --- |
| Authorization | All 8 combinations of request, privilege, and bypass; grant must equal request AND privilege | Bypass permits unprivileged access |
| Register locking | Reset/preload checks and all 8 lock/write-port combinations; unlocked writes work and locked contents remain unchanged | Alternate write port ignores the lock |
| Debug access | All 256 protected bytes × 4 read/authorization combinations | Unauthorized debug reads expose protected data |
| Reset clearing | Load/hold each of 255 nonzero bytes, then reset with load inactive and active: 510 reset checks | Load takes priority over reset |
| Output isolation | All 256 protected bytes × 2 enable states | Disabled output exposes the least significant bit |

For example, the authorization designs differ in their grant expression:

```systemverilog
// Safe design
assign grant = request & privileged;
// Faulty counterpart
assign grant = request & (privileged | bypass);
```

The testbench enumerates the inputs and asserts the requirement using a
four-state comparison, so an unknown output cannot silently pass:

```systemverilog
if (grant !== (request & privileged))
    $fatal(1, "SECURITY_VIOLATION: authorization");
```

Successful completion prints `SECURITY_TEST_PASS`. Security violations terminate
with an explicit marker and exit code 1; normal-operation failures use a separate
`FUNCTIONAL_FAILURE` marker where applicable. Failing cases stop at the first
violation, so their logs do not imply execution of later stimuli. All testbenches
use explicit `1ns/1ps` timing and export waveforms.

Construction checks included real local compilation/simulation of every case,
followed by the same suite through the VM's Docker-backed MCP server. Each safe
design was additionally replaced with an always-zero-output mutant; all five
mutants were rejected. This checks that the testbenches do not accept a circuit
merely because it disables useful functionality.

## 6. Findings and performance

### Context capacity

Staged context tests succeeded on the same single R9700:

| Serving limit | Actual long-prompt input | Complete probe time | Outcome |
| --- | ---: | ---: | --- |
| 16,384 tokens | 14,292 tokens | 33.35 s | Passed |
| 32,768 tokens | 30,292 tokens | 64.03 s | Passed |
| 65,536 tokens | 64,292 tokens | 148.20 s | Passed |

Each probe included short generation, a long-prompt tool call, and consumption
of the tool result. These are capacity/protocol checks, not tests of long-document
reasoning quality or steady-state decoding throughput.

An initial 8K server setting had been mistaken for a hardware limit. The apparent
high VRAM usage was largely a reserved cache pool, not the memory demand of a
single 8K request. Raising the actual server limit and testing it resolved this:
the current 64K configuration does not require a second GPU or configured CPU
offload. A runtime inspection recorded 16.74 GiB for model loading and 8.94 GiB
available for GPU KV cache. Hermes was also corrected to advertise the same
context limit as the server; an earlier mismatch had caused request failures.

### Ten-case trial

| Test family | Safe case time | Faulty case time | Strict agent results |
| --- | ---: | ---: | --- |
| Authorization | 40.99 s | 40.65 s | 2/2 passed |
| Register locking | 44.24 s | 42.25 s | 2/2 passed |
| Debug access | 90.82 s | 41.64 s | 2/2 passed |
| Reset clearing | 58.10 s | 44.35 s | 2/2 passed |
| Output isolation | 64.77 s | 39.20 s | 2/2 passed |

The deterministic MCP-only run matched all ten expected outcomes in **8.48 seconds**
of summed case time. The Qwen-driven run required **507.01 seconds** (8 min 27 s),
with a mean of **50.70 seconds** and median of **43.24 seconds** per case.
These are separate runs; their comparison indicates that the agent/inference path
dominates elapsed time for these small circuits, but does not isolate decoding,
prompt processing, queueing, or transport overhead.

The agent trial made **30 inference requests** and **20 tool calls**, reporting
**145,122 input tokens** and **3,031 generated tokens** across requests. Input-token
totals include repeatedly submitted conversation history and tool results; they
are not unique source tokens or a measure of uncached computation. The debug safe
case's final request alone contained 37,088 input tokens, consistent with the
larger complete execution log contributing to its longer latency.

Three scoring dimensions were kept separate:

| Dimension | Acceptance condition | Result |
| --- | --- | ---: |
| Tool evidence | Correct sources/top; successful compile; linked simulation; expected marker/exit code; exactly two calls | 10/10 |
| Verdict correctness | Recognized verdict matches the expected outcome and accepted evidence | 10/10 |
| Format compliance | Entire final response is valid JSON with an allowed verdict and nonempty explanation | 10/10 |

Timeouts, compilation failures, unrelated run IDs, functional failures, and
truncated outputs cannot count as successful security detections. An earlier
two-case trial achieved only 1/2 strict passes: the faulty case was correctly
explained but included prose before its JSON. That result has been retained.
The newer trial does not establish that formatting reliability has been solved
or that a prompt change alone caused the improvement.

## 7. Limitations and next steps

The evaluation used one trial on ten small, project-authored synthetic
designs with supplied testbenches and explicit marker interpretation. There is
no held-out benchmark, external testbench review, formal proof, repeated-run
variance estimate, or comparison against another model or orchestration strategy.
Case identifiers are not randomized. Temperature 0 alone does not establish
reproducibility across runs or runtime versions.

The agent currently cannot independently browse source files, author or repair RTL
through the tool interface, or invoke synthesis/formal verification. The four-role
workflow remains future work. Therefore, 10/10 should be presented as an initial
integration/evidence-interpretation result, not as hardware-security detection
accuracy.

The next experiments and implementation tasks are:

1. Repeat the current trials and report evidence, verdict, format, and runtime
   variation separately; keep prompts and model configuration versioned.
2. Add bounded, read-only source access through `GUIDE_ROOT`, enabling analysis
   of RTL rather than only execution of supplied paths.
3. Introduce held-out designs and reviewed evaluation testbenches, with ground
   truth and evaluation tests separated from agent-visible material.
4. Establish a scored single-agent analysis baseline before adding a Critic with
   a separate history and a controlled blind-review protocol.
5. Add isolated repair and stronger verification tools as required by the research
   tasks. Consider another GPU when measured concurrency or throughput warrants it.

## 8. Evidence and reproducibility references

The implementation is recorded in commit `e5af86c`, including the ten-case suite
and validation documentation. The trial itself ran from a dirty guest checkout
whose recorded HEAD was `a22a0ff`; it should not be described as a clean execution
of the later commit. Per-source SHA-256 hashes and runtime settings are retained.
Future experiments should run from a synchronized, clean, pinned revision.

- [Deployment and context validation](r9700-deployment.md)
- [Suite protocol and scoring](security-suite.md)
- [Construction and per-case validation record](security-suite-validation-20260914.md)
- [Full Qwen trial](evidence/phase1/security-v1-agent-20260914/report.json)
- [Hermes acceptance response](evidence/phase1/hermes-64k-acceptance-final.log)
- [Qwen trial step log](evidence/phase1/security-v1-agent-20260914/steps.md)
- [Deterministic EDA trial](evidence/phase1/security-v1-tools-20260914/report.json)
- [Original authorization baseline](authorization-baseline.md)

Sanitized copies of the four referenced records are committed under
`docs/evidence/phase1/`; raw results remain local and on the VM. Each referenced
EDA run also has execution logs, provenance, and, for simulations, waveforms.
Those larger generated artifacts can accompany the report when a reviewer needs
to audit an individual finding in more detail.
