# SpinDoctor Qwerty for Google Antigravity

**spindoctor-qwerty-antigravity** is a [Google Antigravity](https://antigravity.google) plugin (Antigravity 2.0, Antigravity CLI and
Antigravity IDE). It bundles the SpinDoctor Qwerty quantum-circuit **simulator** as an MCP server, a skill, a helper subagent and an
honesty rule. The agent can then build and run circuits with SpinDoctor's `q.*` commands, run any of the 241 presets, process a folder
of command files with `q.folder`, test a theory you give it, and write TXT, PDF, JSON and CSV reports.

- Version **1.1.0**, engine at **SpinDoctor 3.1.2 parity** (update 3.1.2-298-20261010).
- Host: **Antigravity plugin**. This repository root is the plugin: `plugin.json`, `mcp_config.json`,
  `skills/spindoctor-qwerty/` (skill + bundled engine), `agents/qwerty-helper.md`, `rules/spindoctor-honesty.md`. There are no hooks.
- Self-contained: the engine (pure Python, standard library only, NumPy optional) lives in `skills/spindoctor-qwerty/`. No network
  access, no installs.

> **Honest limits.** SpinDoctor runs classical FP64 arithmetic on your computer. It is **not** a quantum computer, never contacts
> quantum hardware, and gives no quantum speed-up or quantum advantage. Registers hold 1-298 logical qubits, but any group of
> entangled qubits (one "factor") is limited to 59 qubits, and dense factors are limited much further by memory
> (2^n x 16 bytes; about 22 qubits with the standard library, more with NumPy). Registers wider than 29 qubits sample in basis Z only.
> Python 3.8 or newer is required (`python3` on PATH).

## Install

1. Install **Python 3.8+** and make sure `python3` runs it.
2. Install the plugin:
   - **Antigravity CLI:** `agy plugin install https://github.com/LKVexa/spindoctor-qwerty-antigravity`. You can also clone the repository
     and run `agy plugin install ./spindoctor-qwerty-antigravity`. Check with `agy plugin list` and `agy agents`.
   - **Antigravity 2.0 / IDE (manual):** copy this repository folder to `<workspace>/.agents/plugins/spindoctor-qwerty/` (one project)
     or `~/.gemini/config/plugins/spindoctor-qwerty/` (all workspaces).
3. Open the Customizations panel (or `/plugin` in the CLI) to see the skill, agent and MCP server. Then ask: *"show the SpinDoctor
   functions"*.

**If the MCP server does not start.** `mcp_config.json` starts `python3 ./skills/spindoctor-qwerty/scripts/spindoctor_mcp.py` with
`cwd` set to the plugin folder. The Antigravity docs do not document a plugin-root variable for MCP paths. If your surface starts the
server from a different folder, add the server to `.agents/mcp_config.json` (workspace) or `~/.gemini/config/mcp_config.json`
(global) with an absolute path:

```json
{ "mcpServers": { "spindoctor-qwerty": { "command": "python3", "args": ["/absolute/path/to/spindoctor-qwerty/skills/spindoctor-qwerty/scripts/spindoctor_mcp.py"] } } }
```

On Windows use `"command": "python"` if `python3` is not available. Set `SPINDOCTOR_WORKSPACE` in `env` to choose where reports go
(default `~/spindoctor-workspace`).

**Sample theory PDFs.** `skills/spindoctor-qwerty/examples/theory/` holds sample theory files and chat transcripts. The two sample PDFs
are stored as text; run `python3 skills/spindoctor-qwerty/examples/theory/make_sample_pdfs.py` to recreate them.

## What you can ask for

## SpinDoctor Qwerty - plugin tools

