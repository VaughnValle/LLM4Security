# security-v1 — agent

Actual execution steps; raw tool results and model responses are in report.json.

## case_01 / trial 1

Access is granted exactly when request and privileged are both asserted, regardless of bypass.

1. Staged and SHA-256 hashed design and testbench.
3. Called `compile_rtl` with `{"sources": [".llm4security-suite/security-v1/case_01/design.sv", ".llm4security-suite/security-v1/case_01/tb.sv"], "top": "tb"}`.
   Run `10417712c96941b68e78708d2a190024`; exit `0`; timeout `False`.
5. Called `simulate` with `{"run_id": "10417712c96941b68e78708d2a190024"}`.
   Run `06ba39015a5a4f719a5b4ee8bc1d64f8`; exit `0`; timeout `False`.

```text
CHECK access request=0 privileged=0 bypass=0 grant=0
CHECK access request=0 privileged=0 bypass=1 grant=0
CHECK access request=0 privileged=1 bypass=0 grant=0
CHECK access request=0 privileged=1 bypass=1 grant=0
CHECK access request=1 privileged=0 bypass=0 grant=0
CHECK access request=1 privileged=0 bypass=1 grant=0
CHECK access request=1 privileged=1 bypass=0 grant=1
CHECK access request=1 privileged=1 bypass=1 grant=1
SECURITY_TEST_PASS
```

Observed: `property_held_for_test`; expected: `property_held_for_test`; evidence passed: `True`; strict result: `True`.

## case_02 / trial 1

Access is granted exactly when request and privileged are both asserted, regardless of bypass.

1. Staged and SHA-256 hashed design and testbench.
3. Called `compile_rtl` with `{"sources": [".llm4security-suite/security-v1/case_02/design.sv", ".llm4security-suite/security-v1/case_02/tb.sv"], "top": "tb"}`.
   Run `ba2eef768bf24650adef6becece99021`; exit `0`; timeout `False`.
5. Called `simulate` with `{"run_id": "ba2eef768bf24650adef6becece99021"}`.
   Run `a4943b0a66584b97b71ac5483c0b8bbb`; exit `1`; timeout `False`.

```text
CHECK access request=0 privileged=0 bypass=0 grant=0
CHECK access request=0 privileged=0 bypass=1 grant=0
CHECK access request=0 privileged=1 bypass=0 grant=0
CHECK access request=0 privileged=1 bypass=1 grant=0
CHECK access request=1 privileged=0 bypass=0 grant=0
CHECK access request=1 privileged=0 bypass=1 grant=1
FATAL: /inputs/sources/.llm4security-suite/security-v1/case_02/tb.sv:12: SECURITY_VIOLATION: authorization
```

Observed: `property_violated`; expected: `property_violated`; evidence passed: `True`; strict result: `True`.

## case_03 / trial 1

Reset clears the register. Either write port may update it while unlocked; neither port may change it while locked.

1. Staged and SHA-256 hashed design and testbench.
3. Called `compile_rtl` with `{"sources": [".llm4security-suite/security-v1/case_03/design.sv", ".llm4security-suite/security-v1/case_03/tb.sv"], "top": "tb"}`.
   Run `4e1b7abfaca743dbacb5893aaa1448ba`; exit `0`; timeout `False`.
5. Called `simulate` with `{"run_id": "4e1b7abfaca743dbacb5893aaa1448ba"}`.
   Run `3dd7f52e3d3c4586a668b13528324364`; exit `0`; timeout `False`.

```text
CHECK lock=0 ports=00 value=3c expected=3c
CHECK lock=0 ports=01 value=a5 expected=a5
CHECK lock=0 ports=10 value=a5 expected=a5
CHECK lock=0 ports=11 value=a5 expected=a5
CHECK lock=1 ports=00 value=3c expected=3c
CHECK lock=1 ports=01 value=3c expected=3c
CHECK lock=1 ports=10 value=3c expected=3c
CHECK lock=1 ports=11 value=3c expected=3c
SECURITY_TEST_PASS
```

Observed: `property_held_for_test`; expected: `property_held_for_test`; evidence passed: `True`; strict result: `True`.

## case_04 / trial 1

Reset clears the register. Either write port may update it while unlocked; neither port may change it while locked.

1. Staged and SHA-256 hashed design and testbench.
3. Called `compile_rtl` with `{"sources": [".llm4security-suite/security-v1/case_04/design.sv", ".llm4security-suite/security-v1/case_04/tb.sv"], "top": "tb"}`.
   Run `4e7b99b4c13541d199022aa39ea4166d`; exit `0`; timeout `False`.
5. Called `simulate` with `{"run_id": "4e7b99b4c13541d199022aa39ea4166d"}`.
   Run `4362c3f7ee90449e9f367511c4e4aa69`; exit `1`; timeout `False`.

```text
CHECK lock=0 ports=00 value=3c expected=3c
CHECK lock=0 ports=01 value=a5 expected=a5
CHECK lock=0 ports=10 value=a5 expected=a5
CHECK lock=0 ports=11 value=a5 expected=a5
CHECK lock=1 ports=00 value=3c expected=3c
CHECK lock=1 ports=01 value=a5 expected=3c
FATAL: /inputs/sources/.llm4security-suite/security-v1/case_04/tb.sv:20: SECURITY_VIOLATION: locked register modified
```

Observed: `property_violated`; expected: `property_violated`; evidence passed: `True`; strict result: `True`.

## case_05 / trial 1

Debug output equals the protected byte only when debug_read and authorized are asserted; otherwise output is zero.

1. Staged and SHA-256 hashed design and testbench.
3. Called `compile_rtl` with `{"sources": [".llm4security-suite/security-v1/case_05/design.sv", ".llm4security-suite/security-v1/case_05/tb.sv"], "top": "tb"}`.
   Run `09a9dc5bacf743fa8dc2c41e6f6dacdb`; exit `0`; timeout `False`.
5. Called `simulate` with `{"run_id": "09a9dc5bacf743fa8dc2c41e6f6dacdb"}`.
   Run `a3f09ccb61854a2da5fe62a5aa1ff19f`; exit `0`; timeout `False`.

