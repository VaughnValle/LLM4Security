# GUIDE Integration

Set `GUIDE_ROOT=/path/to/GUIDE`. LLM4Security does not vendor GUIDE, avoiding a circular dependency if GUIDE later includes this repository as a submodule.

Selected RTL/header paths are resolved beneath this root and copied into read-only
input snapshots. Artifacts must live outside GUIDE. Explicit invalid roots fail
without fallback. See [Phase 1](../../docs/phase1.md) for the MCP contracts.
