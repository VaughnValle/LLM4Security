# R9700 deployment record

Provisioned on 2026-09-14. Host: Proxmox `10.0.89.35`, Ryzen 3950X,
96 GB RAM. Guest: VM 200 (`llm4security-r9700`), `researcher@10.0.89.200`.

## Guest configuration

- Q35, OVMF, Secure Boot keys disabled; 16 host-model vCPUs.
- 64 GB fixed RAM; 300 GB thin-provisioned disk on `local-lvm`.
- `vmbr0`, static `10.0.89.200/24`, gateway/DNS `10.0.89.1`.
- Both R9700 functions passed through with `hostpci0: 0000:0c:00,pcie=1`.
- Ubuntu 24.04.5, kernel `6.17.0-42-generic`, inbox `amdgpu` driver.
- Kernel selected in `/etc/default/grub.d/99-llm4security-kernel.cfg`.
  A newer HWE kernel is installed too; changing the selected kernel requires
  rerunning GPU and inference acceptance.
- QEMU guest agent, Docker Engine, Compose, uv, Icarus, and AMD ROCm tools installed.
  `researcher` belongs to `docker`, `video`, and `render`.

ROCm identifies `AMD Radeon AI PRO R9700`, `gfx1201`. Container PyTorch reports
34,208,743,424 bytes of VRAM and HIP `7.2.53211`. The GPU's upstream CPU link is
PCIe 4.0 x8; the downstream card link reports x16. Software configuration does
not change that upstream lane allocation.

This records an observed deployment, not a claim that Ubuntu 24.04.5 is listed
in AMD's supported OS matrix. No driver was installed on the Proxmox host.

## Runtime provenance

The pinned image build is `containers/inference/Dockerfile`: vLLM
`0.28.0+rocm723` plus native Quark INT4 support from upstream source revision
`82227dfe41552044601a9d970bbbc9306cbb58dc`. The base image digest and patch checksum
are enforced by the build. This is an unreleased upstream backport; retain the
recipe and rerun acceptance when replacing it.

Checkpoint: `amd/Qwen3.8-27B-Quark-AWQ-INT4-W4A16`, revision
`0f7ee2559e8dbc25879e1fe1677b2b10708b91a9`. No checkpoint configuration or weights
were rewritten. Text-only serving uses one GPU, 65,536 context tokens, one active
sequence, eager execution, and 85% VRAM utilization.

Hermes is installed at `/home/researcher/.hermes/hermes-agent`, pinned to
`01bae2f9295d7e9797a7c93b8c9b0ac7c8a47f9e`. Its config points to the local
OpenAI-compatible endpoint and `guide-eda-mcp`. Its actual context matches vLLM.
The custom-provider credential is stored as private `model.api_key` in the
mode-600 Hermes config, sourced from the guest's private `.env`. Environment-only
authentication did not work for this custom-provider path. Credentials are not
included in this record.

GUIDE remains at `/home/researcher/GUIDE`, revision
`a3f8643498fe062be1e1e5e6fa5e62bd03470e98`. VerilogEval is an external GUIDE
submodule at `c498220d0a52248f8e3fdffe279075215bde2da6`.
The local `.llm4security-smoke` wrapper is deliberately separate from its
upstream benchmark sources.

## Operating commands

```bash
ssh researcher@10.0.89.200
cd ~/LLM4Security
make inference-up
make inference-smoke
docker compose --env-file .env -f deploy/inference/compose.yaml logs -f inference
```

For workstation clients, keep the service bound to guest loopback:

```bash
ssh -N -L 8000:127.0.0.1:8000 researcher@10.0.89.200
```

Client URL: `http://127.0.0.1:8000/v1`; model alias: `Qwen3.8-27B`.
Use the private `OPENAI_API_KEY` already configured inside the guest.

Configure and use Hermes with its bounded research toolset:

```bash
uv run --env-file .env python scripts/configure_hermes.py
~/.local/bin/hermes mcp test guide-eda-mcp
~/.local/bin/hermes chat
```

The configuration helper validates the actual advertised context, backs up the
existing config, sets non-streaming requests, and selects only `guide-eda-mcp`
for CLI use. Exit older Hermes sessions before starting a new one. No fake
context override or `--ignore-rules` workaround is needed for this configuration.
Docker restarts inference after a guest reboot unless the service was deliberately
stopped. VM auto-start on a Proxmox host reboot is a separate host setting.

## Context acceptance on 2026-09-14

The same single card, checkpoint, image, 85% VRAM budget, and one active sequence
were used for all three stages. Each probe checks short generation, a long prompt
producing an automatic tool call, then consumption of its returned tool result.

| Serving limit | Measured tool-call prompt | Whole probe elapsed | Result |
| --- | ---: | ---: | --- |
| 16,384 | 14,292 tokens | 33.35 seconds | Passed |
| 32,768 | 30,292 tokens | 64.03 seconds | Passed |
| 65,536 | 64,292 tokens | 148.20 seconds | Passed |

Raw records and startup logs are in `results/context-validation/` on the guest.
These elapsed times include three requests and may include kernel compilation;
they are not steady-state tokens/second measurements. Padding tests establish
capacity and protocol behavior, not long-document reasoning or retrieval quality.

The earlier 8K startup log reserved 9.02 GiB of KV cache and reported approximately
90,593 cache tokens. Its roughly 29 GB total VRAM allocation was a reserved pool,
not the memory consumed by one 8K request. Extrapolating that allocation to conclude
64K required more GPUs was incorrect. A second GPU is unnecessary for the validated
single-request 64K configuration; concurrency and throughput need separate measurements.

## Final guest acceptance on 2026-09-14

The guest test suite passed all 44 tests, including Docker execution. Local checks
passed 43 tests with the Docker test skipped, plus Ruff and whitespace checks.
The fresh Hermes session `20260914_203319_f11a4f`, using the real 65,536-token
endpoint, compiled both NOT-gate sources and simulated successfully:

- Compile: `0d9f479e90874e34a00775e104b3d31f` (return code 0).
- Simulation: `641dc175436840b0903373ebf2827621` (return code 0,
  `GUIDE_NOTGATE_PASS`, waveform saved).
- Transcript: `results/hermes-64k-acceptance-final.log` on the guest.

These results were checked against the saved EDA `result.json` files. Hermes'
prose misstated the simulation time; use raw simulator output for timing claims.

See [Phase 1](phase1.md) for the source selection, MCP interface, container limits,
and acceptance commands. Keep model-cache and result retention bounded: the
Proxmox disk uses a shared thin pool.