```text
CHECK secret=00 read=0 authorized=0 data=00
CHECK secret=00 read=0 authorized=1 data=00
CHECK secret=00 read=1 authorized=0 data=00
CHECK secret=00 read=1 authorized=1 data=00
CHECK secret=01 read=0 authorized=0 data=00
CHECK secret=01 read=0 authorized=1 data=00
CHECK secret=01 read=1 authorized=0 data=00
CHECK secret=01 read=1 authorized=1 data=01
CHECK secret=02 read=0 authorized=0 data=00
CHECK secret=02 read=0 authorized=1 data=00
CHECK secret=02 read=1 authorized=0 data=00
CHECK secret=02 read=1 authorized=1 data=02
CHECK secret=03 read=0 authorized=0 data=00
CHECK secret=03 read=0 authorized=1 data=00
CHECK secret=03 read=1 authorized=0 data=00
CHECK secret=03 read=1 authorized=1 data=03
CHECK secret=04 read=0 authorized=0 data=00
CHECK secret=04 read=0 authorized=1 data=00
CHECK secret=04 read=1 authorized=0 data=00
CHECK secret=04 read=1 authorized=1 data=04
CHECK secret=05 read=0 authorized=0 data=00
CHECK secret=05 read=0 authorized=1 data=00
CHECK secret=05 read=1 authorized=0 data=00
CHECK secret=05 read=1 authorized=1 data=05
CHECK secret=06 read=0 authorized=0 data=00
CHECK secret=06 read=0 authorized=1 data=00
CHECK secret=06 read=1 authorized=0 data=00
CHECK secret=06 read=1 authorized=1 data=06
CHECK secret=07 read=0 authorized=0 data=00
CHECK secret=07 read=0 authorized=1 data=00
CHECK secret=07 read=1 authorized=0 data=00
CHECK secret=07 read=1 authorized=1 data=07
CHECK secret=08 read=0 authorized=0 data=00
CHECK secret=08 read=0 authorized=1 data=00
CHECK secret=08 read=1 authorized=0 data=00
CHECK secret=08 read=1 authorized=1 data=08
CHECK secret=09 read=0 authorized=0 data=00
CHECK secret=09 read=0 authorized=1 data=00
CHECK secret=09 read=1 authorized=0 data=00
CHECK secret=09 read=1 authorized=1 data=09
CHECK secret=0a read=0 authorized=0 data=00
CHECK secret=0a read=0 authorized=1 data=00
CHECK secret=0a read=1 authorized=0 data=00
CHECK secret=0a read=1 authorized=1 data=0a
CHECK secret=0b read=0 authorized=0 data=00
CHECK secret=0b read=0 authorized=1 data=00
CHECK secret=0b read=1 authorized=0 data=00
CHECK secret=0b read=1 authorized=1 data=0b
CHECK secret=0c read=0 authorized=0 data=00
CHECK secret=0c read=0 authorized=1 data=00
CHECK secret=0c read=1 authorized=0 data=00
CHECK secret=0c read=1 authorized=1 data=0c
CHECK secret=0d read=0 authorized=0 data=00
CHECK secret=0d read=0 authorized=1 data=00
CHECK secret=0d read=1 authorized=0 data=00
CHECK secret=0d read=1 authorized=1 data=0d
CHECK secret=0e read=0 authorized=0 data=00
CHECK secret=0e read=0 authorized=1 data=00
CHECK secret=0e read=1 authorized=0 data=00
CHECK secret=0e read=1 authorized=1 data=0e
CHECK secret=0f read=0 authorized=0 data=00
CHECK secret=0f read=0 authorized=1 data=00
CHECK secret=0f read=1 authorized=0 data=00
CHECK secret=0f read=1 authorized=1 data=0f
CHECK secret=10 read=0 authorized=0 data=00
CHECK secret=10 read=0 authorized=1 data=00
CHECK secret=10 read=1 authorized=0 data=00
CHECK secret=10 read=1 authorized=1 data=10
CHECK secret=11 read=0 authorized=0 data=00
CHECK secret=11 read=0 authorized=1 data=00
CHECK secret=11 read=1 authorized=0 data=00
CHECK secret=11 read=1 authorized=1 data=11
CHECK secret=12 read=0 authorized=0 data=00
CHECK secret=12 read=0 authorized=1 data=00
CHECK secret=12 read=1 authorized=0 data=00
CHECK secret=12 read=1 authorized=1 data=12
CHECK secret=13 read=0 authorized=0 data=00
CHECK secret=13 read=0 authorized=1 data=00
CHECK secret=13 read=1 authorized=0 data=00
CHECK secret=13 read=1 authorized=1 data=13
CHECK secret=14 read=0 authorized=0 data=00
CHECK secret=14 read=0 authorized=1 data=00
CHECK secret=14 read=1 authorized=0 data=00
CHECK secret=14 read=1 authorized=1 data=14
CHECK secret=15 read=0 authorized=0 data=00
CHECK secret=15 read=0 authorized=1 data=00
CHECK secret=15 read=1 authorized=0 data=00
CHECK secret=15 read=1 authorized=1 data=15
CHECK secret=16 read=0 authorized=0 data=00
CHECK secret=16 read=0 authorized=1 data=00
CHECK secret=16 read=1 authorized=0 data=00
CHECK secret=16 read=1 authorized=1 data=16
CHECK secret=17 read=0 authorized=0 data=00
CHECK secret=17 read=0 authorized=1 data=00
CHECK secret=17 read=1 authorized=0 data=00
CHECK secret=17 read=1 authorized=1 data=17
CHECK secret=18 read=0 authorized=0 data=00
CHECK secret=18 read=0 authorized=1 data=00
CHECK secret=18 read=1 authorized=0 data=00
CHECK secret=18 read=1 authorized=1 data=18
CHECK secret=19 read=0 authorized=0 data=00
CHECK secret=19 read=0 authorized=1 data=00
CHECK secret=19 read=1 authorized=0 data=00
CHECK secret=19 read=1 authorized=1 data=19
CHECK secret=1a read=0 authorized=0 data=00
CHECK secret=1a read=0 authorized=1 data=00
CHECK secret=1a read=1 authorized=0 data=00
CHECK secret=1a read=1 authorized=1 data=1a
CHECK secret=1b read=0 authorized=0 data=00
CHECK secret=1b read=0 authorized=1 data=00
CHECK secret=1b read=1 authorized=0 data=00
CHECK secret=1b read=1 authorized=1 data=1b
CHECK secret=1c read=0 authorized=0 data=00
CHECK secret=1c read=0 authorized=1 data=00
CHECK secret=1c read=1 authorized=0 data=00
CHECK secret=1c read=1 authorized=1 data=1c
CHECK secret=1d read=0 authorized=0 data=00
CHECK secret=1d read=0 authorized=1 data=00
CHECK secret=1d read=1 authorized=0 data=00
CHECK secret=1d read=1 authorized=1 data=1d
CHECK secret=1e read=0 authorized=0 data=00
CHECK secret=1e read=0 authorized=1 data=00
CHECK secret=1e read=1 authorized=0 data=00
CHECK secret=1e read=1 authorized=1 data=1e
CHECK secret=1f read=0 authorized=0 data=00
CHECK secret=1f read=0 authorized=1 data=00
CHECK secret=1f read=1 authorized=0 data=00
CHECK secret=1f read=1 authorized=1 data=1f
CHECK secret=20 read=0 authorized=0 data=00
CHECK secret=20 read=0 authorized=1 data=00
CHECK secret=20 read=1 authorized=0 data=00
CHECK secret=20 read=1 authorized=1 data=20
CHECK secret=21 read=0 authorized=0 data=00
CHECK secret=21 read=0 authorized=1 data=00
CHECK secret=21 read=1 authorized=0 data=00
CHECK secret=21 read=1 authorized=1 data=21
CHECK secret=22 read=0 authorized=0 data=00
CHECK secret=22 read=0 authorized=1 data=00
CHECK secret=22 read=1 authorized=0 data=00
CHECK secret=22 read=1 authorized=1 data=22
CHECK secret=23 read=0 authorized=0 data=00
CHECK secret=23 read=0 authorized=1 data=00
CHECK secret=23 read=1 authorized=0 data=00
CHECK secret=23 read=1 authorized=1 data=23
CHECK secret=24 read=0 authorized=0 data=00
CHECK secret=24 read=0 authorized=1 data=00
CHECK secret=24 read=1 authorized=0 data=00
CHECK secret=24 read=1 authorized=1 data=24
CHECK secret=25 read=0 authorized=0 data=00
CHECK secret=25 read=0 authorized=1 data=00
CHECK secret=25 read=1 authorized=0 data=00
CHECK secret=25 read=1 authorized=1 data=25
CHECK secret=26 read=0 authorized=0 data=00
CHECK secret=26 read=0 authorized=1 data=00
CHECK secret=26 read=1 authorized=0 data=00
CHECK secret=26 read=1 authorized=1 data=26
CHECK secret=27 read=0 authorized=0 data=00
CHECK secret=27 read=0 authorized=1 data=00
CHECK secret=27 read=1 authorized=0 data=00
CHECK secret=27 read=1 authorized=1 data=27
CHECK secret=28 read=0 authorized=0 data=00
CHECK secret=28 read=0 authorized=1 data=00
CHECK secret=28 read=1 authorized=0 data=00
CHECK secret=28 read=1 authorized=1 data=28
CHECK secret=29 read=0 authorized=0 data=00
CHECK secret=29 read=0 authorized=1 data=00
CHECK secret=29 read=1 authorized=0 data=00
CHECK secret=29 read=1 authorized=1 data=29
CHECK secret=2a read=0 authorized=0 data=00
CHECK secret=2a read=0 authorized=1 data=00
CHECK secret=2a read=1 authorized=0 data=00
CHECK secret=2a read=1 authorized=1 data=2a
CHECK secret=2b read=0 authorized=0 data=00
CHECK secret=2b read=0 authorized=1 data=00
CHECK secret=2b read=1 authorized=0 data=00
CHECK secret=2b read=1 authorized=1 data=2b
CHECK secret=2c read=0 authorized=0 data=00
CHECK secret=2c read=0 authorized=1 data=00
CHECK secret=2c read=1 authorized=0 data=00
CHECK secret=2c read=1 authorized=1 data=2c
CHECK secret=2d read=0 authorized=0 data=00
CHECK secret=2d read=0 authorized=1 data=00
CHECK secret=2d read=1 authorized=0 data=00
CHECK secret=2d read=1 authorized=1 data=2d
CHECK secret=2e read=0 authorized=0 data=00
CHECK secret=2e read=0 authorized=1 data=00
CHECK secret=2e read=1 authorized=0 data=00
CHECK secret=2e read=1 authorized=1 data=2e
CHECK secret=2f read=0 authorized=0 data=00
CHECK secret=2f read=0 authorized=1 data=00
CHECK secret=2f read=1 authorized=0 data=00
CHECK secret=2f read=1 authorized=1 data=2f
CHECK secret=30 read=0 authorized=0 data=00
CHECK secret=30 read=0 authorized=1 data=00
CHECK secret=30 read=1 authorized=0 data=00
CHECK secret=30 read=1 authorized=1 data=30
CHECK secret=31 read=0 authorized=0 data=00
CHECK secret=31 read=0 authorized=1 data=00
CHECK secret=31 read=1 authorized=0 data=00
CHECK secret=31 read=1 authorized=1 data=31
CHECK secret=32 read=0 authorized=0 data=00
CHECK secret=32 read=0 authorized=1 data=00
CHECK secret=32 read=1 authorized=0 data=00
CHECK secret=32 read=1 authorized=1 data=32
CHECK secret=33 read=0 authorized=0 data=00
CHECK secret=33 read=0 authorized=1 data=00
CHECK secret=33 read=1 authorized=0 data=00
CHECK secret=33 read=1 authorized=1 data=33
CHECK secret=34 read=0 authorized=0 data=00
CHECK secret=34 read=0 authorized=1 data=00
CHECK secret=34 read=1 authorized=0 data=00
CHECK secret=34 read=1 authorized=1 data=34
CHECK secret=35 read=0 authorized=0 data=00
CHECK secret=35 read=0 authorized=1 data=00
CHECK secret=35 read=1 authorized=0 data=00
CHECK secret=35 read=1 authorized=1 data=35
CHECK secret=36 read=0 authorized=0 data=00
CHECK secret=36 read=0 authorized=1 data=00
CHECK secret=36 read=1 authorized=0 data=00
CHECK secret=36 read=1 authorized=1 data=36
CHECK secret=37 read=0 authorized=0 data=00
CHECK secret=37 read=0 authorized=1 data=00
CHECK secret=37 read=1 authorized=0 data=00
CHECK secret=37 read=1 authorized=1 data=37
CHECK secret=38 read=0 authorized=0 data=00
CHECK secret=38 read=0 authorized=1 data=00
CHECK secret=38 read=1 authorized=0 data=00
CHECK secret=38 read=1 authorized=1 data=38
CHECK secret=39 read=0 authorized=0 data=00
CHECK secret=39 read=0 authorized=1 data=00
CHECK secret=39 read=1 authorized=0 data=00
CHECK secret=39 read=1 authorized=1 data=39
CHECK secret=3a read=0 authorized=0 data=00
CHECK secret=3a read=0 authorized=1 data=00
CHECK secret=3a read=1 authorized=0 data=00
CHECK secret=3a read=1 authorized=1 data=3a
CHECK secret=3b read=0 authorized=0 data=00
CHECK secret=3b read=0 authorized=1 data=00
CHECK secret=3b read=1 authorized=0 data=00
CHECK secret=3b read=1 authorized=1 data=3b
CHECK secret=3c read=0 authorized=0 data=00
CHECK secret=3c read=0 authorized=1 data=00
CHECK secret=3c read=1 authorized=0 data=00
CHECK secret=3c read=1 authorized=1 data=3c
CHECK secret=3d read=0 authorized=0 data=00
CHECK secret=3d read=0 authorized=1 data=00
CHECK secret=3d read=1 authorized=0 data=00
CHECK secret=3d read=1 authorized=1 data=3d
CHECK secret=3e read=0 authorized=0 data=00
CHECK secret=3e read=0 authorized=1 data=00
CHECK secret=3e read=1 authorized=0 data=00
CHECK secret=3e read=1 authorized=1 data=3e
CHECK secret=3f read=0 authorized=0 data=00
CHECK secret=3f read=0 authorized=1 data=00
CHECK secret=3f read=1 authorized=0 data=00
CHECK secret=3f read=1 authorized=1 data=3f
CHECK secret=40 read=0 authorized=0 data=00
CHECK secret=40 read=0 authorized=1 data=00
CHECK secret=40 read=1 authorized=0 data=00
CHECK secret=40 read=1 authorized=1 data=40
CHECK secret=41 read=0 authorized=0 data=00
CHECK secret=41 read=0 authorized=1 data=00
CHECK secret=41 read=1 authorized=0 data=00
CHECK secret=41 read=1 authorized=1 data=41
CHECK secret=42 read=0 authorized=0 data=00
CHECK secret=42 read=0 authorized=1 data=00
CHECK secret=42 read=1 authorized=0 data=00
CHECK secret=42 read=1 authorized=1 data=42
CHECK secret=43 read=0 authorized=0 data=00
CHECK secret=43 read=0 authorized=1 data=00
CHECK secret=43 read=1 authorized=0 data=00
CHECK secret=43 read=1 authorized=1 data=43
CHECK secret=44 read=0 authorized=0 data=00
CHECK secret=44 read=0 authorized=1 data=00
CHECK secret=44 read=1 authorized=0 data=00
CHECK secret=44 read=1 authorized=1 data=44
CHECK secret=45 read=0 authorized=0 data=00
CHECK secret=45 read=0 authorized=1 data=00
CHECK secret=45 read=1 authorized=0 data=00
CHECK secret=45 read=1 authorized=1 data=45
CHECK secret=46 read=0 authorized=0 data=00
CHECK secret=46 read=0 authorized=1 data=00
CHECK secret=46 read=1 authorized=0 data=00
CHECK secret=46 read=1 authorized=1 data=46
CHECK secret=47 read=0 authorized=0 data=00
CHECK secret=47 read=0 authorized=1 data=00
CHECK secret=47 read=1 authorized=0 data=00
CHECK secret=47 read=1 authorized=1 data=47
CHECK secret=48 read=0 authorized=0 data=00
CHECK secret=48 read=0 authorized=1 data=00
CHECK secret=48 read=1 authorized=0 data=00
CHECK secret=48 read=1 authorized=1 data=48
CHECK secret=49 read=0 authorized=0 data=00
CHECK secret=49 read=0 authorized=1 data=00
CHECK secret=49 read=1 authorized=0 data=00
CHECK secret=49 read=1 authorized=1 data=49
CHECK secret=4a read=0 authorized=0 data=00
CHECK secret=4a read=0 authorized=1 data=00
CHECK secret=4a read=1 authorized=0 data=00
CHECK secret=4a read=1 authorized=1 data=4a
CHECK secret=4b read=0 authorized=0 data=00
CHECK secret=4b read=0 authorized=1 data=00
CHECK secret=4b read=1 authorized=0 data=00
CHECK secret=4b read=1 authorized=1 data=4b
CHECK secret=4c read=0 authorized=0 data=00
CHECK secret=4c read=0 authorized=1 data=00
CHECK secret=4c read=1 authorized=0 data=00
CHECK secret=4c read=1 authorized=1 data=4c
CHECK secret=4d read=0 authorized=0 data=00
CHECK secret=4d read=0 authorized=1 data=00
CHECK secret=4d read=1 authorized=0 data=00
CHECK secret=4d read=1 authorized=1 data=4d
CHECK secret=4e read=0 authorized=0 data=00
CHECK secret=4e read=0 authorized=1 data=00
CHECK secret=4e read=1 authorized=0 data=00
CHECK secret=4e read=1 authorized=1 data=4e
CHECK secret=4f read=0 authorized=0 data=00
CHECK secret=4f read=0 authorized=1 data=00
CHECK secret=4f read=1 authorized=0 data=00
CHECK secret=4f read=1 authorized=1 data=4f
CHECK secret=50 read=0 authorized=0 data=00
CHECK secret=50 read=0 authorized=1 data=00
CHECK secret=50 read=1 authorized=0 data=00
CHECK secret=50 read=1 authorized=1 data=50
CHECK secret=51 read=0 authorized=0 data=00
CHECK secret=51 read=0 authorized=1 data=00
CHECK secret=51 read=1 authorized=0 data=00
CHECK secret=51 read=1 authorized=1 data=51
CHECK secret=52 read=0 authorized=0 data=00
CHECK secret=52 read=0 authorized=1 data=00
CHECK secret=52 read=1 authorized=0 data=00
CHECK secret=52 read=1 authorized=1 data=52
CHECK secret=53 read=0 authorized=0 data=00
CHECK secret=53 read=0 authorized=1 data=00
CHECK secret=53 read=1 authorized=0 data=00
CHECK secret=53 read=1 authorized=1 data=53
CHECK secret=54 read=0 authorized=0 data=00
CHECK secret=54 read=0 authorized=1 data=00
CHECK secret=54 read=1 authorized=0 data=00
CHECK secret=54 read=1 authorized=1 data=54
CHECK secret=55 read=0 authorized=0 data=00
CHECK secret=55 read=0 authorized=1 data=00
CHECK secret=55 read=1 authorized=0 data=00
CHECK secret=55 read=1 authorized=1 data=55
CHECK secret=56 read=0 authorized=0 data=00
CHECK secret=56 read=0 authorized=1 data=00
CHECK secret=56 read=1 authorized=0 data=00
CHECK secret=56 read=1 authorized=1 data=56
CHECK secret=57 read=0 authorized=0 data=00
CHECK secret=57 read=0 authorized=1 data=00
CHECK secret=57 read=1 authorized=0 data=00
CHECK secret=57 read=1 authorized=1 data=57
CHECK secret=58 read=0 authorized=0 data=00
CHECK secret=58 read=0 authorized=1 data=00
CHECK secret=58 read=1 authorized=0 data=00
CHECK secret=58 read=1 authorized=1 data=58
CHECK secret=59 read=0 authorized=0 data=00
CHECK secret=59 read=0 authorized=1 data=00
CHECK secret=59 read=1 authorized=0 data=00
CHECK secret=59 read=1 authorized=1 data=59
CHECK secret=5a read=0 authorized=0 data=00
CHECK secret=5a read=0 authorized=1 data=00
CHECK secret=5a read=1 authorized=0 data=00
CHECK secret=5a read=1 authorized=1 data=5a
CHECK secret=5b read=0 authorized=0 data=00
CHECK secret=5b read=0 authorized=1 data=00
CHECK secret=5b read=1 authorized=0 data=00
CHECK secret=5b read=1 authorized=1 data=5b
CHECK secret=5c read=0 authorized=0 data=00
CHECK secret=5c read=0 authorized=1 data=00
CHECK secret=5c read=1 authorized=0 data=00
CHECK secret=5c read=1 authorized=1 data=5c
CHECK secret=5d read=0 authorized=0 data=00
CHECK secret=5d read=0 authorized=1 data=00
CHECK secret=5d read=1 authorized=0 data=00
CHECK secret=5d read=1 authorized=1 data=5d
CHECK secret=5e read=0 authorized=0 data=00
CHECK secret=5e read=0 authorized=1 data=00
CHECK secret=5e read=1 authorized=0 data=00
CHECK secret=5e read=1 authorized=1 data=5e
CHECK secret=5f read=0 authorized=0 data=00
CHECK secret=5f read=0 authorized=1 data=00
CHECK secret=5f read=1 authorized=0 data=00
CHECK secret=5f read=1 authorized=1 data=5f
CHECK secret=60 read=0 authorized=0 data=00
CHECK secret=60 read=0 authorized=1 data=00
CHECK secret=60 read=1 authorized=0 data=00
CHECK secret=60 read=1 authorized=1 data=60
CHECK secret=61 read=0 authorized=0 data=00
CHECK secret=61 read=0 authorized=1 data=00
CHECK secret=61 read=1 authorized=0 data=00
CHECK secret=61 read=1 authorized=1 data=61
CHECK secret=62 read=0 authorized=0 data=00
CHECK secret=62 read=0 authorized=1 data=00
CHECK secret=62 read=1 authorized=0 data=00
CHECK secret=62 read=1 authorized=1 data=62
CHECK secret=63 read=0 authorized=0 data=00
CHECK secret=63 read=0 authorized=1 data=00
CHECK secret=63 read=1 authorized=0 data=00
CHECK secret=63 read=1 authorized=1 data=63
CHECK secret=64 read=0 authorized=0 data=00
CHECK secret=64 read=0 authorized=1 data=00
CHECK secret=64 read=1 authorized=0 data=00
CHECK secret=64 read=1 authorized=1 data=64
CHECK secret=65 read=0 authorized=0 data=00
CHECK secret=65 read=0 authorized=1 data=00
CHECK secret=65 read=1 authorized=0 data=00
CHECK secret=65 read=1 authorized=1 data=65
CHECK secret=66 read=0 authorized=0 data=00
CHECK secret=66 read=0 authorized=1 data=00
CHECK secret=66 read=1 authorized=0 data=00
CHECK secret=66 read=1 authorized=1 data=66
CHECK secret=67 read=0 authorized=0 data=00
CHECK secret=67 read=0 authorized=1 data=00
CHECK secret=67 read=1 authorized=0 data=00
CHECK secret=67 read=1 authorized=1 data=67
CHECK secret=68 read=0 authorized=0 data=00
CHECK secret=68 read=0 authorized=1 data=00
CHECK secret=68 read=1 authorized=0 data=00
CHECK secret=68 read=1 authorized=1 data=68
CHECK secret=69 read=0 authorized=0 data=00
CHECK secret=69 read=0 authorized=1 data=00
CHECK secret=69 read=1 authorized=0 data=00
CHECK secret=69 read=1 authorized=1 data=69
CHECK secret=6a read=0 authorized=0 data=00
CHECK secret=6a read=0 authorized=1 data=00
CHECK secret=6a read=1 authorized=0 data=00
CHECK secret=6a read=1 authorized=1 data=6a
CHECK secret=6b read=0 authorized=0 data=00
CHECK secret=6b read=0 authorized=1 data=00
CHECK secret=6b read=1 authorized=0 data=00
CHECK secret=6b read=1 authorized=1 data=6b
CHECK secret=6c read=0 authorized=0 data=00
CHECK secret=6c read=0 authorized=1 data=00
CHECK secret=6c read=1 authorized=0 data=00
CHECK secret=6c read=1 authorized=1 data=6c
CHECK secret=6d read=0 authorized=0 data=00
CHECK secret=6d read=0 authorized=1 data=00
CHECK secret=6d read=1 authorized=0 data=00
CHECK secret=6d read=1 authorized=1 data=6d
CHECK secret=6e read=0 authorized=0 data=00
CHECK secret=6e read=0 authorized=1 data=00
CHECK secret=6e read=1 authorized=0 data=00
CHECK secret=6e read=1 authorized=1 data=6e
CHECK secret=6f read=0 authorized=0 data=00
CHECK secret=6f read=0 authorized=1 data=00
CHECK secret=6f read=1 authorized=0 data=00
CHECK secret=6f read=1 authorized=1 data=6f
CHECK secret=70 read=0 authorized=0 data=00
CHECK secret=70 read=0 authorized=1 data=00
CHECK secret=70 read=1 authorized=0 data=00
CHECK secret=70 read=1 authorized=1 data=70
CHECK secret=71 read=0 authorized=0 data=00
CHECK secret=71 read=0 authorized=1 data=00
CHECK secret=71 read=1 authorized=0 data=00
CHECK secret=71 read=1 authorized=1 data=71
CHECK secret=72 read=0 authorized=0 data=00
CHECK secret=72 read=0 authorized=1 data=00
CHECK secret=72 read=1 authorized=0 data=00
CHECK secret=72 read=1 authorized=1 data=72
CHECK secret=73 read=0 authorized=0 data=00
CHECK secret=73 read=0 authorized=1 data=00
CHECK secret=73 read=1 authorized=0 data=00
CHECK secret=73 read=1 authorized=1 data=73
CHECK secret=74 read=0 authorized=0 data=00
CHECK secret=74 read=0 authorized=1 data=00
CHECK secret=74 read=1 authorized=0 data=00
CHECK secret=74 read=1 authorized=1 data=74
CHECK secret=75 read=0 authorized=0 data=00
CHECK secret=75 read=0 authorized=1 data=00
CHECK secret=75 read=1 authorized=0 data=00
CHECK secret=75 read=1 authorized=1 data=75
CHECK secret=76 read=0 authorized=0 data=00
CHECK secret=76 read=0 authorized=1 data=00
CHECK secret=76 read=1 authorized=0 data=00
CHECK secret=76 read=1 authorized=1 data=76
CHECK secret=77 read=0 authorized=0 data=00
CHECK secret=77 read=0 authorized=1 data=00
CHECK secret=77 read=1 authorized=0 data=00
CHECK secret=77 read=1 authorized=1 data=77
CHECK secret=78 read=0 authorized=0 data=00
CHECK secret=78 read=0 authorized=1 data=00
CHECK secret=78 read=1 authorized=0 data=00
CHECK secret=78 read=1 authorized=1 data=78
CHECK secret=79 read=0 authorized=0 data=00
CHECK secret=79 read=0 authorized=1 data=00
CHECK secret=79 read=1 authorized=0 data=00
CHECK secret=79 read=1 authorized=1 data=79
CHECK secret=7a read=0 authorized=0 data=00
CHECK secret=7a read=0 authorized=1 data=00
CHECK secret=7a read=1 authorized=0 data=00
CHECK secret=7a read=1 authorized=1 data=7a
CHECK secret=7b read=0 authorized=0 data=00
CHECK secret=7b read=0 authorized=1 data=00
CHECK secret=7b read=1 authorized=0 data=00
CHECK secret=7b read=1 authorized=1 data=7b
CHECK secret=7c read=0 authorized=0 data=00
CHECK secret=7c read=0 authorized=1 data=00
CHECK secret=7c read=1 authorized=0 data=00
CHECK secret=7c read=1 authorized=1 data=7c
CHECK secret=7d read=0 authorized=0 data=00
CHECK secret=7d read=0 authorized=1 data=00
CHECK secret=7d read=1 authorized=0 data=00
CHECK secret=7d read=1 authorized=1 data=7d
CHECK secret=7e read=0 authorized=0 data=00
CHECK secret=7e read=0 authorized=1 data=00
CHECK secret=7e read=1 authorized=0 data=00
CHECK secret=7e read=1 authorized=1 data=7e
CHECK secret=7f read=0 authorized=0 data=00
CHECK secret=7f read=0 authorized=1 data=00
CHECK secret=7f read=1 authorized=0 data=00
CHECK secret=7f read=1 authorized=1 data=7f
CHECK secret=80 read=0 authorized=0 data=00
CHECK secret=80 read=0 authorized=1 data=00
CHECK secret=80 read=1 authorized=0 data=00
CHECK secret=80 read=1 authorized=1 data=80
CHECK secret=81 read=0 authorized=0 data=00
CHECK secret=81 read=0 authorized=1 data=00
CHECK secret=81 read=1 authorized=0 data=00
CHECK secret=81 read=1 authorized=1 data=81
CHECK secret=82 read=0 authorized=0 data=00
CHECK secret=82 read=0 authorized=1 data=00
CHECK secret=82 read=1 authorized=0 data=00
CHECK secret=82 read=1 authorized=1 data=82
CHECK secret=83 read=0 authorized=0 data=00
CHECK secret=83 read=0 authorized=1 data=00
CHECK secret=83 read=1 authorized=0 data=00
CHECK secret=83 read=1 authorized=1 data=83
CHECK secret=84 read=0 authorized=0 data=00
CHECK secret=84 read=0 authorized=1 data=00
CHECK secret=84 read=1 authorized=0 data=00
CHECK secret=84 read=1 authorized=1 data=84
CHECK secret=85 read=0 authorized=0 data=00
CHECK secret=85 read=0 authorized=1 data=00
CHECK secret=85 read=1 authorized=0 data=00
CHECK secret=85 read=1 authorized=1 data=85
CHECK secret=86 read=0 authorized=0 data=00
CHECK secret=86 read=0 authorized=1 data=00
CHECK secret=86 read=1 authorized=0 data=00
CHECK secret=86 read=1 authorized=1 data=86
CHECK secret=87 read=0 authorized=0 data=00
CHECK secret=87 read=0 authorized=1 data=00
CHECK secret=87 read=1 authorized=0 data=00
CHECK secret=87 read=1 authorized=1 data=87
CHECK secret=88 read=0 authorized=0 data=00
CHECK secret=88 read=0 authorized=1 data=00
CHECK secret=88 read=1 authorized=0 data=00
CHECK secret=88 read=1 authorized=1 data=88
CHECK secret=89 read=0 authorized=0 data=00
CHECK secret=89 read=0 authorized=1 data=00
CHECK secret=89 read=1 authorized=0 data=00
CHECK secret=89 read=1 authorized=1 data=89
CHECK secret=8a read=0 authorized=0 data=00
CHECK secret=8a read=0 authorized=1 data=00
CHECK secret=8a read=1 authorized=0 data=00
CHECK secret=8a read=1 authorized=1 data=8a
CHECK secret=8b read=0 authorized=0 data=00
CHECK secret=8b read=0 authorized=1 data=00
CHECK secret=8b read=1 authorized=0 data=00
CHECK secret=8b read=1 authorized=1 data=8b
CHECK secret=8c read=0 authorized=0 data=00
CHECK secret=8c read=0 authorized=1 data=00
CHECK secret=8c read=1 authorized=0 data=00
CHECK secret=8c read=1 authorized=1 data=8c
CHECK secret=8d read=0 authorized=0 data=00
CHECK secret=8d read=0 authorized=1 data=00
CHECK secret=8d read=1 authorized=0 data=00
CHECK secret=8d read=1 authorized=1 data=8d
CHECK secret=8e read=0 authorized=0 data=00
CHECK secret=8e read=0 authorized=1 data=00
CHECK secret=8e read=1 authorized=0 data=00
CHECK secret=8e read=1 authorized=1 data=8e
CHECK secret=8f read=0 authorized=0 data=00
CHECK secret=8f read=0 authorized=1 data=00
CHECK secret=8f read=1 authorized=0 data=00
CHECK secret=8f read=1 authorized=1 data=8f
CHECK secret=90 read=0 authorized=0 data=00
CHECK secret=90 read=0 authorized=1 data=00
CHECK secret=90 read=1 authorized=0 data=00
CHECK secret=90 read=1 authorized=1 data=90
CHECK secret=91 read=0 authorized=0 data=00
CHECK secret=91 read=0 authorized=1 data=00
CHECK secret=91 read=1 authorized=0 data=00
CHECK secret=91 read=1 authorized=1 data=91
CHECK secret=92 read=0 authorized=0 data=00
CHECK secret=92 read=0 authorized=1 data=00
CHECK secret=92 read=1 authorized=0 data=00
CHECK secret=92 read=1 authorized=1 data=92
CHECK secret=93 read=0 authorized=0 data=00
CHECK secret=93 read=0 authorized=1 data=00
CHECK secret=93 read=1 authorized=0 data=00
CHECK secret=93 read=1 authorized=1 data=93
CHECK secret=94 read=0 authorized=0 data=00
CHECK secret=94 read=0 authorized=1 data=00
CHECK secret=94 read=1 authorized=0 data=00
CHECK secret=94 read=1 authorized=1 data=94
CHECK secret=95 read=0 authorized=0 data=00
CHECK secret=95 read=0 authorized=1 data=00
CHECK secret=95 read=1 authorized=0 data=00
CHECK secret=95 read=1 authorized=1 data=95
CHECK secret=96 read=0 authorized=0 data=00
CHECK secret=96 read=0 authorized=1 data=00
CHECK secret=96 read=1 authorized=0 data=00
CHECK secret=96 read=1 authorized=1 data=96
CHECK secret=97 read=0 authorized=0 data=00
CHECK secret=97 read=0 authorized=1 data=00
CHECK secret=97 read=1 authorized=0 data=00
CHECK secret=97 read=1 authorized=1 data=97
CHECK secret=98 read=0 authorized=0 data=00
CHECK secret=98 read=0 authorized=1 data=00
CHECK secret=98 read=1 authorized=0 data=00
CHECK secret=98 read=1 authorized=1 data=98
CHECK secret=99 read=0 authorized=0 data=00
CHECK secret=99 read=0 authorized=1 data=00
CHECK secret=99 read=1 authorized=0 data=00
CHECK secret=99 read=1 authorized=1 data=99
CHECK secret=9a read=0 authorized=0 data=00
CHECK secret=9a read=0 authorized=1 data=00
CHECK secret=9a read=1 authorized=0 data=00
CHECK secret=9a read=1 authorized=1 data=9a
CHECK secret=9b read=0 authorized=0 data=00
CHECK secret=9b read=0 authorized=1 data=00
CHECK secret=9b read=1 authorized=0 data=00
CHECK secret=9b read=1 authorized=1 data=9b
CHECK secret=9c read=0 authorized=0 data=00
CHECK secret=9c read=0 authorized=1 data=00
CHECK secret=9c read=1 authorized=0 data=00
CHECK secret=9c read=1 authorized=1 data=9c
CHECK secret=9d read=0 authorized=0 data=00
CHECK secret=9d read=0 authorized=1 data=00
CHECK secret=9d read=1 authorized=0 data=00
CHECK secret=9d read=1 authorized=1 data=9d
CHECK secret=9e read=0 authorized=0 data=00
CHECK secret=9e read=0 authorized=1 data=00
CHECK secret=9e read=1 authorized=0 data=00
CHECK secret=9e read=1 authorized=1 data=9e
CHECK secret=9f read=0 authorized=0 data=00
CHECK secret=9f read=0 authorized=1 data=00
CHECK secret=9f read=1 authorized=0 data=00
CHECK secret=9f read=1 authorized=1 data=9f
CHECK secret=a0 read=0 authorized=0 data=00
CHECK secret=a0 read=0 authorized=1 data=00
CHECK secret=a0 read=1 authorized=0 data=00
CHECK secret=a0 read=1 authorized=1 data=a0
CHECK secret=a1 read=0 authorized=0 data=00
CHECK secret=a1 read=0 authorized=1 data=00
CHECK secret=a1 read=1 authorized=0 data=00
CHECK secret=a1 read=1 authorized=1 data=a1
CHECK secret=a2 read=0 authorized=0 data=00
CHECK secret=a2 read=0 authorized=1 data=00
CHECK secret=a2 read=1 authorized=0 data=00
CHECK secret=a2 read=1 authorized=1 data=a2
CHECK secret=a3 read=0 authorized=0 data=00
CHECK secret=a3 read=0 authorized=1 data=00
CHECK secret=a3 read=1 authorized=0 data=00
CHECK secret=a3 read=1 authorized=1 data=a3
CHECK secret=a4 read=0 authorized=0 data=00
CHECK secret=a4 read=0 authorized=1 data=00
CHECK secret=a4 read=1 authorized=0 data=00
CHECK secret=a4 read=1 authorized=1 data=a4
CHECK secret=a5 read=0 authorized=0 data=00
CHECK secret=a5 read=0 authorized=1 data=00
CHECK secret=a5 read=1 authorized=0 data=00
CHECK secret=a5 read=1 authorized=1 data=a5
CHECK secret=a6 read=0 authorized=0 data=00
CHECK secret=a6 read=0 authorized=1 data=00
CHECK secret=a6 read=1 authorized=0 data=00
CHECK secret=a6 read=1 authorized=1 data=a6
CHECK secret=a7 read=0 authorized=0 data=00
CHECK secret=a7 read=0 authorized=1 data=00
CHECK secret=a7 read=1 authorized=0 data=00
CHECK secret=a7 read=1 authorized=1 data=a7
CHECK secret=a8 read=0 authorized=0 data=00
CHECK secret=a8 read=0 authorized=1 data=00
CHECK secret=a8 read=1 authorized=0 data=00
CHECK secret=a8 read=1 authorized=1 data=a8
CHECK secret=a9 read=0 authorized=0 data=00
CHECK secret=a9 read=0 authorized=1 data=00
CHECK secret=a9 read=1 authorized=0 data=00
CHECK secret=a9 read=1 authorized=1 data=a9
CHECK secret=aa read=0 authorized=0 data=00
CHECK secret=aa read=0 authorized=1 data=00
CHECK secret=aa read=1 authorized=0 data=00
CHECK secret=aa read=1 authorized=1 data=aa
CHECK secret=ab read=0 authorized=0 data=00
CHECK secret=ab read=0 authorized=1 data=00
CHECK secret=ab read=1 authorized=0 data=00
CHECK secret=ab read=1 authorized=1 data=ab
CHECK secret=ac read=0 authorized=0 data=00
CHECK secret=ac read=0 authorized=1 data=00
CHECK secret=ac read=1 authorized=0 data=00
CHECK secret=ac read=1 authorized=1 data=ac
CHECK secret=ad read=0 authorized=0 data=00
CHECK secret=ad read=0 authorized=1 data=00
CHECK secret=ad read=1 authorized=0 data=00
CHECK secret=ad read=1 authorized=1 data=ad
CHECK secret=ae read=0 authorized=0 data=00
CHECK secret=ae read=0 authorized=1 data=00
CHECK secret=ae read=1 authorized=0 data=00
CHECK secret=ae read=1 authorized=1 data=ae
CHECK secret=af read=0 authorized=0 data=00
CHECK secret=af read=0 authorized=1 data=00
CHECK secret=af read=1 authorized=0 data=00
CHECK secret=af read=1 authorized=1 data=af
CHECK secret=b0 read=0 authorized=0 data=00
CHECK secret=b0 read=0 authorized=1 data=00
CHECK secret=b0 read=1 authorized=0 data=00
CHECK secret=b0 read=1 authorized=1 data=b0
CHECK secret=b1 read=0 authorized=0 data=00
CHECK secret=b1 read=0 authorized=1 data=00
CHECK secret=b1 read=1 authorized=0 data=00
CHECK secret=b1 read=1 authorized=1 data=b1
CHECK secret=b2 read=0 authorized=0 data=00
CHECK secret=b2 read=0 authorized=1 data=00
CHECK secret=b2 read=1 authorized=0 data=00
CHECK secret=b2 read=1 authorized=1 data=b2
CHECK secret=b3 read=0 authorized=0 data=00
CHECK secret=b3 read=0 authorized=1 data=00
CHECK secret=b3 read=1 authorized=0 data=00
CHECK secret=b3 read=1 authorized=1 data=b3
CHECK secret=b4 read=0 authorized=0 data=00
CHECK secret=b4 read=0 authorized=1 data=00
CHECK secret=b4 read=1 authorized=0 data=00
CHECK secret=b4 read=1 authorized=1 data=b4
CHECK secret=b5 read=0 authorized=0 data=00
CHECK secret=b5 read=0 authorized=1 data=00
CHECK secret=b5 read=1 authorized=0 data=00
CHECK secret=b5 read=1 authorized=1 data=b5
CHECK secret=b6 read=0 authorized=0 data=00
CHECK secret=b6 read=0 authorized=1 data=00
CHECK secret=b6 read=1 authorized=0 data=00
CHECK secret=b6 read=1 authorized=1 data=b6
CHECK secret=b7 read=0 authorized=0 data=00
CHECK secret=b7 read=0 authorized=1 data=00
CHECK secret=b7 read=1 authorized=0 data=00
CHECK secret=b7 read=1 authorized=1 data=b7
CHECK secret=b8 read=0 authorized=0 data=00
CHECK secret=b8 read=0 authorized=1 data=00
CHECK secret=b8 read=1 authorized=0 data=00
CHECK secret=b8 read=1 authorized=1 data=b8
CHECK secret=b9 read=0 authorized=0 data=00
CHECK secret=b9 read=0 authorized=1 data=00
CHECK secret=b9 read=1 authorized=0 data=00
CHECK secret=b9 read=1 authorized=1 data=b9
CHECK secret=ba read=0 authorized=0 data=00
CHECK secret=ba read=0 authorized=1 data=00
CHECK secret=ba read=1 authorized=0 data=00
CHECK secret=ba read=1 authorized=1 data=ba
CHECK secret=bb read=0 authorized=0 data=00
CHECK secret=bb read=0 authorized=1 data=00
CHECK secret=bb read=1 authorized=0 data=00
CHECK secret=bb read=1 authorized=1 data=bb
CHECK secret=bc read=0 authorized=0 data=00
CHECK secret=bc read=0 authorized=1 data=00
CHECK secret=bc read=1 authorized=0 data=00
CHECK secret=bc read=1 authorized=1 data=bc
CHECK secret=bd read=0 authorized=0 data=00
CHECK secret=bd read=0 authorized=1 data=00
CHECK secret=bd read=1 authorized=0 data=00
CHECK secret=bd read=1 authorized=1 data=bd
CHECK secret=be read=0 authorized=0 data=00
CHECK secret=be read=0 authorized=1 data=00
CHECK secret=be read=1 authorized=0 data=00
CHECK secret=be read=1 authorized=1 data=be
CHECK secret=bf read=0 authorized=0 data=00
CHECK secret=bf read=0 authorized=1 data=00
CHECK secret=bf read=1 authorized=0 data=00
CHECK secret=bf read=1 authorized=1 data=bf
CHECK secret=c0 read=0 authorized=0 data=00
CHECK secret=c0 read=0 authorized=1 data=00
CHECK secret=c0 read=1 authorized=0 data=00
CHECK secret=c0 read=1 authorized=1 data=c0
CHECK secret=c1 read=0 authorized=0 data=00
CHECK secret=c1 read=0 authorized=1 data=00
CHECK secret=c1 read=1 authorized=0 data=00
CHECK secret=c1 read=1 authorized=1 data=c1
CHECK secret=c2 read=0 authorized=0 data=00
CHECK secret=c2 read=0 authorized=1 data=00
CHECK secret=c2 read=1 authorized=0 data=00
CHECK secret=c2 read=1 authorized=1 data=c2
CHECK secret=c3 read=0 authorized=0 data=00
CHECK secret=c3 read=0 authorized=1 data=00
CHECK secret=c3 read=1 authorized=0 data=00
CHECK secret=c3 read=1 authorized=1 data=c3
CHECK secret=c4 read=0 authorized=0 data=00
CHECK secret=c4 read=0 authorized=1 data=00
CHECK secret=c4 read=1 authorized=0 data=00
CHECK secret=c4 read=1 authorized=1 data=c4
CHECK secret=c5 read=0 authorized=0 data=00
CHECK secret=c5 read=0 authorized=1 data=00
CHECK secret=c5 read=1 authorized=0 data=00
CHECK secret=c5 read=1 authorized=1 data=c5
CHECK secret=c6 read=0 authorized=0 data=00
CHECK secret=c6 read=0 authorized=1 data=00
CHECK secret=c6 read=1 authorized=0 data=00
CHECK secret=c6 read=1 authorized=1 data=c6
CHECK secret=c7 read=0 authorized=0 data=00
CHECK secret=c7 read=0 authorized=1 data=00
CHECK secret=c7 read=1 authorized=0 data=00
CHECK secret=c7 read=1 authorized=1 data=c7
CHECK secret=c8 read=0 authorized=0 data=00
CHECK secret=c8 read=0 authorized=1 data=00
CHECK secret=c8 read=1 authorized=0 data=00
CHECK secret=c8 read=1 authorized=1 data=c8
CHECK secret=c9 read=0 authorized=0 data=00
CHECK secret=c9 read=0 authorized=1 data=00
CHECK secret=c9 read=1 authorized=0 data=00
CHECK secret=c9 read=1 authorized=1 data=c9
CHECK secret=ca read=0 authorized=0 data=00
CHECK secret=ca read=0 authorized=1 data=00
CHECK secret=ca read=1 authorized=0 data=00
CHECK secret=ca read=1 authorized=1 data=ca
CHECK secret=cb read=0 authorized=0 data=00
CHECK secret=cb read=0 authorized=1 data=00
CHECK secret=cb read=1 authorized=0 data=00
CHECK secret=cb read=1 authorized=1 data=cb
CHECK secret=cc read=0 authorized=0 data=00
CHECK secret=cc read=0 authorized=1 data=00
CHECK secret=cc read=1 authorized=0 data=00
CHECK secret=cc read=1 authorized=1 data=cc
CHECK secret=cd read=0 authorized=0 data=00
CHECK secret=cd read=0 authorized=1 data=00
CHECK secret=cd read=1 authorized=0 data=00
CHECK secret=cd read=1 authorized=1 data=cd
CHECK secret=ce read=0 authorized=0 data=00
CHECK secret=ce read=0 authorized=1 data=00
CHECK secret=ce read=1 authorized=0 data=00
CHECK secret=ce read=1 authorized=1 data=ce
CHECK secret=cf read=0 authorized=0 data=00
CHECK secret=cf read=0 authorized=1 data=00
CHECK secret=cf read=1 authorized=0 data=00
CHECK secret=cf read=1 authorized=1 data=cf
CHECK secret=d0 read=0 authorized=0 data=00
CHECK secret=d0 read=0 authorized=1 data=00
CHECK secret=d0 read=1 authorized=0 data=00
CHECK secret=d0 read=1 authorized=1 data=d0
CHECK secret=d1 read=0 authorized=0 data=00
CHECK secret=d1 read=0 authorized=1 data=00
CHECK secret=d1 read=1 authorized=0 data=00
CHECK secret=d1 read=1 authorized=1 data=d1
CHECK secret=d2 read=0 authorized=0 data=00
CHECK secret=d2 read=0 authorized=1 data=00
CHECK secret=d2 read=1 authorized=0 data=00
CHECK secret=d2 read=1 authorized=1 data=d2
CHECK secret=d3 read=0 authorized=0 data=00
CHECK secret=d3 read=0 authorized=1 data=00
CHECK secret=d3 read=1 authorized=0 data=00
CHECK secret=d3 read=1 authorized=1 data=d3
CHECK secret=d4 read=0 authorized=0 data=00
CHECK secret=d4 read=0 authorized=1 data=00
CHECK secret=d4 read=1 authorized=0 data=00
CHECK secret=d4 read=1 authorized=1 data=d4
CHECK secret=d5 read=0 authorized=0 data=00
CHECK secret=d5 read=0 authorized=1 data=00
CHECK secret=d5 read=1 authorized=0 data=00
CHECK secret=d5 read=1 authorized=1 data=d5
CHECK secret=d6 read=0 authorized=0 data=00
CHECK secret=d6 read=0 authorized=1 data=00
CHECK secret=d6 read=1 authorized=0 data=00
CHECK secret=d6 read=1 authorized=1 data=d6
CHECK secret=d7 read=0 authorized=0 data=00
CHECK secret=d7 read=0 authorized=1 data=00
CHECK secret=d7 read=1 authorized=0 data=00
CHECK secret=d7 read=1 authorized=1 data=d7
CHECK secret=d8 read=0 authorized=0 data=00
CHECK secret=d8 read=0 authorized=1 data=00
CHECK secret=d8 read=1 authorized=0 data=00
CHECK secret=d8 read=1 authorized=1 data=d8
CHECK secret=d9 read=0 authorized=0 data=00
CHECK secret=d9 read=0 authorized=1 data=00
CHECK secret=d9 read=1 authorized=0 data=00
CHECK secret=d9 read=1 authorized=1 data=d9
CHECK secret=da read=0 authorized=0 data=00
CHECK secret=da read=0 authorized=1 data=00
CHECK secret=da read=1 authorized=0 data=00
CHECK secret=da read=1 authorized=1 data=da
CHECK secret=db read=0 authorized=0 data=00
CHECK secret=db read=0 authorized=1 data=00
CHECK secret=db read=1 authorized=0 data=00
CHECK secret=db read=1 authorized=1 data=db
CHECK secret=dc read=0 authorized=0 data=00
CHECK secret=dc read=0 authorized=1 data=00
CHECK secret=dc read=1 authorized=0 data=00
CHECK secret=dc read=1 authorized=1 data=dc
CHECK secret=dd read=0 authorized=0 data=00
CHECK secret=dd read=0 authorized=1 data=00
CHECK secret=dd read=1 authorized=0 data=00
CHECK secret=dd read=1 authorized=1 data=dd
CHECK secret=de read=0 authorized=0 data=00
CHECK secret=de read=0 authorized=1 data=00
CHECK secret=de read=1 authorized=0 data=00
CHECK secret=de read=1 authorized=1 data=de
CHECK secret=df read=0 authorized=0 data=00
CHECK secret=df read=0 authorized=1 data=00
CHECK secret=df read=1 authorized=0 data=00
CHECK secret=df read=1 authorized=1 data=df
CHECK secret=e0 read=0 authorized=0 data=00
CHECK secret=e0 read=0 authorized=1 data=00
CHECK secret=e0 read=1 authorized=0 data=00
CHECK secret=e0 read=1 authorized=1 data=e0
CHECK secret=e1 read=0 authorized=0 data=00
CHECK secret=e1 read=0 authorized=1 data=00
CHECK secret=e1 read=1 authorized=0 data=00
CHECK secret=e1 read=1 authorized=1 data=e1
CHECK secret=e2 read=0 authorized=0 data=00
CHECK secret=e2 read=0 authorized=1 data=00
CHECK secret=e2 read=1 authorized=0 data=00
CHECK secret=e2 read=1 authorized=1 data=e2
CHECK secret=e3 read=0 authorized=0 data=00
CHECK secret=e3 read=0 authorized=1 data=00
CHECK secret=e3 read=1 authorized=0 data=00
CHECK secret=e3 read=1 authorized=1 data=e3
CHECK secret=e4 read=0 authorized=0 data=00
CHECK secret=e4 read=0 authorized=1 data=00
CHECK secret=e4 read=1 authorized=0 data=00
CHECK secret=e4 read=1 authorized=1 data=e4
CHECK secret=e5 read=0 authorized=0 data=00
CHECK secret=e5 read=0 authorized=1 data=00
CHECK secret=e5 read=1 authorized=0 data=00
CHECK secret=e5 read=1 authorized=1 data=e5
CHECK secret=e6 read=0 authorized=0 data=00
CHECK secret=e6 read=0 authorized=1 data=00
CHECK secret=e6 read=1 authorized=0 data=00
CHECK secret=e6 read=1 authorized=1 data=e6
CHECK secret=e7 read=0 authorized=0 data=00
CHECK secret=e7 read=0 authorized=1 data=00
CHECK secret=e7 read=1 authorized=0 data=00
CHECK secret=e7 read=1 authorized=1 data=e7
CHECK secret=e8 read=0 authorized=0 data=00
CHECK secret=e8 read=0 authorized=1 data=00
CHECK secret=e8 read=1 authorized=0 data=00
CHECK secret=e8 read=1 authorized=1 data=e8
CHECK secret=e9 read=0 authorized=0 data=00
CHECK secret=e9 read=0 authorized=1 data=00
CHECK secret=e9 read=1 authorized=0 data=00
CHECK secret=e9 read=1 authorized=1 data=e9
CHECK secret=ea read=0 authorized=0 data=00
CHECK secret=ea read=0 authorized=1 data=00
CHECK secret=ea read=1 authorized=0 data=00
CHECK secret=ea read=1 authorized=1 data=ea
CHECK secret=eb read=0 authorized=0 data=00
CHECK secret=eb read=0 authorized=1 data=00
CHECK secret=eb read=1 authorized=0 data=00
CHECK secret=eb read=1 authorized=1 data=eb
CHECK secret=ec read=0 authorized=0 data=00
CHECK secret=ec read=0 authorized=1 data=00
CHECK secret=ec read=1 authorized=0 data=00
CHECK secret=ec read=1 authorized=1 data=ec
CHECK secret=ed read=0 authorized=0 data=00
CHECK secret=ed read=0 authorized=1 data=00
CHECK secret=ed read=1 authorized=0 data=00
CHECK secret=ed read=1 authorized=1 data=ed
CHECK secret=ee read=0 authorized=0 data=00
CHECK secret=ee read=0 authorized=1 data=00
CHECK secret=ee read=1 authorized=0 data=00
CHECK secret=ee read=1 authorized=1 data=ee
CHECK secret=ef read=0 authorized=0 data=00
CHECK secret=ef read=0 authorized=1 data=00
CHECK secret=ef read=1 authorized=0 data=00
CHECK secret=ef read=1 authorized=1 data=ef
CHECK secret=f0 read=0 authorized=0 data=00
CHECK secret=f0 read=0 authorized=1 data=00
CHECK secret=f0 read=1 authorized=0 data=00
CHECK secret=f0 read=1 authorized=1 data=f0
CHECK secret=f1 read=0 authorized=0 data=00
CHECK secret=f1 read=0 authorized=1 data=00
CHECK secret=f1 read=1 authorized=0 data=00
CHECK secret=f1 read=1 authorized=1 data=f1
CHECK secret=f2 read=0 authorized=0 data=00
CHECK secret=f2 read=0 authorized=1 data=00
CHECK secret=f2 read=1 authorized=0 data=00
CHECK secret=f2 read=1 authorized=1 data=f2
CHECK secret=f3 read=0 authorized=0 data=00
CHECK secret=f3 read=0 authorized=1 data=00
CHECK secret=f3 read=1 authorized=0 data=00
CHECK secret=f3 read=1 authorized=1 data=f3
CHECK secret=f4 read=0 authorized=0 data=00
CHECK secret=f4 read=0 authorized=1 data=00
CHECK secret=f4 read=1 authorized=0 data=00
CHECK secret=f4 read=1 authorized=1 data=f4
CHECK secret=f5 read=0 authorized=0 data=00
CHECK secret=f5 read=0 authorized=1 data=00
CHECK secret=f5 read=1 authorized=0 data=00
CHECK secret=f5 read=1 authorized=1 data=f5
CHECK secret=f6 read=0 authorized=0 data=00
CHECK secret=f6 read=0 authorized=1 data=00
CHECK secret=f6 read=1 authorized=0 data=00
CHECK secret=f6 read=1 authorized=1 data=f6
CHECK secret=f7 read=0 authorized=0 data=00
CHECK secret=f7 read=0 authorized=1 data=00
CHECK secret=f7 read=1 authorized=0 data=00
CHECK secret=f7 read=1 authorized=1 data=f7
CHECK secret=f8 read=0 authorized=0 data=00
CHECK secret=f8 read=0 authorized=1 data=00
CHECK secret=f8 read=1 authorized=0 data=00
CHECK secret=f8 read=1 authorized=1 data=f8
CHECK secret=f9 read=0 authorized=0 data=00
CHECK secret=f9 read=0 authorized=1 data=00
CHECK secret=f9 read=1 authorized=0 data=00
CHECK secret=f9 read=1 authorized=1 data=f9
CHECK secret=fa read=0 authorized=0 data=00
CHECK secret=fa read=0 authorized=1 data=00
CHECK secret=fa read=1 authorized=0 data=00
CHECK secret=fa read=1 authorized=1 data=fa
CHECK secret=fb read=0 authorized=0 data=00
CHECK secret=fb read=0 authorized=1 data=00
CHECK secret=fb read=1 authorized=0 data=00
CHECK secret=fb read=1 authorized=1 data=fb
CHECK secret=fc read=0 authorized=0 data=00
CHECK secret=fc read=0 authorized=1 data=00
CHECK secret=fc read=1 authorized=0 data=00
CHECK secret=fc read=1 authorized=1 data=fc
CHECK secret=fd read=0 authorized=0 data=00
CHECK secret=fd read=0 authorized=1 data=00
CHECK secret=fd read=1 authorized=0 data=00
CHECK secret=fd read=1 authorized=1 data=fd
CHECK secret=fe read=0 authorized=0 data=00
CHECK secret=fe read=0 authorized=1 data=00
CHECK secret=fe read=1 authorized=0 data=00
CHECK secret=fe read=1 authorized=1 data=fe
CHECK secret=ff read=0 authorized=0 data=00
CHECK secret=ff read=0 authorized=1 data=00
CHECK secret=ff read=1 authorized=0 data=00
CHECK secret=ff read=1 authorized=1 data=ff
SECURITY_TEST_PASS
```

