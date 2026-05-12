# Project Knowledge Base

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
4. Open the folder in your AI tool of choice and start a chat. The
   agent will see the template-default banners in
   `_knowledge/STATE.md` and `_knowledge/materials/OVERVIEW.md`, ask
   what your project is about, and replace them with real content.

That is it. No setup script, no configuration.

## What you'll observe

After the first session, the agent maintains:

* `_knowledge/STATE.md` -- the project's operational state. Rewritten
  as understanding matures, never just appended. Starts with a Hot
  List of the most important facts and priorities right now.
* `_knowledge/materials/` -- session summaries, exploration notes,
  durable knowledge artifacts, handoffs for future agents. Messy by
  design.
* `_knowledge/materials/INDEX.md` -- keyword index of working files.
  Updated whenever materials change.
* `_knowledge/materials/OVERVIEW.md` -- one-paragraph external-facing
  description of what the project knows.

Optional, introduced when the project earns them:

* `_knowledge/IDENTITY.md` -- the project's worldview, architectural
  commitments, posture.
* `_knowledge/VISION.md` -- long-term ambitions, reframes, moon
  shots.
* `_knowledge/archive/` and `_knowledge/attic/` -- consumed and
  parked materials.

`AGENTS.md` at the repo root holds the canonical always-on rules.
`CLAUDE.md` is a one-line shim that points Claude Code at
`AGENTS.md`; you do not need to edit it.

`_knowledge/check.py` is a small advisory script that flags
bootstrap state issues and `INDEX.md` drift. Run
`python3 _knowledge/check.py` when you suspect bookkeeping drift or
as a pre-commit sanity check.

You can drive maintenance explicitly when useful -- "consolidate
these materials into STATE.md", "audit state", "wrap up the session
and write a handoff" -- but most of it happens without prompting.

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
breaking changes live in the separate meta repo:
[project-knowledge-base-meta](../project-knowledge-base-meta). Read
it when extending the template, migrating an existing project to a
newer template version, or just curious about the why.
