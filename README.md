# Project Knowledge Base

Most projects with AI tooling ship an `AGENTS.md` file -- rules for
agents to follow. This template adds something rarer: a self-organizing
knowledge layer for the project itself (curated state, optional tiered
worldview, materials, keyword index), kept in the project's own
Git repo alongside the code. What was learned, decided, and tried
survives across chats, machines, and future contributors.

![Demo: an off-hand statement becomes a materials note in the project's knowledge layer.](_template-docs/images/demo-capture.png)

*An off-hand statement becomes a materials note. Future chats find it
without anyone having to remember it was said.*

![Demo: a reasonable-sounding design proposal meets the project's accumulated context, and the agent flags conflicts from materials and identity before any code is written.](_template-docs/images/demo-pushback.png)

*A reasonable-sounding proposal meets the project's accumulated
context. The agent flags conflicts from materials and identity
before any code is written.*

Copy this folder into a project to start. Compatible with Cursor, Claude Code, and Codex App and CLI.

> [!TIP]
> TLDR: copy this folder, feel free to delete `README.md` and the
> `_template-docs/` folder, open an AI chat, and tell the agent what
> you want to work on. That's it. The first agent will likely offer to
> bootstrap `_knowledge/STATE.md` and ask what it needs to know; let it.
> The structure described below grows from there naturally.
> You can stop reading at this point and still use the template competently -- 
> the rest of this README is for when you want to understand the design.


## Contents

- [Project Knowledge Base](#project-knowledge-base)
  - [Contents](#contents)
  - [The Problem This Solves](#the-problem-this-solves)
  - [Core Concepts](#core-concepts)
  - [Setting Up a New Workspace](#setting-up-a-new-workspace)
  - [Day-to-Day Workflow](#day-to-day-workflow)
  - [Beyond STATE.md: Identity and Vision](#beyond-statemd-identity-and-vision)
  - [What Goes Where](#what-goes-where)
  - [Relationship to Karpathy's "LLM Wiki" Pattern](#relationship-to-karpathys-llm-wiki-pattern)
    - [What we share](#what-we-share)
    - [Where we differ](#where-we-differ)
    - [What we deliberately left out](#what-we-deliberately-left-out)
    - [If you outgrow this template](#if-you-outgrow-this-template)
  - [Design Principles](#design-principles)
    - [Artifact-forward root, meta in `_knowledge/`](#artifact-forward-root-meta-in-_knowledge)
    - [Structure over procedure](#structure-over-procedure)
    - [Bounded curated layer](#bounded-curated-layer)
    - [Knowledge persistence across sessions](#knowledge-persistence-across-sessions)
    - [The AI is a maintainer, not a retriever](#the-ai-is-a-maintainer-not-a-retriever)
    - [Tool compatibility](#tool-compatibility)
  - [Tips](#tips)


## The Problem This Solves

When working with AI on longer efforts -- code analysis, debugging,
design exploration, research -- understanding accumulates in chat
sessions and scattered markdown files. There are two ways it gets
lost.

Across chats: sessions hit context limits and get abandoned. Files
become redundant or contradictory as understanding evolves. You feel
the urge to start from scratch but are afraid of losing buried
insights.

Across the project / code split: when code lives in a versioned repo
(GitLab, GitHub) but the meta -- motivating ideas, requirements,
alternatives explored, the reasoning behind decisions -- lives in a
personal OneDrive folder or scattered notes, that meta gets stranded
the moment the code becomes the authoritative checkout. A new
contributor cloning the repo gets the code with no story. An agent
starting fresh in a clone gets no context. Reasoning is reconstructed
from scratch -- or, more often, abandoned.

This template addresses both. It separates raw exploration from
curated understanding (so you can work messily without losing
clarity), and stores both alongside the code in the same Git repo
(so what was learned travels with the project rather than living in
a separate workspace that gets forgotten or stranded). The repo
root stays artifact-forward; the meta sits one level in, under
`_knowledge/`.


## Core Concepts

There are two kinds of material in this workspace:

* Materials (`_knowledge/materials/`) -- the messy, temporal record of
  exploration. Chat dumps, notes, half-formed ideas, dead ends, session
  summaries, handoffs for future agents. These are expected to be
  redundant, contradictory, and incomplete. They are raw material.
  Their primary function is preserving knowledge across short-lived
  agent sessions; err on the side of dumping -- lost knowledge costs
  more than a messy file. See "Knowledge persistence across sessions"
  under Design Principles for the rationale.

* The state document (`_knowledge/STATE.md`) -- your single, clean,
  current-state summary. This is what you would hand someone to get
  them up to speed. It is rewritten as understanding matures, not
  appended to. Stale information is overwritten, not preserved
  alongside new information. It always starts with a "Hot List" (max
  5 bullets, each terse -- a headline plus pointers, not a status
  paragraph) of the most important facts and priorities right now,
  and each section heading carries a freshness marker like
  `(updated 2026-04-01)`.

The key discipline: materials flow into STATE.md when an aspect crystallizes,
and then they get archived. STATE.md is never a log -- it is always a snapshot of
"what I know right now." The Hot List at the top is the fastest way to re-orient
after a break.

For larger or longer-lived projects, the curated layer can extend with two
optional documents -- `_knowledge/IDENTITY.md` (what the project IS) and
`_knowledge/VISION.md` (where it is HEADING). They are introduced manually
when a project earns them, not by default. See "Beyond STATE.md" below.

Both layers live under `_knowledge/` at the repo root. The root itself
stays artifact-forward (README, build manifest, src/, tests/, etc.)
so consumers see a normal project, while contributors and agents who
want the project's accumulated understanding find it one directory
in. The whole thing -- code AND meta -- lives in one Git repo, so a
clone has the full context.


## Setting Up a New Workspace

1. Copy this template folder to a new location.
2. Open it in your editor (Cursor, VS Code, or similar).
3. If this workspace analyzes an external codebase, note the paths and mention
   them when you tell the AI about the project in step 4 -- they will go into
   `_knowledge/STATE.md`.
4. Start a chat. The AI will notice that `_knowledge/STATE.md` does not
   exist and offer to create one based on what you tell it about the
   project. The initial `_knowledge/STATE.md` will include a Hot List, a
   Purpose section, Open Questions, and Action Items as a minimum
   skeleton.
5. Delete `README.md` and the `_template-docs/` folder. Both are template
   setup material -- the README is the template repo's landing page
   (GitHub conventions named it that), and `_template-docs/` holds the
   demo assets it embeds. Neither is needed once the template has been
   copied into a project.


## Day-to-Day Workflow

Work in chats as usual. The agent updates `_knowledge/STATE.md` directly
with clean operational findings and drops a dated `_knowledge/materials/`
file (e.g. `2026-03-09-memory-layout-notes.md`) for preliminary or
session-handoff material. Most of this happens without direction; the
prompts below are for when you want to drive something specific.

* "consolidate these materials into STATE.md" (name them, or say
  "everything about topic X") -- the agent rewrites affected sections and
  tells you which files are now fully absorbed.
* "audit state" (or "audit identity" / "audit vision") -- the agent checks
  for contradictions, stale freshness dates, dead references, and whether
  the Hot List still matches reality. It reports without silently rewriting.
* "wrap up the session" or "write a handoff" -- the agent dumps findings and
  open questions to a `_knowledge/materials/` file before context runs out.
  Agents are supposed to do this proactively when context is filling;
  ask if a session ends without one and you noticed.

When the urge hits to reorganize from scratch, resist copying everything into
a new folder. Instead, rewrite the stale `_knowledge/STATE.md` sections,
archive the materials that fed them, and leave in-progress aspects
untouched. Same psychological reset, no information loss.


## Beyond STATE.md: Identity and Vision

Most projects are well-served by `_knowledge/STATE.md` alone. As a project
grows and its worldview stabilises, two more curated documents become
useful under `_knowledge/`:

* `_knowledge/IDENTITY.md` -- what the project IS. Purpose, architectural
  commitments, posture, the "no, you cannot do that" rules that guard
  against shortcuts. Slow-changing.
* `_knowledge/VISION.md` -- where the project is HEADING. Long-term
  capabilities, reframes, moon shots, ambitions that orient design
  without driving immediate work. Updated occasionally.

The three together form the knowledge layer, each with a distinct role and
update cadence: STATE every session, IDENTITY when the worldview shifts (rare),
VISION when reflection produces durable new ambitions (occasional). If a
project has IDENTITY but no VISION, that is fine; the reverse is a smell --
vision without grounded identity tends to drift, so add IDENTITY first.

The agent watches for the cues that justify introducing these (architectural
content bleeding into the STATE.md hot list, vision-shaped material accumulating
across materials) and proposes the lift when warranted. You can also
trigger it directly: "lift the architectural sections of STATE.md into a new
IDENTITY.md" or "we have enough vision-shaped material in `_knowledge/materials/`;
create VISION.md from it."


## What Goes Where

The agent handles routing automatically; this list is just for orientation if
you want to know where things end up.

* Findings, answered questions, decisions --> `_knowledge/STATE.md`
  (rewrite sections, update freshness markers, re-examine the Hot
  List). This is the default destination.
* Architectural commitments, posture, "do not do this" rules (when
  `_knowledge/IDENTITY.md` exists) --> `_knowledge/IDENTITY.md`
* Long-term ambitions, reframes, moon shots (when
  `_knowledge/VISION.md` exists) --> `_knowledge/VISION.md`
* In-workspace project layout (run / build / test commands for
  `src/`, `impl/`, `android/`, etc.) --> a `## Layout` section in
  `_knowledge/STATE.md`, or section in `_knowledge/IDENTITY.md` if it
  exists
* Preliminary exploration, raw notes, chat dumps, session summaries,
  handoffs for future agents --> `_knowledge/materials/`
* Keyword index of materials --> `_knowledge/materials/INDEX.md`
  (agents maintain this automatically when they create or update
  materials; it lets future agents find relevant material
  without reading everything)
* Consumed materials --> `_knowledge/archive/` (the user moves them;
  the agent surfaces which are absorbed and updates the INDEX). Or
  just delete.
* External codebase paths (when the workspace analyzes code that
  lives elsewhere) --> `_knowledge/STATE.md` (or `_knowledge/IDENTITY.md`
  when it exists)


## Relationship to Karpathy's "LLM Wiki" Pattern

Andrey Karpathy proposed (April 2026) an LLM-maintained wiki as a persistent
knowledge layer over raw source documents. His design and this template share the
same core conviction: stop reconstructing understanding from scratch every session,
and maintain a living knowledge artifact instead.

### What we share

* Persistent synthesis as the central artifact, not ephemeral chat.
* Raw sources kept separate from curated knowledge.
* A schema file (AGENTS.md) that governs how the LLM maintains the knowledge layer.
* Rewrite-in-place rather than append-only updates.
* Freshness tracking on sections.
* Proactive maintenance -- the agent flags staleness, contradictions, and drift.
* Plain markdown, inspectable and editable, version-controlled.

### Where we differ

* Karpathy uses a multi-page wiki with cross-linked entity, concept,
  and synthesis pages. We default to a single STATE.md, with optional
  IDENTITY.md and VISION.md as a fixed-size extension when a
  project's worldview and ambitions outgrow what STATE alone can
  hold. This avoids inter-page consistency problems and ontology
  drift at the cost of a natural ceiling on volume. Beyond three
  curated documents, the right move is to split into separate
  workspaces.
* Karpathy defines ingest as a first-class automated operation (new
  source arrives, LLM updates 10-15 pages). Our system is
  conversation-driven -- the human controls the pace. This trades
  systematic coverage for tighter editorial control, which matters
  when "sources" are live code analysis rather than static documents.
* We add a materials layer (`_knowledge/materials/`) as a sanctioned
  messy staging area. Karpathy's design has no equivalent -- material
  goes straight into the wiki.
* We add a Hot List for rapid re-orientation. Karpathy has no equivalent.
* We add an explicit audit workflow (check contradictions, staleness,
  dead references). Karpathy's "lint" concept is similar but broader
  -- it also covers orphan pages and missing cross-links, which are
  multi-page wiki concerns.

### What we deliberately left out

* Formal page taxonomy (entity, concept, comparison pages) -- current LLMs already
  handle document granularity well without being told what page types exist.
  Imposing a taxonomy adds friction without solving a real problem at this scale.
* log.md as a changelog -- version control already provides history. A separate
  log file is maintenance overhead for information you rarely look at.
* Immutable/mutable document type distinction -- in practice the content itself
  signals what should and should not be rewritten (a meeting transcript vs. a
  synthesis). The formal distinction solves a problem that does not arise when a
  human controls the workflow.
* Multi-page wiki structure -- correct for large cross-domain knowledge bases,
  but trades the context-size problem for a harder context-selection problem
  (which of 500 pages need updating?). A single document eliminates update
  ambiguity entirely.
* Write-back from queries as an automatic workflow -- Karpathy says valuable
  answers should become wiki pages. Our agents are instructed to default to
  updating STATE.md with findings, which covers most of the same ground. The
  remaining gap (useful answers the user does not explicitly ask to save) could
  be addressed with a proactive suggestion, but has not caused problems in
  practice.

### If you outgrow this template

The natural evolution path if a single STATE.md becomes unwieldy:

* First, introduce IDENTITY.md and VISION.md as described in "Beyond
  STATE.md" above. This handles a deepening single project --
  architectural identity and long-term ambitions get their own homes,
  and STATE.md returns to operational state only.
* If the workspace genuinely contains multiple projects, split into
  per-project STATE-<name>.md files (or per-project subdirectories
  under `_knowledge/` with their own three-document knowledge layer).
  Add a top-level `_knowledge/STATE.md` that summarizes all projects (a
  few lines each). The agent reads the top-level state first, then
  loads the relevant project.

This gives bounded context per session without the multi-page consistency problem.
Beyond that, retrieval infrastructure (keyword search, semantic search) over the
curated knowledge layer becomes necessary regardless of organizational pattern.


## Design Principles

These explain why the template is shaped the way it is. Useful context for anyone
modifying or extending it.

### Artifact-forward root, meta in `_knowledge/`

The repository root is intended to look like a normal project: a
README, a build manifest if applicable (`pyproject.toml`, etc.),
`src/`, `tests/`, and so on. All meta -- the curated knowledge
layer, materials, optional helpers -- lives under `_knowledge/`.

This is the shape the template optimizes for, and the reason the
template exists in this form. The dominant failure mode of
long-running AI-assisted projects is stranded meta: code gets
versioned somewhere (GitLab, GitHub), meta gets parked in a personal
OneDrive folder or scattered notes alongside a non-versioned clone,
and the two diverge the moment the code becomes the authoritative
checkout. A clone gives the next contributor only the artifact, not
the reasoning. An agent starting in that clone has no project
history to draw on. Whatever the previous contributor (or previous
agent session) understood, tried, rejected, or pinned down --
gone, or at best searchable on the wrong machine.

Putting meta inside `_knowledge/` keeps it in the same repo as the code,
so it travels with every clone, every machine, every new contributor,
every fresh agent session, without dominating the root view that
consumers and casual readers see. Nothing is stranded outside the
repo. Nothing has to be reconstructed from chat history.

### Structure over procedure

AGENTS.md tells the AI what the workspace looks like and what the authority rules
are, but not step-by-step how to perform every task. Current LLMs handle judgment
calls -- what to update, how to split a topic, what granularity to use -- well
enough that specifying procedures for these things adds friction without improving
results. If you find yourself wanting to add detailed procedural instructions,
consider whether the model already does the right thing without them.

### Bounded curated layer

The curated layer is bounded: STATE.md by default, with optional IDENTITY.md and
VISION.md as a fixed extension. Not a wiki. This eliminates the hardest problems
in multi-page systems: inter-page consistency, update ambiguity (which pages
need changing?), and ontology drift (page categories that blur over time). The
tradeoff is a natural ceiling on volume. One project per workspace, three
documents max in the curated layer. If it gets unwieldy, split into separate
workspaces. See "If you outgrow this template" for the next step beyond that.

The cap at three is deliberate. Two would be too few -- experience showed that
mixing operational state with architectural worldview in one document creates a
hot list that keeps growing past its limits and eventually obscures what is
actually hot. Four or more starts to recreate wiki-style consistency problems.
Three is the smallest split where each tier has a distinct role (operational,
binding, aspirational) and each has a distinct update cadence (continuous, rare,
occasional). Adding a fourth would require an equally clean role and cadence
distinction, which has not surfaced in practice.

### Knowledge persistence across sessions

Agent chats are typically ephemeral. They hit context limits, get abandoned,
and -- depending on the tool -- may not even live with the project files (some
tools store chat history on the host machine, so a project accessed from
multiple machines effectively starts each session from a blank slate). The
materials layer (`_knowledge/materials/`) is the mechanism for getting
knowledge out of a chat and into the project before that happens, so
understanding is never trapped inside a single session.

This shifts the operational default. When an agent is unsure whether
a finding belongs in the curated layer, the right move is to drop a
materials file -- the cost of a messy file that gets archived later is
much smaller than the cost of knowledge lost when the chat ends. The
keyword index (`_knowledge/materials/INDEX.md`) is what makes this work
without future agents getting buried; every materials file lives behind
a few keywords that future agents grep before reading anything.

Materials do not need to pass any durability test. Session summaries, debug
notes, ideas that may not pan out, and handoffs for future agents are all valid
even if they will be obsolete in a week. Anything worth not losing is worth a
materials file.

### The AI is a maintainer, not a retriever

The template positions the AI's role as continuously maintaining a knowledge
artifact, not just answering questions from context. This is a deliberate framing
that affects behavior: agents default to updating STATE.md (or dropping a
materials file when in doubt) rather than producing standalone answers that
evaporate when the chat ends.

### Tool compatibility

`AGENTS.md` is the convergent standard for agent instructions and is
what this template treats as canonical. Tools that read it natively
work with no extra setup; tools that need a redirect get a small
import file at the root.

* Cursor (3.2.1+): reads `AGENTS.md` natively from the project root.
  No extra setup. Older Cursor versions may need a `.cursor/rules/`
  rule pointing at `AGENTS.md`; the template does not ship one.
* Codex CLI (OpenAI): reads `AGENTS.md` natively, walking from the
  project root upward, plus a global `~/.codex/AGENTS.md` if present.
  No extra setup.
* Claude Code (Anthropic): reads `CLAUDE.md` natively. The template
  ships a `CLAUDE.md` containing one line, `@AGENTS.md`, which Claude
  Code interprets as "import the contents of AGENTS.md as part of my
  rules." This means CLAUDE.md and AGENTS.md stay synchronized
  automatically -- you only edit AGENTS.md.
* Other tools: add the equivalent of "always read `AGENTS.md` first"
  in whatever mechanism the tool provides.


## Tips

* The `_knowledge/archive/` and `_knowledge/attic/` folders are optional.
  If you are comfortable deleting consumed materials, skip them.
  They exist for people who are not ready to let go yet.
* For meetings and interviews, consider keeping the full transcript
  in `_knowledge/archive/` and a shorter summary in `_knowledge/materials/`.
  The summary is what agents will find via the index and use
  day-to-day. The full transcript stays available in case you need
  to look up a specific quote, exact wording, or a detail the
  summary missed.
