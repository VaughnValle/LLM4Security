# syntax=docker/dockerfile:1
FROM vllm/vllm-openai-rocm:v0.28.0@sha256:e0a3b2bd3fe7ec563916c3a5d949898d133458c18d6b2f460c906885cfb32032

# Native Quark INT4 support required by AMD's checkpoint. Release vLLM lacks
# this scheme. Pin the reviewed release-era upstream PR #52642 (folded into
# still-open #48606); fail the build if the source or patch context changes.
ADD --checksum=sha256:9736866be1fb9453e5fa313737bff509edcacb0147556c9f48d06bc8aa2abdf6 \
    https://github.com/vllm-project/vllm/compare/d1e3eee6fb8ed3623241ef5c8e3ac533f775bff9...82227dfe41552044601a9d970bbbc9306cbb58dc.diff /tmp/quark.patch
RUN cd /usr/local/lib/python3.12/dist-packages \
    && git apply --check --include='vllm/*' /tmp/quark.patch \
    && git apply --include='vllm/*' /tmp/quark.patch \
    && python3 -m compileall -q vllm/model_executor/layers/quantization/quark \
    && rm /tmp/quark.patch
LABEL org.llm4security.quark-source="82227dfe41552044601a9d970bbbc9306cbb58dc"
