"""Single-GPU vLLM entrypoint; also usable inside a ROCm vLLM image."""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def command(env=None):
    env = os.environ if env is None else env
    model = env.get("VLLM_MODEL", "amd/Qwen3.8-27B-Quark-AWQ-INT4-W4A16")
    revision = env.get("VLLM_MODEL_REVISION", "")
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Set VLLM_MODEL_REVISION to the checkpoint commit SHA")
    context = int(env.get("VLLM_MAX_MODEL_LEN", "8192"))
    sequences = int(env.get("VLLM_MAX_NUM_SEQS", "1"))
    utilization = float(env.get("VLLM_GPU_MEMORY_UTILIZATION", "0.85"))
    if not 512 <= context <= 65536 or sequences not in (1, 2):
        raise ValueError("Phase 1 requires 512..65536 context tokens and 1..2 sequences")
    if not 0.1 <= utilization <= 0.95:
        raise ValueError("GPU memory utilization must be between 0.1 and 0.95")
    if not env.get("VLLM_API_KEY"):
        raise ValueError("Set VLLM_API_KEY (same value as the client OPENAI_API_KEY)")
    # vLLM reads VLLM_API_KEY directly; never put credentials in argv or dry-run output.
    return [
        "vllm",
        "serve",
        model,
        "--revision",
        revision,
        "--served-model-name",
        env.get("LLM_MODEL", "Qwen3.8-27B"),
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--tensor-parallel-size",
        "1",
        "--language-model-only",
        "--dtype",
        "auto",
        "--max-model-len",
        str(context),
        "--max-num-seqs",
        str(sequences),
        "--gpu-memory-utilization",
        str(utilization),
        "--enable-auto-tool-choice",
        "--tool-call-parser",
        env.get("VLLM_TOOL_PARSER", "qwen3_xml"),
        "--reasoning-parser",
        env.get("VLLM_REASONING_PARSER", "qwen3"),
        "--enforce-eager",
    ]


def preflight():
    if not Path("/dev/kfd").exists():
        raise RuntimeError("/dev/kfd missing: run in the Linux GPU guest with ROCm devices mapped")
    import torch

    if not torch.version.hip or not torch.cuda.is_available():
        raise RuntimeError("A working ROCm PyTorch runtime is required")
    if torch.cuda.device_count() != 1:
        raise RuntimeError("Expose exactly one GPU using HIP_VISIBLE_DEVICES")
    props = torch.cuda.get_device_properties(0)
    if "gfx1201" not in props.gcnArchName or props.total_memory < 30 * 1024**3:
        raise RuntimeError(f"Expected a 32GB gfx1201 R9700, got {props}")
    subprocess.run(["vllm", "--version"], check=True)
    print(
        json.dumps(
            {
                "gpu": props.name,
                "arch": props.gcnArchName,
                "vram_bytes": props.total_memory,
                "rocm": torch.version.hip,
            }
        ),
        flush=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    try:
        argv = command()
        if args.dry_run:
            print(json.dumps(argv, indent=2))
            return
        preflight()
        if not args.preflight_only:
            os.execvp(argv[0], argv)
    except (ValueError, RuntimeError, OSError) as exc:
        sys.exit(str(exc))


if __name__ == "__main__":
    main()
