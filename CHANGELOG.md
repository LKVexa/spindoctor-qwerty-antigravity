# Changelog

## 1.1.0 (2026-10-10)

- Engine rebased on **SpinDoctor 3.1.2** (update 3.1.2-298-20261010): 1-298 logical qubits with 59-qubit entangled factors,
  prepared-factor Born-Z sampling above 29 qubits, the `mcx7` gate, wide basis indices, `q.folder` with 3.1.2 semantics,
  CSV report copies and measurement-CSV fitting equations. 241 presets replayed against the updated 3.1.2 reference.
- New tools: `spindoctor_functions` (in-chat function table) and `spindoctor_test_theory` (file, pasted text, chat history,
  exported chat transcripts).
- Antigravity plugin: repository root is now the plugin, so `agy plugin install https://github.com/LKVexa/spindoctor-qwerty-antigravity`
  works (the Antigravity CLI installs from GitHub URLs). Empty `hooks.json` removed (no hooks). Skill, agent and rule updated
  from 3.0.3 / "1..29 qubits" to the 3.1.2 limits; skill license MIT -> GPL-3.0-or-later; MCP server gets `PYTHONUTF8`; README
  documents an absolute-path fallback, because the docs define no plugin-root variable for MCP paths.
- Validated with the real Antigravity CLI 1.3.3 (`agy plugin validate`, `install`, `list`, `agents`).
- Optional reproducibility: `SPINDOCTOR_MEASUREMENT_SEED` / `SPINDOCTOR_FIELD_SEED` (64 hex characters) seed a new workspace.

## 1.0.0

- First release (SpinDoctor 3.0.3 semantics).