Observed: `property_held_for_test`; expected: `property_held_for_test`; evidence passed: `True`; strict result: `True`.

## case_06 / trial 1

Debug output equals the protected byte only when debug_read and authorized are asserted; otherwise output is zero.

1. Staged and SHA-256 hashed design and testbench.
3. Called `compile_rtl` with `{"sources": [".llm4security-suite/security-v1/case_06/design.sv", ".llm4security-suite/security-v1/case_06/tb.sv"], "top": "tb"}`.
   Run `c37af7ae697e4503be6b0a0ca0f32432`; exit `0`; timeout `False`.
5. Called `simulate` with `{"run_id": "c37af7ae697e4503be6b0a0ca0f32432"}`.
   Run `0370c18e416d4dfda94bcaacc233e808`; exit `1`; timeout `False`.

```text
CHECK secret=00 read=0 authorized=0 data=00
CHECK secret=00 read=0 authorized=1 data=00
CHECK secret=00 read=1 authorized=0 data=00
CHECK secret=00 read=1 authorized=1 data=00
CHECK secret=01 read=0 authorized=0 data=00
CHECK secret=01 read=0 authorized=1 data=00
CHECK secret=01 read=1 authorized=0 data=01
FATAL: /inputs/sources/.llm4security-suite/security-v1/case_06/tb.sv:15: SECURITY_VIOLATION: unauthorized debug output
```