| Function | What it does | Command to type |
|---|---|---|
| Function table (spindoctor_functions) | Show this table in chat | Ask: "show the SpinDoctor functions" (CLI: `spindoctor_cli.py functions`) |
| Run a script (spindoctor_run_script) | Run any q.* lines above; returns results + TXT/JSON/CSV/PDF report paths | Ask: "run q.circuit new bell 2 / q.circuit add h 0 / ..." |
| Run a preset (spindoctor_run_preset) | Run qc-001..qc-241 with overrides | Ask: "run preset qc-067 with shots=64" |
| List presets (spindoctor_list_presets) | Search the 241 presets | Ask: "list presets about Grover" |
| Read a report (spindoctor_report) | List/read TXT reports (PDF/JSON paths alongside) | Ask: "show the newest SpinDoctor report" |
| Test a theory from a file (spindoctor_test_theory source=file) | Read a .txt/.md/.pdf/.py/.json/.csv/.q attachment, then hypothesis -> prediction -> q.* script -> run -> verdict + TXT/PDF theory report | Ask: "test the theory in C:/notes/theory.md" (the host must pass the file path/content) |
| Test a theory from text (spindoctor_test_theory source=text) | Same pipeline for pasted text | Ask: "test this theory: a Hadamard on \|0> gives 50/50" |
| Test the theory we discussed (spindoctor_test_theory source=chat) | The AI summarises the theory from the conversation (claims, assumptions, variables, prediction), you confirm, then it is tested; quoted excerpts go in the report under 'Source: chat history'. An exported chat transcript (.txt/.md/.json/.html) also works | Ask: "test the theory we discussed" or "test the theory in my exported chat C:/chats/conversation.json" |

Every command family is listed with a runnable example in **[FUNCTIONS.md](FUNCTIONS.md)** (the exact table the tool shows):
circuits (`q.circuit`, including 298-qubit wide registers and the `mcx7` gate), queries (`q.query`), the tranche register
(`q.tranche`), the procedural grid, presets and sequences, resource planning, math calculators, physics models, lessons, noise, error
correction, compilation, algorithms, inputs/folders/history (`q.input`, `q.folder`, `q.history`) and the cartridge commands.

## Theory testing

`spindoctor_test_theory` turns a claim into a test: hypothesis -> measurable prediction -> `q.*` script -> run -> compare -> a TXT +
JSON + PDF **theory test report** with the hypothesis, script, raw results, verdict (*supported*, *not supported* or *inconclusive*)
and limits.

- **From a file:** .txt, .md, .pdf, .py, .json, .csv or .q. In Antigravity, give the file's path in the workspace.
- **From pasted text.**
- **From the chat history:** say *"test the theory we discussed"*. The agent writes a short summary (claims, assumptions, variables,
  measurable prediction), shows it to you to confirm or correct, then passes it with optional quoted excerpts; the report records them
  under *Source: chat history*. Exported chat transcripts (.txt/.md/.json/.html from ChatGPT, Claude and others) also work.
- The plugin cannot read your conversation or attachments by itself: only the agent sees them, and very long conversations may already
  be truncated by the context window.

## Folder ingestion (`q.folder`)

`q.folder run path="<folder>"` runs every supported file at the top level of a folder (.txt, .csv, .json, .qasm, .qasm2, .circuit,
.pdf) in ordinal name order: 1-128 supported files, at most 4 MiB per file, 1-128 commands per file and 4096 characters per command,
strict UTF-8. Other files (for example .md) are skipped and listed. The first failing file stops the job.

## Testing

| Test | Command | Result for 1.1.0 |
|---|---|---|
| Real Antigravity CLI 1.3.3 validation | `agy plugin validate .` | ok (1 skill, 1 agent, 1 MCP server, no hooks) |
| Real Antigravity CLI install + load | `agy plugin install <folder>`, `agy plugin list`, `agy agents` | installed; `qwerty-helper` agent listed |
| Stand-in host + end-to-end | `python3 tests/antigravity_host_check.py` | 8/8 host checks, end-to-end 12/12 |

**host-simulated (MCP tools):** the real Antigravity CLI was installed for free and used without signing in. It validates, installs and
loads the plugin, and lists its agent. Listing MCP tools needs a signed-in agent session, which was not used, so the MCP server was driven
by the stand-in host `tests/antigravity_host_check.py`. It starts the server exactly as `mcp_config.json` declares it. Details in
[E2E_RESULTS.md](E2E_RESULTS.md).

## Author and license

Author: **RUSSELL PHILIP SMITHSON** <russellsmithson77@outlook.com>

Copyright (C) 2026 RUSSELL PHILIP SMITHSON. Licensed under the GNU General Public License v3.0 or later
(`GPL-3.0-or-later`): see [LICENSE](LICENSE), [NOTICE](NOTICE) and [COPYRIGHT](COPYRIGHT). The Antigravity `plugin.json` schema allows
only `name` and `description` (`additionalProperties: false`), so the license and author are stated in its description, the skill
and these files rather than in separate manifest fields.
