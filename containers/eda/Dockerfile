FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends iverilog=12.0-2build1 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