Observed: `property_violated`; expected: `property_violated`; evidence passed: `True`; strict result: `True`.

## case_07 / trial 1

Synchronous reset has priority over load and clears stored data to zero. Otherwise load updates it and idle holds it.

1. Staged and SHA-256 hashed design and testbench.
3. Called `compile_rtl` with `{"sources": [".llm4security-suite/security-v1/case_07/design.sv", ".llm4security-suite/security-v1/case_07/tb.sv"], "top": "tb"}`.
   Run `ee698f6fd4f64dc980a9de789b813c7e`; exit `0`; timeout `False`.
5. Called `simulate` with `{"run_id": "ee698f6fd4f64dc980a9de789b813c7e"}`.
   Run `dbb84d250be94c6ea902f32e9f986f5b`; exit `0`; timeout `False`.

```text
CHECK reset=1 load=0 previous=01 value=00
CHECK reset=1 load=1 previous=01 value=00
CHECK reset=1 load=0 previous=02 value=00
CHECK reset=1 load=1 previous=02 value=00
CHECK reset=1 load=0 previous=03 value=00
CHECK reset=1 load=1 previous=03 value=00
CHECK reset=1 load=0 previous=04 value=00
CHECK reset=1 load=1 previous=04 value=00
CHECK reset=1 load=0 previous=05 value=00
CHECK reset=1 load=1 previous=05 value=00
CHECK reset=1 load=0 previous=06 value=00
CHECK reset=1 load=1 previous=06 value=00
CHECK reset=1 load=0 previous=07 value=00
CHECK reset=1 load=1 previous=07 value=00
CHECK reset=1 load=0 previous=08 value=00
CHECK reset=1 load=1 previous=08 value=00
CHECK reset=1 load=0 previous=09 value=00
CHECK reset=1 load=1 previous=09 value=00
CHECK reset=1 load=0 previous=0a value=00
CHECK reset=1 load=1 previous=0a value=00
CHECK reset=1 load=0 previous=0b value=00
CHECK reset=1 load=1 previous=0b value=00
CHECK reset=1 load=0 previous=0c value=00
CHECK reset=1 load=1 previous=0c value=00
CHECK reset=1 load=0 previous=0d value=00
CHECK reset=1 load=1 previous=0d value=00
CHECK reset=1 load=0 previous=0e value=00
CHECK reset=1 load=1 previous=0e value=00
CHECK reset=1 load=0 previous=0f value=00
CHECK reset=1 load=1 previous=0f value=00
CHECK reset=1 load=0 previous=10 value=00
CHECK reset=1 load=1 previous=10 value=00
CHECK reset=1 load=0 previous=11 value=00
CHECK reset=1 load=1 previous=11 value=00
CHECK reset=1 load=0 previous=12 value=00
CHECK reset=1 load=1 previous=12 value=00
CHECK reset=1 load=0 previous=13 value=00
CHECK reset=1 load=1 previous=13 value=00
CHECK reset=1 load=0 previous=14 value=00
CHECK reset=1 load=1 previous=14 value=00
CHECK reset=1 load=0 previous=15 value=00
CHECK reset=1 load=1 previous=15 value=00
CHECK reset=1 load=0 previous=16 value=00
CHECK reset=1 load=1 previous=16 value=00
CHECK reset=1 load=0 previous=17 value=00
CHECK reset=1 load=1 previous=17 value=00
CHECK reset=1 load=0 previous=18 value=00
CHECK reset=1 load=1 previous=18 value=00
CHECK reset=1 load=0 previous=19 value=00
CHECK reset=1 load=1 previous=19 value=00
CHECK reset=1 load=0 previous=1a value=00
CHECK reset=1 load=1 previous=1a value=00
CHECK reset=1 load=0 previous=1b value=00
CHECK reset=1 load=1 previous=1b value=00
CHECK reset=1 load=0 previous=1c value=00
CHECK reset=1 load=1 previous=1c value=00
CHECK reset=1 load=0 previous=1d value=00
CHECK reset=1 load=1 previous=1d value=00
CHECK reset=1 load=0 previous=1e value=00
CHECK reset=1 load=1 previous=1e value=00
CHECK reset=1 load=0 previous=1f value=00
CHECK reset=1 load=1 previous=1f value=00
CHECK reset=1 load=0 previous=20 value=00
CHECK reset=1 load=1 previous=20 value=00
CHECK reset=1 load=0 previous=21 value=00
CHECK reset=1 load=1 previous=21 value=00
CHECK reset=1 load=0 previous=22 value=00
CHECK reset=1 load=1 previous=22 value=00
CHECK reset=1 load=0 previous=23 value=00
CHECK reset=1 load=1 previous=23 value=00
CHECK reset=1 load=0 previous=24 value=00
CHECK reset=1 load=1 previous=24 value=00
CHECK reset=1 load=0 previous=25 value=00
CHECK reset=1 load=1 previous=25 value=00
CHECK reset=1 load=0 previous=26 value=00
CHECK reset=1 load=1 previous=26 value=00
CHECK reset=1 load=0 previous=27 value=00
CHECK reset=1 load=1 previous=27 value=00
CHECK reset=1 load=0 previous=28 value=00
CHECK reset=1 load=1 previous=28 value=00
CHECK reset=1 load=0 previous=29 value=00
CHECK reset=1 load=1 previous=29 value=00
CHECK reset=1 load=0 previous=2a value=00
CHECK reset=1 load=1 previous=2a value=00
CHECK reset=1 load=0 previous=2b value=00
CHECK reset=1 load=1 previous=2b value=00
CHECK reset=1 load=0 previous=2c value=00
CHECK reset=1 load=1 previous=2c value=00
CHECK reset=1 load=0 previous=2d value=00
CHECK reset=1 load=1 previous=2d value=00
CHECK reset=1 load=0 previous=2e value=00
CHECK reset=1 load=1 previous=2e value=00
CHECK reset=1 load=0 previous=2f value=00
CHECK reset=1 load=1 previous=2f value=00
CHECK reset=1 load=0 previous=30 value=00
CHECK reset=1 load=1 previous=30 value=00
CHECK reset=1 load=0 previous=31 value=00
CHECK reset=1 load=1 previous=31 value=00
CHECK reset=1 load=0 previous=32 value=00
CHECK reset=1 load=1 previous=32 value=00
CHECK reset=1 load=0 previous=33 value=00
CHECK reset=1 load=1 previous=33 value=00
CHECK reset=1 load=0 previous=34 value=00
CHECK reset=1 load=1 previous=34 value=00
CHECK reset=1 load=0 previous=35 value=00
CHECK reset=1 load=1 previous=35 value=00
CHECK reset=1 load=0 previous=36 value=00
CHECK reset=1 load=1 previous=36 value=00
CHECK reset=1 load=0 previous=37 value=00
CHECK reset=1 load=1 previous=37 value=00
CHECK reset=1 load=0 previous=38 value=00
CHECK reset=1 load=1 previous=38 value=00
CHECK reset=1 load=0 previous=39 value=00
CHECK reset=1 load=1 previous=39 value=00
CHECK reset=1 load=0 previous=3a value=00
CHECK reset=1 load=1 previous=3a value=00
CHECK reset=1 load=0 previous=3b value=00
CHECK reset=1 load=1 previous=3b value=00
CHECK reset=1 load=0 previous=3c value=00
CHECK reset=1 load=1 previous=3c value=00
CHECK reset=1 load=0 previous=3d value=00
CHECK reset=1 load=1 previous=3d value=00
CHECK reset=1 load=0 previous=3e value=00
CHECK reset=1 load=1 previous=3e value=00
CHECK reset=1 load=0 previous=3f value=00
CHECK reset=1 load=1 previous=3f value=00
CHECK reset=1 load=0 previous=40 value=00
CHECK reset=1 load=1 previous=40 value=00
CHECK reset=1 load=0 previous=41 value=00
CHECK reset=1 load=1 previous=41 value=00
CHECK reset=1 load=0 previous=42 value=00
CHECK reset=1 load=1 previous=42 value=00
CHECK reset=1 load=0 previous=43 value=00
CHECK reset=1 load=1 previous=43 value=00
CHECK reset=1 load=0 previous=44 value=00
CHECK reset=1 load=1 previous=44 value=00
CHECK reset=1 load=0 previous=45 value=00
CHECK reset=1 load=1 previous=45 value=00
CHECK reset=1 load=0 previous=46 value=00
CHECK reset=1 load=1 previous=46 value=00
CHECK reset=1 load=0 previous=47 value=00
CHECK reset=1 load=1 previous=47 value=00
CHECK reset=1 load=0 previous=48 value=00
CHECK reset=1 load=1 previous=48 value=00
CHECK reset=1 load=0 previous=49 value=00
CHECK reset=1 load=1 previous=49 value=00
CHECK reset=1 load=0 previous=4a value=00
CHECK reset=1 load=1 previous=4a value=00
CHECK reset=1 load=0 previous=4b value=00
CHECK reset=1 load=1 previous=4b value=00
CHECK reset=1 load=0 previous=4c value=00
CHECK reset=1 load=1 previous=4c value=00
CHECK reset=1 load=0 previous=4d value=00
CHECK reset=1 load=1 previous=4d value=00
CHECK reset=1 load=0 previous=4e value=00
CHECK reset=1 load=1 previous=4e value=00
CHECK reset=1 load=0 previous=4f value=00
CHECK reset=1 load=1 previous=4f value=00
CHECK reset=1 load=0 previous=50 value=00
CHECK reset=1 load=1 previous=50 value=00
CHECK reset=1 load=0 previous=51 value=00
CHECK reset=1 load=1 previous=51 value=00
CHECK reset=1 load=0 previous=52 value=00
CHECK reset=1 load=1 previous=52 value=00
CHECK reset=1 load=0 previous=53 value=00
CHECK reset=1 load=1 previous=53 value=00
CHECK reset=1 load=0 previous=54 value=00
CHECK reset=1 load=1 previous=54 value=00
CHECK reset=1 load=0 previous=55 value=00
CHECK reset=1 load=1 previous=55 value=00
CHECK reset=1 load=0 previous=56 value=00
CHECK reset=1 load=1 previous=56 value=00
CHECK reset=1 load=0 previous=57 value=00
CHECK reset=1 load=1 previous=57 value=00
CHECK reset=1 load=0 previous=58 value=00
CHECK reset=1 load=1 previous=58 value=00
CHECK reset=1 load=0 previous=59 value=00
CHECK reset=1 load=1 previous=59 value=00
CHECK reset=1 load=0 previous=5a value=00
CHECK reset=1 load=1 previous=5a value=00
CHECK reset=1 load=0 previous=5b value=00
CHECK reset=1 load=1 previous=5b value=00
CHECK reset=1 load=0 previous=5c value=00
CHECK reset=1 load=1 previous=5c value=00
CHECK reset=1 load=0 previous=5d value=00
CHECK reset=1 load=1 previous=5d value=00
CHECK reset=1 load=0 previous=5e value=00
CHECK reset=1 load=1 previous=5e value=00
CHECK reset=1 load=0 previous=5f value=00
CHECK reset=1 load=1 previous=5f value=00
CHECK reset=1 load=0 previous=60 value=00
CHECK reset=1 load=1 previous=60 value=00
CHECK reset=1 load=0 previous=61 value=00
CHECK reset=1 load=1 previous=61 value=00
CHECK reset=1 load=0 previous=62 value=00
CHECK reset=1 load=1 previous=62 value=00
CHECK reset=1 load=0 previous=63 value=00
CHECK reset=1 load=1 previous=63 value=00
CHECK reset=1 load=0 previous=64 value=00
CHECK reset=1 load=1 previous=64 value=00
CHECK reset=1 load=0 previous=65 value=00
CHECK reset=1 load=1 previous=65 value=00
CHECK reset=1 load=0 previous=66 value=00
CHECK reset=1 load=1 previous=66 value=00
CHECK reset=1 load=0 previous=67 value=00
CHECK reset=1 load=1 previous=67 value=00
CHECK reset=1 load=0 previous=68 value=00
CHECK reset=1 load=1 previous=68 value=00
CHECK reset=1 load=0 previous=69 value=00
CHECK reset=1 load=1 previous=69 value=00
CHECK reset=1 load=0 previous=6a value=00
CHECK reset=1 load=1 previous=6a value=00
CHECK reset=1 load=0 previous=6b value=00
CHECK reset=1 load=1 previous=6b value=00
CHECK reset=1 load=0 previous=6c value=00
CHECK reset=1 load=1 previous=6c value=00
CHECK reset=1 load=0 previous=6d value=00
CHECK reset=1 load=1 previous=6d value=00
CHECK reset=1 load=0 previous=6e value=00
CHECK reset=1 load=1 previous=6e value=00
CHECK reset=1 load=0 previous=6f value=00
CHECK reset=1 load=1 previous=6f value=00
CHECK reset=1 load=0 previous=70 value=00
CHECK reset=1 load=1 previous=70 value=00
CHECK reset=1 load=0 previous=71 value=00
CHECK reset=1 load=1 previous=71 value=00
CHECK reset=1 load=0 previous=72 value=00
CHECK reset=1 load=1 previous=72 value=00
CHECK reset=1 load=0 previous=73 value=00
CHECK reset=1 load=1 previous=73 value=00
CHECK reset=1 load=0 previous=74 value=00
CHECK reset=1 load=1 previous=74 value=00
CHECK reset=1 load=0 previous=75 value=00
CHECK reset=1 load=1 previous=75 value=00
CHECK reset=1 load=0 previous=76 value=00
CHECK reset=1 load=1 previous=76 value=00
CHECK reset=1 load=0 previous=77 value=00
CHECK reset=1 load=1 previous=77 value=00
CHECK reset=1 load=0 previous=78 value=00
CHECK reset=1 load=1 previous=78 value=00
CHECK reset=1 load=0 previous=79 value=00
CHECK reset=1 load=1 previous=79 value=00
CHECK reset=1 load=0 previous=7a value=00
CHECK reset=1 load=1 previous=7a value=00
CHECK reset=1 load=0 previous=7b value=00
CHECK reset=1 load=1 previous=7b value=00
CHECK reset=1 load=0 previous=7c value=00
CHECK reset=1 load=1 previous=7c value=00
CHECK reset=1 load=0 previous=7d value=00
CHECK reset=1 load=1 previous=7d value=00
CHECK reset=1 load=0 previous=7e value=00
CHECK reset=1 load=1 previous=7e value=00
CHECK reset=1 load=0 previous=7f value=00
CHECK reset=1 load=1 previous=7f value=00
CHECK reset=1 load=0 previous=80 value=00
CHECK reset=1 load=1 previous=80 value=00
CHECK reset=1 load=0 previous=81 value=00
CHECK reset=1 load=1 previous=81 value=00
CHECK reset=1 load=0 previous=82 value=00
CHECK reset=1 load=1 previous=82 value=00
CHECK reset=1 load=0 previous=83 value=00
CHECK reset=1 load=1 previous=83 value=00
CHECK reset=1 load=0 previous=84 value=00
CHECK reset=1 load=1 previous=84 value=00
CHECK reset=1 load=0 previous=85 value=00
CHECK reset=1 load=1 previous=85 value=00
CHECK reset=1 load=0 previous=86 value=00
CHECK reset=1 load=1 previous=86 value=00
CHECK reset=1 load=0 previous=87 value=00
CHECK reset=1 load=1 previous=87 value=00
CHECK reset=1 load=0 previous=88 value=00
CHECK reset=1 load=1 previous=88 value=00
CHECK reset=1 load=0 previous=89 value=00
CHECK reset=1 load=1 previous=89 value=00
CHECK reset=1 load=0 previous=8a value=00
CHECK reset=1 load=1 previous=8a value=00
CHECK reset=1 load=0 previous=8b value=00
CHECK reset=1 load=1 previous=8b value=00
CHECK reset=1 load=0 previous=8c value=00
CHECK reset=1 load=1 previous=8c value=00
CHECK reset=1 load=0 previous=8d value=00
CHECK reset=1 load=1 previous=8d value=00
CHECK reset=1 load=0 previous=8e value=00
CHECK reset=1 load=1 previous=8e value=00
CHECK reset=1 load=0 previous=8f value=00
CHECK reset=1 load=1 previous=8f value=00
CHECK reset=1 load=0 previous=90 value=00
CHECK reset=1 load=1 previous=90 value=00
CHECK reset=1 load=0 previous=91 value=00
CHECK reset=1 load=1 previous=91 value=00
CHECK reset=1 load=0 previous=92 value=00
CHECK reset=1 load=1 previous=92 value=00
CHECK reset=1 load=0 previous=93 value=00
CHECK reset=1 load=1 previous=93 value=00
CHECK reset=1 load=0 previous=94 value=00
CHECK reset=1 load=1 previous=94 value=00
CHECK reset=1 load=0 previous=95 value=00
CHECK reset=1 load=1 previous=95 value=00
CHECK reset=1 load=0 previous=96 value=00
CHECK reset=1 load=1 previous=96 value=00
CHECK reset=1 load=0 previous=97 value=00
CHECK reset=1 load=1 previous=97 value=00
CHECK reset=1 load=0 previous=98 value=00
CHECK reset=1 load=1 previous=98 value=00
CHECK reset=1 load=0 previous=99 value=00
CHECK reset=1 load=1 previous=99 value=00
CHECK reset=1 load=0 previous=9a value=00
CHECK reset=1 load=1 previous=9a value=00
CHECK reset=1 load=0 previous=9b value=00
CHECK reset=1 load=1 previous=9b value=00
CHECK reset=1 load=0 previous=9c value=00
CHECK reset=1 load=1 previous=9c value=00
CHECK reset=1 load=0 previous=9d value=00
CHECK reset=1 load=1 previous=9d value=00
CHECK reset=1 load=0 previous=9e value=00
CHECK reset=1 load=1 previous=9e value=00
CHECK reset=1 load=0 previous=9f value=00
CHECK reset=1 load=1 previous=9f value=00
CHECK reset=1 load=0 previous=a0 value=00
CHECK reset=1 load=1 previous=a0 value=00
CHECK reset=1 load=0 previous=a1 value=00
CHECK reset=1 load=1 previous=a1 value=00
CHECK reset=1 load=0 previous=a2 value=00
CHECK reset=1 load=1 previous=a2 value=00
CHECK reset=1 load=0 previous=a3 value=00
CHECK reset=1 load=1 previous=a3 value=00
CHECK reset=1 load=0 previous=a4 value=00
CHECK reset=1 load=1 previous=a4 value=00
CHECK reset=1 load=0 previous=a5 value=00
CHECK reset=1 load=1 previous=a5 value=00
CHECK reset=1 load=0 previous=a6 value=00
CHECK reset=1 load=1 previous=a6 value=00
CHECK reset=1 load=0 previous=a7 value=00
CHECK reset=1 load=1 previous=a7 value=00
CHECK reset=1 load=0 previous=a8 value=00
CHECK reset=1 load=1 previous=a8 value=00
CHECK reset=1 load=0 previous=a9 value=00
CHECK reset=1 load=1 previous=a9 value=00
CHECK reset=1 load=0 previous=aa value=00
CHECK reset=1 load=1 previous=aa value=00
CHECK reset=1 load=0 previous=ab value=00
CHECK reset=1 load=1 previous=ab value=00
CHECK reset=1 load=0 previous=ac value=00
CHECK reset=1 load=1 previous=ac value=00
CHECK reset=1 load=0 previous=ad value=00
CHECK reset=1 load=1 previous=ad value=00
CHECK reset=1 load=0 previous=ae value=00
CHECK reset=1 load=1 previous=ae value=00
CHECK reset=1 load=0 previous=af value=00
CHECK reset=1 load=1 previous=af value=00
CHECK reset=1 load=0 previous=b0 value=00
CHECK reset=1 load=1 previous=b0 value=00
CHECK reset=1 load=0 previous=b1 value=00
CHECK reset=1 load=1 previous=b1 value=00
CHECK reset=1 load=0 previous=b2 value=00
CHECK reset=1 load=1 previous=b2 value=00
CHECK reset=1 load=0 previous=b3 value=00
CHECK reset=1 load=1 previous=b3 value=00
CHECK reset=1 load=0 previous=b4 value=00
CHECK reset=1 load=1 previous=b4 value=00
CHECK reset=1 load=0 previous=b5 value=00
CHECK reset=1 load=1 previous=b5 value=00
CHECK reset=1 load=0 previous=b6 value=00
CHECK reset=1 load=1 previous=b6 value=00
CHECK reset=1 load=0 previous=b7 value=00
CHECK reset=1 load=1 previous=b7 value=00
CHECK reset=1 load=0 previous=b8 value=00
CHECK reset=1 load=1 previous=b8 value=00
CHECK reset=1 load=0 previous=b9 value=00
CHECK reset=1 load=1 previous=b9 value=00
CHECK reset=1 load=0 previous=ba value=00
CHECK reset=1 load=1 previous=ba value=00
CHECK reset=1 load=0 previous=bb value=00
CHECK reset=1 load=1 previous=bb value=00
CHECK reset=1 load=0 previous=bc value=00
CHECK reset=1 load=1 previous=bc value=00
CHECK reset=1 load=0 previous=bd value=00
CHECK reset=1 load=1 previous=bd value=00
CHECK reset=1 load=0 previous=be value=00
CHECK reset=1 load=1 previous=be value=00
CHECK reset=1 load=0 previous=bf value=00
CHECK reset=1 load=1 previous=bf value=00
CHECK reset=1 load=0 previous=c0 value=00
CHECK reset=1 load=1 previous=c0 value=00
CHECK reset=1 load=0 previous=c1 value=00
CHECK reset=1 load=1 previous=c1 value=00
CHECK reset=1 load=0 previous=c2 value=00
CHECK reset=1 load=1 previous=c2 value=00
CHECK reset=1 load=0 previous=c3 value=00
CHECK reset=1 load=1 previous=c3 value=00
CHECK reset=1 load=0 previous=c4 value=00
CHECK reset=1 load=1 previous=c4 value=00
CHECK reset=1 load=0 previous=c5 value=00
CHECK reset=1 load=1 previous=c5 value=00
CHECK reset=1 load=0 previous=c6 value=00
CHECK reset=1 load=1 previous=c6 value=00
CHECK reset=1 load=0 previous=c7 value=00
CHECK reset=1 load=1 previous=c7 value=00
CHECK reset=1 load=0 previous=c8 value=00
CHECK reset=1 load=1 previous=c8 value=00
CHECK reset=1 load=0 previous=c9 value=00
CHECK reset=1 load=1 previous=c9 value=00
CHECK reset=1 load=0 previous=ca value=00
CHECK reset=1 load=1 previous=ca value=00
CHECK reset=1 load=0 previous=cb value=00
CHECK reset=1 load=1 previous=cb value=00
CHECK reset=1 load=0 previous=cc value=00
CHECK reset=1 load=1 previous=cc value=00
CHECK reset=1 load=0 previous=cd value=00
CHECK reset=1 load=1 previous=cd value=00
CHECK reset=1 load=0 previous=ce value=00
CHECK reset=1 load=1 previous=ce value=00
CHECK reset=1 load=0 previous=cf value=00
CHECK reset=1 load=1 previous=cf value=00
CHECK reset=1 load=0 previous=d0 value=00
CHECK reset=1 load=1 previous=d0 value=00
CHECK reset=1 load=0 previous=d1 value=00
CHECK reset=1 load=1 previous=d1 value=00
CHECK reset=1 load=0 previous=d2 value=00
CHECK reset=1 load=1 previous=d2 value=00
CHECK reset=1 load=0 previous=d3 value=00
CHECK reset=1 load=1 previous=d3 value=00
CHECK reset=1 load=0 previous=d4 value=00
CHECK reset=1 load=1 previous=d4 value=00
CHECK reset=1 load=0 previous=d5 value=00
CHECK reset=1 load=1 previous=d5 value=00
CHECK reset=1 load=0 previous=d6 value=00
CHECK reset=1 load=1 previous=d6 value=00
CHECK reset=1 load=0 previous=d7 value=00
CHECK reset=1 load=1 previous=d7 value=00
CHECK reset=1 load=0 previous=d8 value=00
CHECK reset=1 load=1 previous=d8 value=00
CHECK reset=1 load=0 previous=d9 value=00
CHECK reset=1 load=1 previous=d9 value=00
CHECK reset=1 load=0 previous=da value=00
CHECK reset=1 load=1 previous=da value=00
CHECK reset=1 load=0 previous=db value=00
CHECK reset=1 load=1 previous=db value=00
CHECK reset=1 load=0 previous=dc value=00
CHECK reset=1 load=1 previous=dc value=00
CHECK reset=1 load=0 previous=dd value=00
CHECK reset=1 load=1 previous=dd value=00
CHECK reset=1 load=0 previous=de value=00
CHECK reset=1 load=1 previous=de value=00
CHECK reset=1 load=0 previous=df value=00
CHECK reset=1 load=1 previous=df value=00
CHECK reset=1 load=0 previous=e0 value=00
CHECK reset=1 load=1 previous=e0 value=00
CHECK reset=1 load=0 previous=e1 value=00
CHECK reset=1 load=1 previous=e1 value=00
CHECK reset=1 load=0 previous=e2 value=00
CHECK reset=1 load=1 previous=e2 value=00
CHECK reset=1 load=0 previous=e3 value=00
CHECK reset=1 load=1 previous=e3 value=00
CHECK reset=1 load=0 previous=e4 value=00
CHECK reset=1 load=1 previous=e4 value=00
CHECK reset=1 load=0 previous=e5 value=00
CHECK reset=1 load=1 previous=e5 value=00
CHECK reset=1 load=0 previous=e6 value=00
CHECK reset=1 load=1 previous=e6 value=00
CHECK reset=1 load=0 previous=e7 value=00
CHECK reset=1 load=1 previous=e7 value=00
CHECK reset=1 load=0 previous=e8 value=00
CHECK reset=1 load=1 previous=e8 value=00
CHECK reset=1 load=0 previous=e9 value=00
CHECK reset=1 load=1 previous=e9 value=00
CHECK reset=1 load=0 previous=ea value=00
CHECK reset=1 load=1 previous=ea value=00
CHECK reset=1 load=0 previous=eb value=00
CHECK reset=1 load=1 previous=eb value=00
CHECK reset=1 load=0 previous=ec value=00
CHECK reset=1 load=1 previous=ec value=00
CHECK reset=1 load=0 previous=ed value=00
CHECK reset=1 load=1 previous=ed value=00
CHECK reset=1 load=0 previous=ee value=00
CHECK reset=1 load=1 previous=ee value=00
CHECK reset=1 load=0 previous=ef value=00
CHECK reset=1 load=1 previous=ef value=00
CHECK reset=1 load=0 previous=f0 value=00
CHECK reset=1 load=1 previous=f0 value=00
CHECK reset=1 load=0 previous=f1 value=00
CHECK reset=1 load=1 previous=f1 value=00
CHECK reset=1 load=0 previous=f2 value=00
CHECK reset=1 load=1 previous=f2 value=00
CHECK reset=1 load=0 previous=f3 value=00
CHECK reset=1 load=1 previous=f3 value=00
CHECK reset=1 load=0 previous=f4 value=00
CHECK reset=1 load=1 previous=f4 value=00
CHECK reset=1 load=0 previous=f5 value=00
CHECK reset=1 load=1 previous=f5 value=00
CHECK reset=1 load=0 previous=f6 value=00
CHECK reset=1 load=1 previous=f6 value=00
CHECK reset=1 load=0 previous=f7 value=00
CHECK reset=1 load=1 previous=f7 value=00
CHECK reset=1 load=0 previous=f8 value=00
CHECK reset=1 load=1 previous=f8 value=00
CHECK reset=1 load=0 previous=f9 value=00
CHECK reset=1 load=1 previous=f9 value=00
CHECK reset=1 load=0 previous=fa value=00
CHECK reset=1 load=1 previous=fa value=00
CHECK reset=1 load=0 previous=fb value=00
CHECK reset=1 load=1 previous=fb value=00
CHECK reset=1 load=0 previous=fc value=00
CHECK reset=1 load=1 previous=fc value=00
CHECK reset=1 load=0 previous=fd value=00
CHECK reset=1 load=1 previous=fd value=00
CHECK reset=1 load=0 previous=fe value=00
CHECK reset=1 load=1 previous=fe value=00
CHECK reset=1 load=0 previous=ff value=00
CHECK reset=1 load=1 previous=ff value=00
SECURITY_TEST_PASS
```

