# Project Memory

Most projects with AI tooling ship an `AGENTS.md` -- always-on rules
for agents. This template adds something rarer: an AI-maintained
knowledge layer that travels with the project's Git repo. The agent
keeps a curated operational state, optional identity and vision, and
a `materials/` namespace of working notes. The next agent on any
clone, on any machine, picks up where the last one left off.

Compatible with Cursor (3.2.1+), Claude Code, and Codex (CLI and app)
out of the box. No per-tool configuration.

## How to use

1. Copy this folder to your project location (or `git clone` it).
2. Delete `.git/` if you cloned.
3. Delete this `README.md`.
4. Open the folder in your AI tool of choice and tell the agent
   what you want to do -- e.g. "let's start this project, it'll be
   about ...". The template-default banners in `_knowledge/STATE.md`
   and `_knowledge/materials/OVERVIEW.md` will steer it toward
   capturing what the project is about and replacing them with real
   content.

That is it. No install step, no service, no per-tool configuration.

## Custom project rules (AGENTS.md, CLAUDE.md)

Whether your tool reads `AGENTS.md` (Cursor, Codex CLI / IDE) or
`CLAUDE.md` (Claude Code), the template generates both files from
the same source fragments under `_agent-rules/`. If you want to add
project-specific or team-specific agent rules on top of the
template's defaults, do not edit `AGENTS.md` or `CLAUDE.md`
directly -- edit the source fragments and regenerate.

The template's rules ship in `_agent-rules/50-project-memory-core.md`.
Add your own fragments alongside: e.g. `40-team.md` for team
conventions, `60-project.md` for project rules. The numeric prefix
sets composition order (lower comes first). A placeholder ships as
`_agent-rules/70-project.example.md`; copy it to a real name and
edit.

Regenerate both files:

```powershell
python _agent-rules/compose.py
```

`AGENTS.md` is the rules file Codex-compatible tools read. `CLAUDE.md`
is a one-line shim (`@AGENTS.md`) so Claude Code reads the same
content. The composer refuses to overwrite `AGENTS.md` if it detects
changes it did not write, so a hand-edit (yours or an agent's) is
not silently clobbered. Copy any such changes into `_agent-rules/*.md`
and re-run, or pass `--force` to overwrite. Check for stale output:

```powershell
python _agent-rules/compose.py --check
```

## What you'll observe

After the first session, the agent maintains:

* `_knowledge/STATE.md` -- the project's operational state. Rewritten
  as understanding matures, never just appended. Starts with a Hot
  List of the most important facts and priorities right now.
* `_knowledge/materials/` -- session summaries, exploration notes,
  context notes, and durable knowledge artifacts. Messy by design.
* `_knowledge/materials/INDEX.md` -- keyword index of working files.
  Updated whenever materials change.
* `_knowledge/materials/OVERVIEW.md` -- one-paragraph external-facing
  description of what the project knows.

Optional, introduced when the project earns them:

* `_knowledge/IDENTITY.md` -- the project's worldview, architectural
  commitments, posture.
* `_knowledge/VISION.md` -- long-term ambitions, reframes, moon
  shots.
* `_knowledge/archive/` -- consumed materials whose insights have
  been absorbed into the curated layer.

`_knowledge/check.py` is a small advisory script that flags
bootstrap state issues and `INDEX.md` drift. Run
`python3 _knowledge/check.py` when you suspect bookkeeping drift or
as a pre-commit sanity check.

You can drive maintenance explicitly when useful -- "consolidate
these materials into STATE.md", "audit state", "wrap up the session
and summarize what changed" -- but most of it happens without
prompting.

## What this enables

* Knowledge survives across chats, machines, contributors, and tool
  changes. It travels with the repo. The next session is never the
  first session.
* External agents and MCP servers can discover the project via
  `_knowledge/materials/OVERVIEW.md`, the project's external-facing
  announcement of what it knows. Whether to also serve any of the
  underlying materials files outside the project (e.g. via an MCP)
  is a separate, opt-in decision the project makes when it has
  decided what is safe to expose.
* A new contributor (or a fresh agent) cloning the repo gets the
  code AND the story behind it. Reasoning is no longer reconstructed
  from chat history that lives somewhere else.

## Design rationale

Design decisions, alternatives considered, and the changelog of
breaking changes live in the separate meta repo *project-memory-meta*. 
Read it when extending the template, migrating an existing project to a
newer template version, or just curious about the why.
