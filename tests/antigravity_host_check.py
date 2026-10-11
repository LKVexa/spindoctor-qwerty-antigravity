#!/usr/bin/env python3
# SpinDoctor Qwerty 1.1.0 - Antigravity stand-in host
# Copyright (C) 2026 RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. It is distributed WITHOUT ANY WARRANTY; see the LICENSE file for details.
"""Antigravity stand-in host check (no Antigravity needed): validates plugin.json against the schema printed in the
Antigravity plugin docs, checks mcp_config.json, skills, agents and rules, confirms there are no hooks, then starts the
MCP server exactly as mcp_config.json declares it (command + args, cwd = plugin root) and runs tests/e2e_mcp.py
through it.  Standard library only (Python 3.8+).

usage: python3 tests/antigravity_host_check.py [PLUGIN_DIR]   (default: the repository root)"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ALLOWED_SERVER_KEYS = {"command", "args", "env", "cwd", "serverUrl", "headers", "authProviderType", "oauth", "disabled", "disabledTools", "timeout"}


def frontmatter(path):
    m = re.match(r"^---\n(.*?)\n---\n", open(path, encoding="utf-8").read(), re.S)
    return dict(re.findall(r"^([A-Za-z_-]+):\s*(.+)$", m.group(1), re.M)) if m else {}


def main():
    root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(HERE)
    ok = True

    def T(name, cond, detail=""):
        nonlocal ok
        ok = ok and bool(cond); print(("PASS " if cond else "FAIL ") + name + ("" if cond else "  -- " + str(detail)))

    pj = json.load(open(os.path.join(root, "plugin.json"), encoding="utf-8"))
    T("plugin.json: required name matching ^[a-zA-Z0-9-_]+$", isinstance(pj.get("name"), str) and re.match(r"^[a-zA-Z0-9-_]+$", pj["name"]), pj.get("name"))
    T("plugin.json: no properties beyond $schema/name/description (additionalProperties false)", set(pj) <= {"$schema", "name", "description"}, sorted(pj))
    mc = json.load(open(os.path.join(root, "mcp_config.json"), encoding="utf-8"))
    srv = mc.get("mcpServers", {}).get("spindoctor-qwerty", {})
    T("mcp_config.json: mcpServers.spindoctor-qwerty with documented stdio keys", srv.get("command") and isinstance(srv.get("args"), list) and set(srv) <= ALLOWED_SERVER_KEYS, srv)
    skills = [d for d in os.listdir(os.path.join(root, "skills")) if os.path.isfile(os.path.join(root, "skills", d, "SKILL.md"))]
    T("skills/<name>/SKILL.md with frontmatter name = folder name and a description", skills and all(frontmatter(os.path.join(root, "skills", d, "SKILL.md")).get("name") == d and frontmatter(os.path.join(root, "skills", d, "SKILL.md")).get("description") for d in skills), skills)
    agents = [f for f in os.listdir(os.path.join(root, "agents")) if f.endswith(".md")]
    T("agents/*.md with name and description", agents and all(frontmatter(os.path.join(root, "agents", f)).get("name") == f[:-3] and frontmatter(os.path.join(root, "agents", f)).get("description") for f in agents), agents)
    T("rules/*.md present", any(f.endswith(".md") for f in os.listdir(os.path.join(root, "rules"))))
    T("no hooks (hooks.json absent or empty)", not os.path.exists(os.path.join(root, "hooks.json")) or json.load(open(os.path.join(root, "hooks.json"))) == {})
    cwd = os.path.normpath(os.path.join(root, srv.get("cwd", ".")))
    cmd = [os.environ.get("SPINDOCTOR_PYTHON") or srv["command"]] + srv["args"]
    env = dict(os.environ, **srv.get("env", {}))
    examples = os.path.join(root, "skills", "spindoctor-qwerty", "examples", "theory")
    r = subprocess.run([sys.executable, os.path.join(HERE, "e2e_mcp.py"), "--server"] + cmd + ["--examples", examples, "--out", os.path.join(HERE, "e2e_results.json")], cwd=cwd, env=env)
    T("end-to-end test through the server declared in mcp_config.json", r.returncode == 0)
    print("HOST-CHECK", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
