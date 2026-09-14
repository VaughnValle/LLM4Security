FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip yosys z3 boolector git make && rm -rf /var/lib/apt/lists/*
# TODO: install/pin SymbiYosys and additional solver backends.
WORKDIR /workspace
