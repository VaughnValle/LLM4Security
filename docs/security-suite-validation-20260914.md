# Security suite validation — 2026-09-14

Environment: existing R9700 guest, external GUIDE_ROOT, Icarus 12.0 inside the
production EDA Docker sandbox. Original two-case baseline results were preserved.

## Construction and checking sequence

1. Defined five small interfaces with explicit normal behavior and security requirements.
2. Wrote one testbench per requirement, used identically for the safe and faulty designs.
3. Ran actual compilation/simulation for all ten fixtures in local pytest.
4. Tested five additional always-zero mutants to ensure every testbench rejects
   disabling normal functionality. All five were rejected.
5. Checked evaluator failure handling and fixture preservation with automated tests.
6. Executed `python -m runner.security_suite --output results/security-v1-tools-20260914`
   through MCP on the guest, with its private `.env` loaded by uv.
7. Inspected per-case results and copied the complete report, step log, and all
   twenty compile/simulation artifact directories to local `results/`.
8. Ran the final regression checks: local 66 passed / one Docker test skipped;
   guest 67 passed including Docker; Ruff passed.

## Actual per-case checks

Every case compiled successfully (exit 0). Each simulation below has its own
`output.log`, `result.json`, and waveform under `results/eda/<simulation run>`.
Full compile run IDs, arguments, source hashes, and every executed CHECK line
are in `results/security-v1-tools-20260914/report.json` and `steps.md`.

| Case | Checks logged before termination | Simulator result | Simulation run |
| --- | ---: | --- | --- |
| 01 authorization | 8 | Pass, exit 0 | `361439788f3345018e2e73e92875a102` |
| 02 authorization | 6 | Unauthorized bypass, exit 1 | `180350cdadb549d0bbc5f0edf11a4eb1` |
| 03 register lock | 8 | Pass, exit 0 | `f6f84b261ac944349bbfed1df0e69e34` |
| 04 register lock | 6 | Locked alternate-port write, exit 1 | `a9e091e0f9c54594b2d4737b7413b798` |
| 05 debug access | 1,024 | Pass, exit 0 | `12e352ccf907486e81470289786cbbc6` |
| 06 debug access | 7 | Unauthorized debug output, exit 1 | `1d9ad867953e4b13bd7a7ae39f279304` |
| 07 reset clearing | 510 | Pass, exit 0 | `1a6d15339653499e8ae8fc3106facd6c` |
| 08 reset clearing | 2 | Concurrent load defeats reset, exit 1 | `ca07161ce15e4b7d88588cae75c40f62` |
| 09 output isolation | 512 | Pass, exit 0 | `3c79186c77f64225bb57d91ffaa36972` |
| 10 output isolation | 3 | Disabled output leaks bit 0, exit 1 | `af33b16af5c54edaa48ec998799f586c` |

The count is the number of logged CHECK lines, not the number of all assertions:
the sequential testbenches also assert successful initialization/load/hold.
Failing cases stop at their first security violation. All ten matched expected
outcomes with no timeout or functional/compiler failure. This is deterministic
fixture/tool validation, not a 10/10 score for an agent.

See [suite protocol](security-suite.md) for scoring and the limits of these tests.

## Qwen tool-use trial

Executed one fresh-history trial per case using:

```bash
uv run --extra eda --env-file .env python -m runner.security_suite \
  --agent --output results/security-v1-agent-20260914
```

All ten cases passed linked tool evidence, correct verdict, and strict JSON format
checks (10/10 in each dimension). Each case made exactly one compile and one
simulation call. Summed case time was 507.01 seconds (about 8 minutes 27 seconds).
The full reports, per-case step logs, and referenced EDA artifacts were copied
from the guest into local `results/` for inspection.

This trial used the direct Qwen OpenAI-to-MCP evaluation runner, not the Hermes CLI.
It measures evidence interpretation for these supplied testbenches, not independent
security analysis. It is one trial on ten synthetic cases; it does not supersede
the earlier two-case baseline's recorded format failure or establish benchmark
accuracy. The prompt and scoring protocol are recorded with the trial.
