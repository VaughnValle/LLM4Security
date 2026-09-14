# Phase 1: one R9700 and the first EDA loop

This implementation provides an inference launcher, endpoint acceptance probe, two
MCP tools, and a bounded single-agent feedback loop. It does **not** implement the
broker or multi-agent experiments. Local tests cover real Icarus execution and MCP
stdio. R9700 inference, Hermes itself, and Docker execution require deployment
validation; unit tests are not evidence of GPU compatibility or security findings.

## Proxmox deployment target

The supplied machine is `https://10.0.89.35:8006`, Ryzen 3950X, 96 GB system RAM,
with one 32 GB Radeon AI PRO R9700. Port 8006 is Proxmox management, not inference.
Use a dedicated Ubuntu 24.04 Linux VM with the GPU passed through. The GPU guest's
planned IP is `10.0.89.200`; the VM has not been created yet and its SSH login
must be established during provisioning; this repository does not change
Proxmox configuration or install drivers on the hypervisor.

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

The example vLLM 0.23.0 ROCm image is pinned by its registry manifest digest. The
registry artifact and parser names were checked during implementation; **the
image/checkpoint/kernel combination has not been validated on this R9700**. If it
fails with unsupported gfx1201, Quark kernels, or model architecture, select/build
a compatible ROCm vLLM image and set `VLLM_IMAGE` to its digest. Record that change
with test results; do not silently switch models or use a CUDA image.

```bash
# Validate resolved configuration without printing its API key.
docker compose --env-file .env -f deploy/inference/compose.yaml config --quiet
# Pull image and check GPU/runtime before downloading model weights.
docker compose --env-file .env -f deploy/inference/compose.yaml run --rm inference --preflight-only
make inference-up
docker compose --env-file .env -f deploy/inference/compose.yaml logs -f inference
make inference-smoke
```

The launcher checks for one visible GPU, gfx1201 and ~32 GB VRAM. Defaults are TP=1,
8,192 context tokens, one active sequence, eager execution, and 85% GPU memory use.
Quantization is read from the checkpoint metadata. The inference container has a
48 GB host-memory cap, 12 CPU quota, and 8 GB shared memory. No claim is made that
64K context or two simultaneous generations fits until measured.

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

After the 8K check passes, increase `VLLM_MAX_MODEL_LEN` in stages (16K, 32K, 64K),
recreate inference, and run a padded probe, for example:

```bash
uv run --env-file .env llm4security-inference-smoke \
  --padding-repeats 30000 --output results/inference-32k.json
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
Python `mcp` SDK. Merge `deploy/hermes/config.example.yaml` into Hermes' config,
substitute absolute paths, and set the same `OPENAI_API_KEY` in the Hermes process
(or its `.env`). The MCP process and Docker daemon must share the local filesystem;
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
production has no host-shell fallback. GPU launch, short/long-context acceptance,
and an actual Hermes session remain required before reporting Phase 1 deployment
as validated. Neither broker delegation nor the four-agent reference experiment
is wired by this change.
