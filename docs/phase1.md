# Phase 1: one R9700 and the first EDA loop

This implementation provides an inference launcher, endpoint acceptance probe, two
MCP tools, and a bounded single-agent feedback loop. It does **not** implement the
broker or multi-agent experiments. Local tests cover real Icarus execution and MCP
stdio. R9700 inference, Docker execution, and an actual Hermes compile/simulate
session have passed on the deployed guest. See [deployment evidence](r9700-deployment.md).
Unit tests alone are not evidence of GPU compatibility or security findings.

## Proxmox deployment target

The supplied machine is `https://10.0.89.35:8006`, Ryzen 3950X, 96 GB system RAM,
with one 32 GB Radeon AI PRO R9700. Port 8006 is Proxmox management, not inference.
Use a dedicated Ubuntu 24.04 Linux VM with the GPU passed through. The deployed
guest is VM 200 at `10.0.89.200`, with SSH user `researcher`. It uses Q35/OVMF,
16 host-model vCPUs, 64 GB fixed RAM, and a 300 GB thin disk. Both functions of
host device `0000:0c:00` are passed through. The hypervisor retains VFIO ownership;
ROCm and Hermes run inside the guest.

Suggested initial allocation: 16 vCPUs, 64 GB fixed guest RAM, and at least 200 GB
free storage for the image, checkpoint/cache, and small experiments. Leave the rest
for Proxmox and existing services; adjust for their actual consumption. These are
starting allocations, not measured requirements. Follow the host's applicable
Proxmox PCI passthrough procedure (IOMMU group, VFIO binding, VM PCI device), then
install a supported Radeon ROCm driver/runtime inside the guest. Confirm inside
the guest before model launch:

```bash
lspci -nn | rg -i 'amd|radeon'
ls -l /dev/kfd /dev/dri/render*
rocminfo
getent group video render
```

Expected architecture: `gfx1201`. Installing a ROCm container alone does not create
a working GPU driver or configure passthrough. AMD's [ROCm vLLM documentation](https://rocm.docs.amd.com/en/7.13.0-preview/ai-inference/vllm.html)
includes R9700/gfx1201 runtime guidance. Use its current supported driver matrix
for the guest kernel; do not substitute an Instinct-only image.

## Install and start inference

From the repository checkout **inside the Linux GPU guest**:

```bash
uv sync --frozen --extra dev --extra eda
cp .env.example .env
```

Edit `.env`: set `GUIDE_ROOT`, a non-default `OPENAI_API_KEY`, and numeric `VIDEO_GID`
and `RENDER_GID` from `getent`. `.env` stays ignored by Git. The supplied checkpoint
is AMD's [Qwen3.8-27B Quark AWQ INT4 W4A16](https://huggingface.co/amd/Qwen3.8-27B-Quark-AWQ-INT4-W4A16),
pinned to a repository SHA. The served alias is `Qwen3.8-27B`; clients use the alias.
The BF16 base checkpoint is not the single-card configuration.

