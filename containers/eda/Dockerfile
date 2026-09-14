FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip iverilog verilator yosys git make g++ && rm -rf /var/lib/apt/lists/*
# TODO: pin versions, add cocotb environment and Verible/Slang.
WORKDIR /workspace