Observed: `property_held_for_test`; expected: `property_held_for_test`; evidence passed: `True`; strict result: `True`.

## case_08 / trial 1

Synchronous reset has priority over load and clears stored data to zero. Otherwise load updates it and idle holds it.

1. Staged and SHA-256 hashed design and testbench.
3. Called `compile_rtl` with `{"sources": [".llm4security-suite/security-v1/case_08/design.sv", ".llm4security-suite/security-v1/case_08/tb.sv"], "top": "tb"}`.
   Run `8acc8406cfb540739804c7b64bf6fadd`; exit `0`; timeout `False`.
5. Called `simulate` with `{"run_id": "8acc8406cfb540739804c7b64bf6fadd"}`.
   Run `7e682f4c1dfb459c8401fa7992922317`; exit `1`; timeout `False`.

```text
CHECK reset=1 load=0 previous=01 value=00
CHECK reset=1 load=1 previous=01 value=01
FATAL: /inputs/sources/.llm4security-suite/security-v1/case_08/tb.sv:18: SECURITY_VIOLATION: reset did not clear data
```

Observed: `property_violated`; expected: `property_violated`; evidence passed: `True`; strict result: `True`.

## case_09 / trial 1

Enabled output equals protected data. Disabled output is zero for every protected byte.

1. Staged and SHA-256 hashed design and testbench.
3. Called `compile_rtl` with `{"sources": [".llm4security-suite/security-v1/case_09/design.sv", ".llm4security-suite/security-v1/case_09/tb.sv"], "top": "tb"}`.
   Run `b54abd1fe26a429e9c6eb6c07d30b88d`; exit `0`; timeout `False`.
