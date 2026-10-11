# End-to-end results - spindoctor-qwerty-antigravity 1.1.0

Date: 2026-10-10 (PT). Engine: SpinDoctor Qwerty 1.1.0, SpinDoctor 3.1.2 parity (update 3.1.2-298-20261010).

## Publishing decision (recorded as required)

RUSSELL PHILIP SMITHSON approved publishing ("GO") on the basis that the **updated SpinDoctor 3.1.2** builds and passes its own test
suite **18/18**, with the three test checks that still assumed the old 29-qubit limit adapted to the new 298-qubit limit
(`engine_regressions` dense comparison restricted to gates with at most 3 operands now that `mcx7` has 8; `direct_preset_regressions`
and `csv_gate_regressions` now expect 299 qubits, not 30, to be refused). Unmodified, the update passes 15/18 because of exactly
those three stale checks.

## Reference used

All parity comparisons use reference outputs regenerated from the **updated** SpinDoctor 3.1.2 C# build (241 presets in one
session, the folder-ingest chug series, and direct wide-register commands).

## Shared engine (Phase A, run once for all repos)

| Suite | Result |
|---|---|
| 241 presets replayed against the updated 3.1.2 reference | 236 identical; 5 with documented differences (qc-006, qc-008, qc-009, qc-016, qc-019: OpenCL GPU fields absent in a CPU-only engine, tranche checkpoint wording, session-state file name). qc-198 fails preflight in both C# and the engine (`q.compile synthesize` is not implemented in SpinDoctor 3.1.2 either). Work-accounting counters are compared separately and documented. |
| Folder-ingest chug series (41 folders) | 40 pass; `08_cancel` not applicable (the engine runs `q.folder` synchronously, so there is nothing to cancel; the job completes correctly) |
| Wide-register parity (direct 298-qubit commands) | 0 differences |
| 11-file 298-qubit example folder | identical (73 distinct outcomes, histogram preview and counts match) |
| Engine validation suite | 22/22 |
| Theory-testing suite (files, text, chat summary, 5 transcript formats) | 43/43 |
| Function-table examples (every "Command to type") | 168/168 run OK |

## This repository: clean-room test

The staged repository was copied into a fresh, empty folder with an empty HOME (no access to engine development folders or tools).
The README steps were followed exactly: the plugin was installed with the real Antigravity CLI, and the stand-in host was then run
**from the installed copy** (`~/.gemini/config/plugins/spindoctor-qwerty/`), using a minimal environment (`env -i`, Python standard
library only).

| Check (through the MCP server declared in `mcp_config.json`, cwd = plugin root) | Result |
|---|---|
| plugin.json matches the documented schema (name pattern, no extra properties) | PASS |
| mcp_config.json uses documented stdio keys; skill, agent and rule frontmatter valid; no hooks | PASS |
| MCP initialize + tools/list (6 tools) | PASS |
| Function table shown (`spindoctor_functions`) | PASS |
| One script per command family (every family in the function table) | PASS |
| Preset run (`qc-001`) and presets qc-001..qc-025 compared with the updated-3.1.2 reference (seeded) | PASS |
| `q.folder` on a small mixed folder (.txt/.csv/.json/.qasm, .md skipped and listed) | PASS |
| Theory test from a file and from a chat summary + transcript | PASS |
| TXT + PDF reports generated; PDFs validated (header, xref, trailer, EOF) | PASS |
| Summary | host checks 8/8, end-to-end 12/12 |

## Host app

| Item | Result |
|---|---|
| Antigravity CLI | Real `agy` 1.3.3, installed for free with the official installer into an isolated HOME. **No sign-in, no API key.** |
| `agy plugin validate .` | ok: 1 skill, 1 agent, 1 MCP server, no hooks |
| `agy plugin install <folder>` / `agy plugin list` | installed to `~/.gemini/config/plugins/spindoctor-qwerty/`; components skills, agents, mcpServers |
| `agy agents` | lists `qwerty-helper` (the plugin's subagent is loaded) |
| MCP tool listing | **host-simulated**: listing or calling MCP tools needs a signed-in agent session, which was not used. The stand-in host `tests/antigravity_host_check.py` starts the server exactly as `mcp_config.json` declares it. |

## Post-push verification

After the push (content commit `ffaf887`), the public repository was cloned back from GitHub into a fresh folder with an empty HOME:

| Check | Result |
|---|---|
| Cloned tree vs staged tree | 51/51 files present, byte-identical, no extra files |
| `agy plugin validate .` on the clone | ok |
| `agy plugin install <clone>` + `agy agents` | installed; `qwerty-helper` listed |
| Stand-in host check from the installed clone | host checks 8/8, end-to-end 12/12 (PASS) |

Commits are made through the GitHub connector and show the LKVexa account as committer. The author of the work is
RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com> (see NOTICE and COPYRIGHT).
