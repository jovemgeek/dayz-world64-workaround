# Native capacity trace

All addresses below refer only to the original Windows x64 server SHA-256 recorded in the README. Virtual addresses use the preferred image base and are not guaranteed runtime addresses under ASLR.

## Method

We inspected PE metadata and bounded x64 disassembly using pefile 2024.8.26 and Capstone 5.0.6, followed by controlled native executions. No claim is made that these tools recovered the original C++ source. PE unwind entries can split logical functions; function boundaries and labels should be treated as analysis descriptions.

## Argument and allocator

1. Module initializer around `0x140A4EAC0` supplies a fifth argument to `0x140239370`. The World argument instruction is at `0x140A4F32D`, file offset `0xA4E72D`.
2. `0x1402393B1` reads the argument and `0x1402393B4` stores it at module descriptor offset `+0x48`.
3. In the compiler path around `0x1402399F0`, `0x140239C1C` loads that descriptor field and forwards it to `0x140243DB0`.
4. At `0x140243DFA`, capacity is passed in EDX to allocator construction at `0x14039FC60`.
5. That constructor requests the capacity through `0x14020CAF0`, clears the region, and establishes base (`+0x20`), cursor (`+0x10`), uint32 capacity (`+0x28`) and end (`+0x18`) fields.
6. The logging path near `0x140239ED5`, through compiled-module offset `+0x78`, divides used bytes and capacity by 1,000 for its printed kB values.

Observed guards near `0x14024FF0F`, `0x140250C4B` and `0x1402573B2` check remaining capacity against 4,096 bytes and lead to the static-buffer error. These instructions are unchanged. The patch increases the allocation argument; it does not merely silence an error or skip a bounds check.

| Module | Instruction file offset | Original capacity | Public patch |
| --- | --- | --- | --- |
| GameLib | 0xA4E662 | 2 MiB | Unchanged |
| Game | 0xA4E6C8 | 32 MiB | Unchanged |
| World | 0xA4E72D | 32 MiB | 64 MiB |
| Mission | 0xA4E78E | 32 MiB | Unchanged |

These four capacities sum to 98 MiB; this excludes Core and unrelated allocations and is not a shared budget. Independent retail-client and diagnostic inspections found corresponding capacities, but neither executable is modified or supported by this patcher.

## A/B workload design

The historical fixture generated 140,000 constant-returning methods in 1,094 classes, with up to 128 methods per class. Every return value was checked. Nine verification helpers split class checks into groups (eight groups of 128 and one of 70) to avoid a separate per-function instruction limit. The same 38-entry PBO was used in both runs; its timestamps were normalized for deterministic packing.

Both runs used early World initialization and the same `-no_preload_vehicles` option. Installed game data was referenced identically; this is not a claim of a pristine vanilla environment. The original hit the World static buffer limit. The candidate ran all checks above that limit, printed success markers, and requested exit before full mission initialization.

Raw private deployment logs and game files are deliberately excluded. The sanitized record preserves binary/workload hashes, scope and results. The historical synthetic PBO and its private harness are not included; that record is evidence of a past experiment, not a claim that this repository contains a fully reproducible gameplay test suite. The executable transformation itself is reproducible using the supported original input.

## What remains unproven

The trace and successful workload do not prove all engine references, VM encodings or late gameplay paths support the larger region. Full-mission initialization, realistic sustained population, mod interactions, saves/reloads and security-system compatibility require separate validation. Initial full-mission controls did not complete within their timeout; their cause was not established, and they are not counted as successful validation.

Any future game build needs fresh instruction/data-flow analysis and native tests. Matching a byte pattern alone is insufficient justification to patch another build.