5. Called `simulate` with `{"run_id": "b54abd1fe26a429e9c6eb6c07d30b88d"}`.
   Run `ab42afb2da3f4f84bb66b9c61e91f496`; exit `0`; timeout `False`.

```text
CHECK secret=00 enabled=0 data=00
CHECK secret=00 enabled=1 data=00
CHECK secret=01 enabled=0 data=00
CHECK secret=01 enabled=1 data=01
CHECK secret=02 enabled=0 data=00
CHECK secret=02 enabled=1 data=02
CHECK secret=03 enabled=0 data=00
CHECK secret=03 enabled=1 data=03
CHECK secret=04 enabled=0 data=00
CHECK secret=04 enabled=1 data=04
CHECK secret=05 enabled=0 data=00
CHECK secret=05 enabled=1 data=05
CHECK secret=06 enabled=0 data=00
CHECK secret=06 enabled=1 data=06
CHECK secret=07 enabled=0 data=00
CHECK secret=07 enabled=1 data=07
CHECK secret=08 enabled=0 data=00
CHECK secret=08 enabled=1 data=08
CHECK secret=09 enabled=0 data=00
CHECK secret=09 enabled=1 data=09
CHECK secret=0a enabled=0 data=00
CHECK secret=0a enabled=1 data=0a
CHECK secret=0b enabled=0 data=00
CHECK secret=0b enabled=1 data=0b
CHECK secret=0c enabled=0 data=00
CHECK secret=0c enabled=1 data=0c
CHECK secret=0d enabled=0 data=00
CHECK secret=0d enabled=1 data=0d
CHECK secret=0e enabled=0 data=00
CHECK secret=0e enabled=1 data=0e
CHECK secret=0f enabled=0 data=00
CHECK secret=0f enabled=1 data=0f
CHECK secret=10 enabled=0 data=00
CHECK secret=10 enabled=1 data=10
CHECK secret=11 enabled=0 data=00
CHECK secret=11 enabled=1 data=11
CHECK secret=12 enabled=0 data=00
CHECK secret=12 enabled=1 data=12
CHECK secret=13 enabled=0 data=00
CHECK secret=13 enabled=1 data=13
CHECK secret=14 enabled=0 data=00
CHECK secret=14 enabled=1 data=14
CHECK secret=15 enabled=0 data=00
CHECK secret=15 enabled=1 data=15
CHECK secret=16 enabled=0 data=00
CHECK secret=16 enabled=1 data=16
CHECK secret=17 enabled=0 data=00
CHECK secret=17 enabled=1 data=17
CHECK secret=18 enabled=0 data=00
CHECK secret=18 enabled=1 data=18
CHECK secret=19 enabled=0 data=00
CHECK secret=19 enabled=1 data=19
CHECK secret=1a enabled=0 data=00
CHECK secret=1a enabled=1 data=1a
CHECK secret=1b enabled=0 data=00
CHECK secret=1b enabled=1 data=1b
CHECK secret=1c enabled=0 data=00
CHECK secret=1c enabled=1 data=1c
CHECK secret=1d enabled=0 data=00
CHECK secret=1d enabled=1 data=1d
CHECK secret=1e enabled=0 data=00
CHECK secret=1e enabled=1 data=1e
CHECK secret=1f enabled=0 data=00
CHECK secret=1f enabled=1 data=1f
CHECK secret=20 enabled=0 data=00
CHECK secret=20 enabled=1 data=20
CHECK secret=21 enabled=0 data=00
CHECK secret=21 enabled=1 data=21
CHECK secret=22 enabled=0 data=00
CHECK secret=22 enabled=1 data=22
CHECK secret=23 enabled=0 data=00
CHECK secret=23 enabled=1 data=23
CHECK secret=24 enabled=0 data=00
CHECK secret=24 enabled=1 data=24
CHECK secret=25 enabled=0 data=00
CHECK secret=25 enabled=1 data=25
CHECK secret=26 enabled=0 data=00
CHECK secret=26 enabled=1 data=26
CHECK secret=27 enabled=0 data=00
CHECK secret=27 enabled=1 data=27
CHECK secret=28 enabled=0 data=00
CHECK secret=28 enabled=1 data=28
CHECK secret=29 enabled=0 data=00
CHECK secret=29 enabled=1 data=29
CHECK secret=2a enabled=0 data=00
CHECK secret=2a enabled=1 data=2a
CHECK secret=2b enabled=0 data=00
CHECK secret=2b enabled=1 data=2b
CHECK secret=2c enabled=0 data=00
CHECK secret=2c enabled=1 data=2c
CHECK secret=2d enabled=0 data=00
CHECK secret=2d enabled=1 data=2d
CHECK secret=2e enabled=0 data=00
CHECK secret=2e enabled=1 data=2e
CHECK secret=2f enabled=0 data=00
CHECK secret=2f enabled=1 data=2f
CHECK secret=30 enabled=0 data=00
CHECK secret=30 enabled=1 data=30
CHECK secret=31 enabled=0 data=00
CHECK secret=31 enabled=1 data=31
CHECK secret=32 enabled=0 data=00
CHECK secret=32 enabled=1 data=32
CHECK secret=33 enabled=0 data=00
CHECK secret=33 enabled=1 data=33
CHECK secret=34 enabled=0 data=00
CHECK secret=34 enabled=1 data=34
CHECK secret=35 enabled=0 data=00
CHECK secret=35 enabled=1 data=35
CHECK secret=36 enabled=0 data=00
CHECK secret=36 enabled=1 data=36
CHECK secret=37 enabled=0 data=00
CHECK secret=37 enabled=1 data=37
CHECK secret=38 enabled=0 data=00
CHECK secret=38 enabled=1 data=38
CHECK secret=39 enabled=0 data=00
CHECK secret=39 enabled=1 data=39
CHECK secret=3a enabled=0 data=00
CHECK secret=3a enabled=1 data=3a
CHECK secret=3b enabled=0 data=00
CHECK secret=3b enabled=1 data=3b
CHECK secret=3c enabled=0 data=00
CHECK secret=3c enabled=1 data=3c
CHECK secret=3d enabled=0 data=00
CHECK secret=3d enabled=1 data=3d
CHECK secret=3e enabled=0 data=00
CHECK secret=3e enabled=1 data=3e
CHECK secret=3f enabled=0 data=00
CHECK secret=3f enabled=1 data=3f
CHECK secret=40 enabled=0 data=00
CHECK secret=40 enabled=1 data=40
CHECK secret=41 enabled=0 data=00
CHECK secret=41 enabled=1 data=41
CHECK secret=42 enabled=0 data=00
CHECK secret=42 enabled=1 data=42
CHECK secret=43 enabled=0 data=00
CHECK secret=43 enabled=1 data=43
CHECK secret=44 enabled=0 data=00
CHECK secret=44 enabled=1 data=44
CHECK secret=45 enabled=0 data=00
CHECK secret=45 enabled=1 data=45
CHECK secret=46 enabled=0 data=00
CHECK secret=46 enabled=1 data=46
CHECK secret=47 enabled=0 data=00
CHECK secret=47 enabled=1 data=47
CHECK secret=48 enabled=0 data=00
CHECK secret=48 enabled=1 data=48
CHECK secret=49 enabled=0 data=00
CHECK secret=49 enabled=1 data=49
CHECK secret=4a enabled=0 data=00
CHECK secret=4a enabled=1 data=4a
CHECK secret=4b enabled=0 data=00
CHECK secret=4b enabled=1 data=4b
CHECK secret=4c enabled=0 data=00
CHECK secret=4c enabled=1 data=4c
CHECK secret=4d enabled=0 data=00
CHECK secret=4d enabled=1 data=4d
CHECK secret=4e enabled=0 data=00
CHECK secret=4e enabled=1 data=4e
CHECK secret=4f enabled=0 data=00
CHECK secret=4f enabled=1 data=4f
CHECK secret=50 enabled=0 data=00
CHECK secret=50 enabled=1 data=50
CHECK secret=51 enabled=0 data=00
CHECK secret=51 enabled=1 data=51
CHECK secret=52 enabled=0 data=00
CHECK secret=52 enabled=1 data=52
CHECK secret=53 enabled=0 data=00
CHECK secret=53 enabled=1 data=53
CHECK secret=54 enabled=0 data=00
CHECK secret=54 enabled=1 data=54
CHECK secret=55 enabled=0 data=00
CHECK secret=55 enabled=1 data=55
CHECK secret=56 enabled=0 data=00
CHECK secret=56 enabled=1 data=56
CHECK secret=57 enabled=0 data=00
CHECK secret=57 enabled=1 data=57
CHECK secret=58 enabled=0 data=00
CHECK secret=58 enabled=1 data=58
CHECK secret=59 enabled=0 data=00
CHECK secret=59 enabled=1 data=59
CHECK secret=5a enabled=0 data=00
CHECK secret=5a enabled=1 data=5a
CHECK secret=5b enabled=0 data=00
CHECK secret=5b enabled=1 data=5b
CHECK secret=5c enabled=0 data=00
CHECK secret=5c enabled=1 data=5c
CHECK secret=5d enabled=0 data=00
CHECK secret=5d enabled=1 data=5d
CHECK secret=5e enabled=0 data=00
CHECK secret=5e enabled=1 data=5e
CHECK secret=5f enabled=0 data=00
CHECK secret=5f enabled=1 data=5f
CHECK secret=60 enabled=0 data=00
CHECK secret=60 enabled=1 data=60
CHECK secret=61 enabled=0 data=00
CHECK secret=61 enabled=1 data=61
CHECK secret=62 enabled=0 data=00
CHECK secret=62 enabled=1 data=62
CHECK secret=63 enabled=0 data=00
CHECK secret=63 enabled=1 data=63
CHECK secret=64 enabled=0 data=00
CHECK secret=64 enabled=1 data=64
CHECK secret=65 enabled=0 data=00
CHECK secret=65 enabled=1 data=65
CHECK secret=66 enabled=0 data=00
CHECK secret=66 enabled=1 data=66
CHECK secret=67 enabled=0 data=00
CHECK secret=67 enabled=1 data=67
CHECK secret=68 enabled=0 data=00
CHECK secret=68 enabled=1 data=68
CHECK secret=69 enabled=0 data=00
CHECK secret=69 enabled=1 data=69
CHECK secret=6a enabled=0 data=00
CHECK secret=6a enabled=1 data=6a
CHECK secret=6b enabled=0 data=00
CHECK secret=6b enabled=1 data=6b
CHECK secret=6c enabled=0 data=00
CHECK secret=6c enabled=1 data=6c
CHECK secret=6d enabled=0 data=00
CHECK secret=6d enabled=1 data=6d
CHECK secret=6e enabled=0 data=00
CHECK secret=6e enabled=1 data=6e
CHECK secret=6f enabled=0 data=00
CHECK secret=6f enabled=1 data=6f
CHECK secret=70 enabled=0 data=00
CHECK secret=70 enabled=1 data=70
CHECK secret=71 enabled=0 data=00
CHECK secret=71 enabled=1 data=71
CHECK secret=72 enabled=0 data=00
CHECK secret=72 enabled=1 data=72
CHECK secret=73 enabled=0 data=00
CHECK secret=73 enabled=1 data=73
CHECK secret=74 enabled=0 data=00
CHECK secret=74 enabled=1 data=74
CHECK secret=75 enabled=0 data=00
CHECK secret=75 enabled=1 data=75
CHECK secret=76 enabled=0 data=00
CHECK secret=76 enabled=1 data=76
CHECK secret=77 enabled=0 data=00
CHECK secret=77 enabled=1 data=77
CHECK secret=78 enabled=0 data=00
CHECK secret=78 enabled=1 data=78
CHECK secret=79 enabled=0 data=00
CHECK secret=79 enabled=1 data=79
CHECK secret=7a enabled=0 data=00
CHECK secret=7a enabled=1 data=7a
CHECK secret=7b enabled=0 data=00
CHECK secret=7b enabled=1 data=7b
CHECK secret=7c enabled=0 data=00
CHECK secret=7c enabled=1 data=7c
CHECK secret=7d enabled=0 data=00
CHECK secret=7d enabled=1 data=7d
CHECK secret=7e enabled=0 data=00
CHECK secret=7e enabled=1 data=7e
CHECK secret=7f enabled=0 data=00
CHECK secret=7f enabled=1 data=7f
CHECK secret=80 enabled=0 data=00
CHECK secret=80 enabled=1 data=80
CHECK secret=81 enabled=0 data=00
CHECK secret=81 enabled=1 data=81
CHECK secret=82 enabled=0 data=00
CHECK secret=82 enabled=1 data=82
CHECK secret=83 enabled=0 data=00
CHECK secret=83 enabled=1 data=83
CHECK secret=84 enabled=0 data=00
CHECK secret=84 enabled=1 data=84
CHECK secret=85 enabled=0 data=00
CHECK secret=85 enabled=1 data=85
CHECK secret=86 enabled=0 data=00
CHECK secret=86 enabled=1 data=86
CHECK secret=87 enabled=0 data=00
CHECK secret=87 enabled=1 data=87
CHECK secret=88 enabled=0 data=00
CHECK secret=88 enabled=1 data=88
CHECK secret=89 enabled=0 data=00
CHECK secret=89 enabled=1 data=89
CHECK secret=8a enabled=0 data=00
CHECK secret=8a enabled=1 data=8a
CHECK secret=8b enabled=0 data=00
CHECK secret=8b enabled=1 data=8b
CHECK secret=8c enabled=0 data=00
CHECK secret=8c enabled=1 data=8c
CHECK secret=8d enabled=0 data=00
CHECK secret=8d enabled=1 data=8d
CHECK secret=8e enabled=0 data=00
CHECK secret=8e enabled=1 data=8e
CHECK secret=8f enabled=0 data=00
CHECK secret=8f enabled=1 data=8f
CHECK secret=90 enabled=0 data=00
CHECK secret=90 enabled=1 data=90
CHECK secret=91 enabled=0 data=00
CHECK secret=91 enabled=1 data=91
CHECK secret=92 enabled=0 data=00
CHECK secret=92 enabled=1 data=92
CHECK secret=93 enabled=0 data=00
CHECK secret=93 enabled=1 data=93
CHECK secret=94 enabled=0 data=00
CHECK secret=94 enabled=1 data=94
CHECK secret=95 enabled=0 data=00
CHECK secret=95 enabled=1 data=95
CHECK secret=96 enabled=0 data=00
CHECK secret=96 enabled=1 data=96
CHECK secret=97 enabled=0 data=00
CHECK secret=97 enabled=1 data=97
CHECK secret=98 enabled=0 data=00
CHECK secret=98 enabled=1 data=98
CHECK secret=99 enabled=0 data=00
CHECK secret=99 enabled=1 data=99
CHECK secret=9a enabled=0 data=00
CHECK secret=9a enabled=1 data=9a
CHECK secret=9b enabled=0 data=00
CHECK secret=9b enabled=1 data=9b
CHECK secret=9c enabled=0 data=00
CHECK secret=9c enabled=1 data=9c
CHECK secret=9d enabled=0 data=00
CHECK secret=9d enabled=1 data=9d
CHECK secret=9e enabled=0 data=00
CHECK secret=9e enabled=1 data=9e
CHECK secret=9f enabled=0 data=00
CHECK secret=9f enabled=1 data=9f
CHECK secret=a0 enabled=0 data=00
CHECK secret=a0 enabled=1 data=a0
CHECK secret=a1 enabled=0 data=00
CHECK secret=a1 enabled=1 data=a1
CHECK secret=a2 enabled=0 data=00
CHECK secret=a2 enabled=1 data=a2
CHECK secret=a3 enabled=0 data=00
CHECK secret=a3 enabled=1 data=a3
CHECK secret=a4 enabled=0 data=00
CHECK secret=a4 enabled=1 data=a4
CHECK secret=a5 enabled=0 data=00
CHECK secret=a5 enabled=1 data=a5
CHECK secret=a6 enabled=0 data=00
CHECK secret=a6 enabled=1 data=a6
CHECK secret=a7 enabled=0 data=00
CHECK secret=a7 enabled=1 data=a7
CHECK secret=a8 enabled=0 data=00
CHECK secret=a8 enabled=1 data=a8
CHECK secret=a9 enabled=0 data=00
CHECK secret=a9 enabled=1 data=a9
CHECK secret=aa enabled=0 data=00
CHECK secret=aa enabled=1 data=aa
CHECK secret=ab enabled=0 data=00
CHECK secret=ab enabled=1 data=ab
CHECK secret=ac enabled=0 data=00
CHECK secret=ac enabled=1 data=ac
CHECK secret=ad enabled=0 data=00
CHECK secret=ad enabled=1 data=ad
CHECK secret=ae enabled=0 data=00
CHECK secret=ae enabled=1 data=ae
CHECK secret=af enabled=0 data=00
CHECK secret=af enabled=1 data=af
CHECK secret=b0 enabled=0 data=00
CHECK secret=b0 enabled=1 data=b0
CHECK secret=b1 enabled=0 data=00
CHECK secret=b1 enabled=1 data=b1
CHECK secret=b2 enabled=0 data=00
CHECK secret=b2 enabled=1 data=b2
CHECK secret=b3 enabled=0 data=00
CHECK secret=b3 enabled=1 data=b3
CHECK secret=b4 enabled=0 data=00
CHECK secret=b4 enabled=1 data=b4
CHECK secret=b5 enabled=0 data=00
CHECK secret=b5 enabled=1 data=b5
CHECK secret=b6 enabled=0 data=00
CHECK secret=b6 enabled=1 data=b6
CHECK secret=b7 enabled=0 data=00
CHECK secret=b7 enabled=1 data=b7
CHECK secret=b8 enabled=0 data=00
CHECK secret=b8 enabled=1 data=b8
CHECK secret=b9 enabled=0 data=00
CHECK secret=b9 enabled=1 data=b9
CHECK secret=ba enabled=0 data=00
CHECK secret=ba enabled=1 data=ba
CHECK secret=bb enabled=0 data=00
CHECK secret=bb enabled=1 data=bb
CHECK secret=bc enabled=0 data=00
CHECK secret=bc enabled=1 data=bc
CHECK secret=bd enabled=0 data=00
CHECK secret=bd enabled=1 data=bd
CHECK secret=be enabled=0 data=00
CHECK secret=be enabled=1 data=be
CHECK secret=bf enabled=0 data=00
CHECK secret=bf enabled=1 data=bf
CHECK secret=c0 enabled=0 data=00
CHECK secret=c0 enabled=1 data=c0
CHECK secret=c1 enabled=0 data=00
CHECK secret=c1 enabled=1 data=c1
CHECK secret=c2 enabled=0 data=00
CHECK secret=c2 enabled=1 data=c2
CHECK secret=c3 enabled=0 data=00
CHECK secret=c3 enabled=1 data=c3
CHECK secret=c4 enabled=0 data=00
CHECK secret=c4 enabled=1 data=c4
CHECK secret=c5 enabled=0 data=00
CHECK secret=c5 enabled=1 data=c5
CHECK secret=c6 enabled=0 data=00
CHECK secret=c6 enabled=1 data=c6
CHECK secret=c7 enabled=0 data=00
CHECK secret=c7 enabled=1 data=c7
CHECK secret=c8 enabled=0 data=00
CHECK secret=c8 enabled=1 data=c8
CHECK secret=c9 enabled=0 data=00
CHECK secret=c9 enabled=1 data=c9
CHECK secret=ca enabled=0 data=00
CHECK secret=ca enabled=1 data=ca
CHECK secret=cb enabled=0 data=00
CHECK secret=cb enabled=1 data=cb
CHECK secret=cc enabled=0 data=00
CHECK secret=cc enabled=1 data=cc
CHECK secret=cd enabled=0 data=00
CHECK secret=cd enabled=1 data=cd
CHECK secret=ce enabled=0 data=00
CHECK secret=ce enabled=1 data=ce
CHECK secret=cf enabled=0 data=00
CHECK secret=cf enabled=1 data=cf
CHECK secret=d0 enabled=0 data=00
CHECK secret=d0 enabled=1 data=d0
CHECK secret=d1 enabled=0 data=00
CHECK secret=d1 enabled=1 data=d1
CHECK secret=d2 enabled=0 data=00
CHECK secret=d2 enabled=1 data=d2
CHECK secret=d3 enabled=0 data=00
CHECK secret=d3 enabled=1 data=d3
CHECK secret=d4 enabled=0 data=00
CHECK secret=d4 enabled=1 data=d4
CHECK secret=d5 enabled=0 data=00
CHECK secret=d5 enabled=1 data=d5
CHECK secret=d6 enabled=0 data=00
CHECK secret=d6 enabled=1 data=d6
CHECK secret=d7 enabled=0 data=00
CHECK secret=d7 enabled=1 data=d7
CHECK secret=d8 enabled=0 data=00
CHECK secret=d8 enabled=1 data=d8
CHECK secret=d9 enabled=0 data=00
CHECK secret=d9 enabled=1 data=d9
CHECK secret=da enabled=0 data=00
CHECK secret=da enabled=1 data=da
CHECK secret=db enabled=0 data=00
CHECK secret=db enabled=1 data=db
CHECK secret=dc enabled=0 data=00
CHECK secret=dc enabled=1 data=dc
CHECK secret=dd enabled=0 data=00
CHECK secret=dd enabled=1 data=dd
CHECK secret=de enabled=0 data=00
CHECK secret=de enabled=1 data=de
CHECK secret=df enabled=0 data=00
CHECK secret=df enabled=1 data=df
CHECK secret=e0 enabled=0 data=00
CHECK secret=e0 enabled=1 data=e0
CHECK secret=e1 enabled=0 data=00
CHECK secret=e1 enabled=1 data=e1
CHECK secret=e2 enabled=0 data=00
CHECK secret=e2 enabled=1 data=e2
CHECK secret=e3 enabled=0 data=00
CHECK secret=e3 enabled=1 data=e3
CHECK secret=e4 enabled=0 data=00
CHECK secret=e4 enabled=1 data=e4
CHECK secret=e5 enabled=0 data=00
CHECK secret=e5 enabled=1 data=e5
CHECK secret=e6 enabled=0 data=00
CHECK secret=e6 enabled=1 data=e6
CHECK secret=e7 enabled=0 data=00
CHECK secret=e7 enabled=1 data=e7
CHECK secret=e8 enabled=0 data=00
CHECK secret=e8 enabled=1 data=e8
CHECK secret=e9 enabled=0 data=00
CHECK secret=e9 enabled=1 data=e9
CHECK secret=ea enabled=0 data=00
CHECK secret=ea enabled=1 data=ea
CHECK secret=eb enabled=0 data=00
CHECK secret=eb enabled=1 data=eb
CHECK secret=ec enabled=0 data=00
CHECK secret=ec enabled=1 data=ec
CHECK secret=ed enabled=0 data=00
CHECK secret=ed enabled=1 data=ed
CHECK secret=ee enabled=0 data=00
CHECK secret=ee enabled=1 data=ee
CHECK secret=ef enabled=0 data=00
CHECK secret=ef enabled=1 data=ef
CHECK secret=f0 enabled=0 data=00
CHECK secret=f0 enabled=1 data=f0
CHECK secret=f1 enabled=0 data=00
CHECK secret=f1 enabled=1 data=f1
CHECK secret=f2 enabled=0 data=00
CHECK secret=f2 enabled=1 data=f2
CHECK secret=f3 enabled=0 data=00
CHECK secret=f3 enabled=1 data=f3
CHECK secret=f4 enabled=0 data=00
CHECK secret=f4 enabled=1 data=f4
CHECK secret=f5 enabled=0 data=00
CHECK secret=f5 enabled=1 data=f5
CHECK secret=f6 enabled=0 data=00
CHECK secret=f6 enabled=1 data=f6
CHECK secret=f7 enabled=0 data=00
CHECK secret=f7 enabled=1 data=f7
CHECK secret=f8 enabled=0 data=00
CHECK secret=f8 enabled=1 data=f8
CHECK secret=f9 enabled=0 data=00
CHECK secret=f9 enabled=1 data=f9
CHECK secret=fa enabled=0 data=00
CHECK secret=fa enabled=1 data=fa
CHECK secret=fb enabled=0 data=00
CHECK secret=fb enabled=1 data=fb
CHECK secret=fc enabled=0 data=00
CHECK secret=fc enabled=1 data=fc
CHECK secret=fd enabled=0 data=00
CHECK secret=fd enabled=1 data=fd
CHECK secret=fe enabled=0 data=00
CHECK secret=fe enabled=1 data=fe
CHECK secret=ff enabled=0 data=00
CHECK secret=ff enabled=1 data=ff
SECURITY_TEST_PASS
```

Observed: `property_held_for_test`; expected: `property_held_for_test`; evidence passed: `True`; strict result: `True`.

## case_10 / trial 1

Enabled output equals protected data. Disabled output is zero for every protected byte.

1. Staged and SHA-256 hashed design and testbench.
3. Called `compile_rtl` with `{"sources": [".llm4security-suite/security-v1/case_10/design.sv", ".llm4security-suite/security-v1/case_10/tb.sv"], "top": "tb"}`.
   Run `64e47015292246a095a9fb1d7a1803f6`; exit `0`; timeout `False`.
5. Called `simulate` with `{"run_id": "64e47015292246a095a9fb1d7a1803f6"}`.
   Run `67538dd47f98454c8b0371f29df8edaf`; exit `1`; timeout `False`.

```text
CHECK secret=00 enabled=0 data=00
CHECK secret=00 enabled=1 data=00
CHECK secret=01 enabled=0 data=01
FATAL: /inputs/sources/.llm4security-suite/security-v1/case_10/tb.sv:14: SECURITY_VIOLATION: disabled output leaks data
```

Observed: `property_violated`; expected: `property_violated`; evidence passed: `True`; strict result: `True`.
