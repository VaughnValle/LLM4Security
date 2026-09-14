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
were rewritten. Text-only serving uses one GPU, 8,192 context tokens, one active
sequence, eager execution, and 85% VRAM utilization.

Hermes is installed at `/home/researcher/.hermes/hermes-agent`, pinned to
`01bae2f9295d7e9797a7c93b8c9b0ac7c8a47f9e`. Its config points to the local
OpenAI-compatible endpoint and `guide-eda-mcp`. Credentials are in private,
untracked `.env` files; they are not included in this record.

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

See [Phase 1](phase1.md) for the source selection, MCP interface, container limits,
and acceptance commands. Keep model-cache and result retention bounded: the
Proxmox disk uses a shared thin pool.