Build `containers/inference/Dockerfile` with `make inference-image`. It pins the
vLLM 0.28.0 ROCm base by digest and applies a checksum-verified upstream native
Quark INT4 backport. The checkpoint requires this scheme; an unmodified 0.23.0
image passed GPU preflight but failed while mapping Quark configuration.
The backport comes from [PR #52642](https://github.com/vllm-project/vllm/pull/52642),
folded into the still-open [PR #48606](https://github.com/vllm-project/vllm/pull/48606).
It uses fixed source commits, checks patch applicability, and makes no checkpoint
changes. Revalidate before replacing this with a newer release.

```bash
# Validate resolved configuration without printing its API key.
docker compose --env-file .env -f deploy/inference/compose.yaml config --quiet
# Build image and check GPU/runtime before downloading model weights.
make inference-image
docker compose --env-file .env -f deploy/inference/compose.yaml run --rm inference --preflight-only
make inference-up
docker compose --env-file .env -f deploy/inference/compose.yaml logs -f inference
make inference-smoke
```

The launcher checks for one visible GPU, gfx1201 and ~32 GB VRAM. It serves the
language model only, avoiding vision-encoder allocation for this text/RTL loop.
Defaults are TP=1,
65,536 context tokens, one active sequence, eager execution, and 85% GPU memory use.
Quantization is read from the checkpoint metadata. The inference container has a
48 GB host-memory cap, 12 CPU quota, and 8 GB shared memory. No claim is made that
two simultaneous 64K generations fit; only one active sequence has been validated.

The service binds guest loopback. For clients on your workstation, tunnel to the
**guest**, then keep `OPENAI_BASE_URL=http://127.0.0.1:8000/v1`:

```bash
ssh -N -L 8000:127.0.0.1:8000 USER@10.0.89.200
```

The probe checks `/v1/models`, normal generation, automatic tool calling with JSON
arguments and a call ID, and consumption of the tool response. It writes full
responses and usage to `results/inference-smoke.json`. A 200 health response alone
is insufficient. Authentication failures, mismatched aliases, malformed calls,
truncated generations, and ignored tool results fail the probe.

The deployed card passed staged 16K, 32K, and 64K checks. For a changed runtime,
repeat that progression with `VLLM_MAX_MODEL_LEN`, recreate inference, and run a
padded probe, for example at the 64K setting:

```bash
uv run --env-file .env llm4security-inference-smoke \
  --padding-repeats 64000 --min-prompt-tokens 64000 --output results/inference-64k.json
```

Repeated words are **not** a tokenizer guarantee. Inspect `usage.prompt_tokens`
and leave output headroom; adjust the count and save latency/VRAM observations.
Keep the last passing configuration. Long-context quality is a separate research
measurement, not established by this acceptance probe.

## GUIDE compile and simulate

GUIDE stays external. Explicit paths and `GUIDE_ROOT` are authoritative; a bad
setting fails instead of silently selecting a sibling repository. The sibling
`../GUIDE` fallback is used only when neither is configured.

```bash
make eda-image
# Replace these with a small, self-checking testbench and RTL already in your GUIDE checkout.
uv run --extra eda --env-file .env llm4security-eda-loop \
  path/to/design.sv path/to/tb.sv --top tb --output results/first-loop.json
```

The deployment smoke case uses GUIDE's pinned VerilogEval reference and a wrapper
from this repository; it does not vendor benchmark source:

```bash
export GUIDE_ROOT=/home/researcher/GUIDE # Or your own external checkout.
git -C "$GUIDE_ROOT" submodule update --init --depth 1 benchmark/VerilogEval
mkdir -p "$GUIDE_ROOT/.llm4security-smoke"
cp examples/eda/notgate_acceptance.sv "$GUIDE_ROOT/.llm4security-smoke/"
uv run --extra eda --env-file .env llm4security-eda-loop \
  benchmark/VerilogEval/dataset_spec-to-rtl/Prob005_notgate_ref.sv \
  .llm4security-smoke/notgate_acceptance.sv --top tb \
  --output results/first-loop.json
```

The wrapper checks both NOT-gate inputs with `$fatal` on mismatch and emits
`GUIDE_NOTGATE_PASS`. This validates reference execution and tool plumbing, not
generated RTL quality or a security property.

`compile_rtl(sources, top=None, timeout_seconds=60)` accepts 1–128 GUIDE-relative
Verilog/SystemVerilog files, totaling at most 16 MiB. List included `.vh`/`.svh`
headers explicitly; their parent directories become include search paths. Absolute
paths, traversal and symlinks escaping GUIDE are rejected. The selected files are
copied into an isolated snapshot, preserving relative layout. Sources and GUIDE
are never mounted writable into the tool container.

`simulate(run_id, timeout_seconds=30)` accepts only a successful compile run ID,
verifies the saved binary hash, and executes that binary in a fresh container.
Testbenches must call `$fatal` for failed checks. To retain a waveform use
`$dumpfile("waveform.vcd")`. Exit 0 means simulation completed; it does not establish
that assertions existed or prove a hardware-security claim. Relative external
memory files, VPI plugins, arbitrary flags, generated RTL editing and other EDA
backends are outside this first interface.

Each call writes a UUID directory under `EDA_ARTIFACT_ROOT`: bounded output log,
JSON result, command, tool version output, Docker image ID, timing/exit status,
source/binary hashes, GUIDE commit if available, and compiled binary or waveform.
Source hashes identify working-copy contents even when GUIDE has uncommitted edits.
Waveforms are optional. The model receives structured results and output; inspect
saved artifacts for detailed evidence. The loop exits nonzero if it ends without
a successful compile followed by its simulation, or exhausts its turn budget.

Tool containers have no network or GPU devices, read-only root/input mounts,
dropped capabilities, no-new-privileges, PID/CPU/memory limits, capped tmpfs, a
64 MiB per-file limit, and a maximum 120-second tool timeout. Only the two named
artifacts are copied out while the container is alive; cleanup runs on all exits.
The MCP process controls Docker on its host. Run it in a dedicated research guest;
containers share that guest's kernel. Accumulated host artifacts need periodic
retention management. Server-wide scheduling/quotas are later work.

## Hermes

The repository package is `guide_mcp`, avoiding a collision with the official
Python `mcp` SDK. Once the server advertises and has passed real 64K acceptance, run:

```bash
uv run --env-file .env python scripts/configure_hermes.py
~/.local/bin/hermes mcp test guide-eda-mcp
~/.local/bin/hermes chat
```

The setup checks the authenticated endpoint's actual context, backs up the existing
config, stores the endpoint credential as private `model.api_key`, and selects the
GUIDE MCP toolset for CLI sessions. This Hermes version deliberately does not use
`OPENAI_API_KEY` for every custom endpoint. Exporting that variable alone did not fix
authentication. `model.context_length` must match vLLM; falsely declaring 64K over
an 8K server caused repeated HTTP 400 and compression failures. Starting new
sessions did not fix that mismatch. Non-streaming requests avoid the runtime's
streaming/tool-parser interoperability issue. The MCP process and Docker daemon must share the local filesystem;
when using a GPU tunnel, EDA may run locally on a separate Linux Docker host.

Hermes uses `provider: custom` for the OpenAI-compatible endpoint. Its name does
not imply that vLLM should use the `hermes` parser: parser selection follows the
checkpoint's tool format (`qwen3_xml` here). See upstream [Hermes configuration](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/configuration.md)
and [MCP setup](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md).
Start `hermes chat`, confirm it discovers both tools, and request compilation and
simulation of the same small GUIDE testbench. Save the tool evidence. The included
CLI tests the same OpenAI/MCP wire contracts but is not the Hermes runtime.

## Validation and remaining deployment gates

```bash
uv sync --frozen --extra dev --extra eda
uv run --no-sync ruff check .
uv run --no-sync pytest -q
make eda-image
RUN_DOCKER_TESTS=1 uv run --no-sync pytest -q
```

CI builds the EDA image and enables the Docker test. Local tests use the real
Icarus compiler with a **test-only trusted-fixture adapter** where Docker is absent;
production has no host-shell fallback. Record GPU and Hermes acceptance separately
from unit tests. Neither broker delegation nor the four-agent reference experiment
is wired by this change. A synthetic single-agent authorization baseline is available
via `uv run --extra eda --env-file .env python -m runner.baseline`; see
[the baseline protocol](authorization-baseline.md).
