# Agents Rules

## Workspace Structure

This workspace is organized for knowledge management around an evolving
project.

Project memory lives under `_knowledge/` at the workspace root. Everything
inside `_knowledge/` is meta: the project's own state, materials, and
optional helpers. The repository's product code, research notes, or
analysis sits alongside it under whatever shape the project calls for.

Curated knowledge layer (under `_knowledge/`):

* `_knowledge/STATE.md` (always present) -- Current operational state.
  What is in flight, what is unresolved, what comes next. Sections are
  rewritten as understanding matures, never merely appended to.
  Touched every session that produces operational findings.
* `_knowledge/IDENTITY.md` (optional; introduced for larger / longer-lived
  projects) -- What the project IS. Purpose, architectural
  commitments, posture, non-negotiables. Slow-changing.
* `_knowledge/VISION.md` (optional; introduced for larger / longer-lived
  projects) -- Where the project is HEADING. Long-term capabilities,
  reframes, moon shots, what the substrate or design enables that has
  not yet been built. Updated occasionally.

Materials layer (under `_knowledge/`):

* `_knowledge/materials/` -- Messy exploration files, chat dumps, in-progress
  notes, session summaries, handoffs for future agents. Raw material,
  not reference. May be redundant, contradictory, or stale. Primary
  function: preserve knowledge across short-lived agent sessions, so
  it never lives only inside one chat. Err on the side of dumping --
  lost knowledge is more expensive than a messy file.
* `_knowledge/materials/INDEX.md` -- Keyword index of all materials.
  This is how you find relevant materials without reading all of
  them. See "Materials hygiene".
* `_knowledge/archive/` -- Materials whose insights have been fully
  absorbed into the knowledge layer, plus raw source material (e.g.
  full meeting transcripts) that backs the summaries in
  `_knowledge/materials/`. You may read files from `_knowledge/archive/` if
  you need original source detail that a summary does not cover.
  Files are moved here by the user after an agent surfaces a list of
  fully-absorbed materials (see "When asked to consolidate");
  agents do not move files into `_knowledge/archive/` themselves.
* `_knowledge/attic/` -- Discontinued work that may have future
  comparative value (a paused design, a deprecated approach kept for
  reference). Agents do NOT read `_knowledge/attic/` proactively, do not
  include it in searches, and do not surface its contents -- only
  access it when the user explicitly asks ("look in `_knowledge/attic/`
  for the old X"). The distinction from `_knowledge/archive/`: archive
  is consumed history; attic is parked work that may resume or be
  compared against later.

Project context:

* `README.md` -- If the workspace was started from the Project
  Knowledge Base template, the initial `README.md` is template setup
  documentation, not project content. Ignore it during normal
  operation. If it still exists alongside `_knowledge/STATE.md`,
  suggest deleting it (its top banner says the same). After
  deletion, a future `README.md` is project content like any other
  file.

Implementation directories (project-specific) sit at the workspace
root alongside `_knowledge/`. Project layout, build / run / test
commands, and key conventions live in `_knowledge/STATE.md` or
`_knowledge/IDENTITY.md` (when the latter exists). If you find a project
with substantial implementation but no orientation pointers in either
file, add a brief `## Layout` section to `_knowledge/STATE.md` -- a few
lines naming each directory and its run command is plenty.

---

## Knowledge Layer Tiers

### What goes where

* `_knowledge/STATE.md` is for what is HAPPENING now. Hot list, in-flight
  work, open questions, action items, freshly-pinned decisions whose
  rationale is still being absorbed. Operational. Updated every
  session.
* `_knowledge/IDENTITY.md` is for what the project IS. The mental model
  and worldview. Architectural commitments. Conventions. Constraints
  that cannot be renegotiated cheaply. The "no, you cannot do that"
  rules that guard against shortcuts. Updated when the worldview
  shifts (rare); treated as a deliberate act, not a side-effect of
  feature work.
* `_knowledge/VISION.md` is for where the project is HEADING. Long-term
  capabilities, reframes, moon shots, ambitions worth preserving so
  they do not get lost in day-to-day work. Updated when reflection
  or brainstorming produces durable new ambitions. Occasional.

When a finding is clean enough for the curated layer, decide which
tier. Will it still be valid in three months? If yes (binding rule,
stable architecture decision, posture commitment) ->
`_knowledge/IDENTITY.md`. If it is something you want to be true at some
future point -> `_knowledge/VISION.md`. Otherwise -> `_knowledge/STATE.md`.
(This is a routing test among curated tiers, not a gate on whether
to capture at all -- findings that are not yet curated-layer-ready
go to `_knowledge/materials/` regardless of how durable they are.)

### When to introduce them

* `_knowledge/IDENTITY.md`: when a Purpose section or Design Summary
  section in `_knowledge/STATE.md` has been substantially stable for
  weeks and you find yourself re-explaining its content rather than
  evolving it. Lift those sections out of `_knowledge/STATE.md` into
  `_knowledge/IDENTITY.md` and replace with a short cross-reference.
* `_knowledge/VISION.md`: when a brainstorm session or reflection
  produces long-term ambitions that you want to preserve as
  orientation without driving immediate work. The brainstorm itself
  can stay in `_knowledge/materials/` while the durable distillation
  moves to `_knowledge/VISION.md`.

If a project has `_knowledge/IDENTITY.md` but no `_knowledge/VISION.md`,
that is fine. If a project has `_knowledge/VISION.md` but no
`_knowledge/IDENTITY.md`, that is a smell -- vision without grounded
identity tends to drift. Add `_knowledge/IDENTITY.md` first.

### Cross-references

Each knowledge layer file should open with a short preamble pointing
at the others (whichever exist), so a reader landing on any one of
them can find the rest. The shape:

* `_knowledge/STATE.md` opens by pointing at `_knowledge/IDENTITY.md` (for
  what the project is) and `_knowledge/VISION.md` (for where it is
  heading) and any canonical design doc in `_knowledge/materials/`.
* `_knowledge/IDENTITY.md` opens by pointing at `_knowledge/VISION.md` and
  `_knowledge/STATE.md`.
* `_knowledge/VISION.md` opens by pointing at `_knowledge/IDENTITY.md` and
  `_knowledge/STATE.md`.

### Reading order for context priming

When starting a session:

1. Read `_knowledge/STATE.md`. The hot list is the most informative thing
   in the workspace.
2. Read `_knowledge/IDENTITY.md` when the task touches architectural
   decisions, when contemplating a shortcut, when reorienting after a
   long break, or when uncertain whether a proposed change matches
   the project's worldview.
3. Read `_knowledge/VISION.md` when doing big-picture work,
   prioritisation, reflection, or when asked to think about
   direction.

Do not read all three on every trivial task. Read the cheapest
sufficient subset.

---

## Rules for AI Assistants

Your primary job in this workspace is to keep knowledge from getting
lost across short-lived agent sessions. Two operational forms:

* Maintain the curated layer (`_knowledge/STATE.md`, plus
  `_knowledge/IDENTITY.md` and `_knowledge/VISION.md` when they exist) as a
  reliable, current set of references.
* Capture session-bound knowledge into `_knowledge/materials/` --
  summaries, handoffs, partial findings -- so understanding persists
  when the chat ends.

The curated layer is the project's reference state; materials
are the persistence mechanism that prevents knowledge loss between
agents. Treat both as continuous responsibilities, not periodic
cleanup tasks.

Knowledge coherence is part of normal edits, not only an audit
task. When you touch a curated file or a materials file, do a
local coherence pass before finishing the turn: re-read the
specific sections and cross-references you touched, and check
`_knowledge/materials/INDEX.md` when materials membership changed.
Fix obvious bookkeeping drift directly -- a stale `INDEX.md` entry
pointing at a file no longer in `_knowledge/materials/`, a cross-
reference to a renamed or moved section, a freshness marker that
contradicts the actual update. If the right fix would require
interpreting content or changing meaning, flag it instead of
guessing. The trigger is local evidence encountered during normal
work; do not expand this into a full audit unless the user asks.

`_knowledge/IDENTITY.md` and `_knowledge/VISION.md` exist only when the
project has earned them; do not create them eagerly. When they exist,
route findings to whichever file's role they fit (see "What goes
where" above).

### Markdown files

These rules keep files diff-friendly, greppable, and consistently rendered in plain-text contexts.

When writing Markdown files, default to these rules:

* Use one or more leading `#` for sections, not the alternative style
  with separate underlining.
* Prefer `*` for unordered lists over `-`. Nested lists inside
  ordered or checkbox lists may use `-` to keep the hierarchy
  visible.
* Do not use text styles like bold or italic.
* Do not use non-ASCII characters like em-dash, arrow glyphs, etc.
  Use ASCII representations like `-`, `--`, `->`, `<->`. Exception:
  when quoting text that uses Unicode glyphs.
* If both list (bullet points) and tables are equally suitable,
  prefer a list.

### Reporting test status

Report green/red, not counts. "532 tests passed" goes stale and is
ambiguous (full suite or subset?); "full suite green".
When a count IS informative, name what it counts
("12 new idempotency tests added; suite green"). Applies to commits,
knowledge layer files, and handoff materials.

### Local file operations

Local file operations (Read, Write, StrReplace, Edit) are cheap. Do
not batch them, avoid them, or stage findings in chat awaiting
permission to write them. Read multiple files in parallel when
relevant; write files when you have content to write. The "minimize
tool calls" instinct applies to MCP tools and external shell
commands, not to local file work.

### When producing findings or insights

* When a finding is clean and operational, update `_knowledge/STATE.md`
  directly. If the topic already has a section, rewrite that section.
  If it is a new aspect, add a section.
* If the finding is binding worldview / posture / architectural
  commitment (and `_knowledge/IDENTITY.md` exists), route there instead.
  If `_knowledge/IDENTITY.md` does not exist but the finding clearly
  belongs there, add it to `_knowledge/STATE.md` and flag that this is a
  candidate for an eventual `_knowledge/IDENTITY.md` lift.
* If the finding is long-term ambition / reframe / moon shot (and
  `_knowledge/VISION.md` exists), route there. Otherwise, drop a
  materials file in `_knowledge/materials/`; vision-shaped material
  benefits from staging in materials until it stabilises.
* A finding may have multiple aspects (operational + architectural,
  or near-term + long-term). Split it across tiers and cross-
  reference rather than forcing the whole thing into one home.
* Use a `_knowledge/materials/` file when the finding is preliminary
  (still exploring, conclusion might change), when it is a session
  summary or handoff for future agents, when it captures context
  another agent should not have to rediscover, or when you need a
  staging area before synthesis.
* Capture in the same turn as you produce the finding. Do not
  present analysis and ask "shall I write this up?" -- write the
  file and announce it in the same reply. Objection is cheaper
  than missed capture.
* Inside `_knowledge/materials/`: create freely; name the file and
  summarise its contents in a sentence or two in the same reply.
* Outside `_knowledge/materials/`: never create or move a file without
  explicit confirmation.

### When updating knowledge layer files

* Rewrite the relevant section to reflect current understanding. Do
  not append "update:" blocks or changelog entries -- the document
  should always read as a clean current-state description.
* Preserve sections unrelated to the current task verbatim.
* If a new aspect has emerged that deserves its own section, add it
  and suggest where it fits in the document's structure.
* Freshness markers. Two conventions, depending on the file:
  - `_knowledge/STATE.md` uses per-section markers
    (`## Technical Status (updated YYYY-MM-DD)`) because its sections
    are rewritten independently. Update the marker on sections you
    actually rewrite; leave others as-is.
  - `_knowledge/IDENTITY.md` and `_knowledge/VISION.md` use a single
    top-level marker on the document title
    (`# Title (updated YYYY-MM-DD)`) because the worldview and
    ambitions tend to evolve as a whole. Bump the top-level marker
    on any substantive edit.
  - Materials do not need freshness markers; their dated
    filename is the freshness signal.

`_knowledge/STATE.md`-specific rule:

* Hot list. `_knowledge/STATE.md` starts with a `## Hot List` section
  immediately after any preamble. This is a short (typically ~5
  bullets) summary of the most important facts and priorities right
  now. The number is a heuristic for spotting trouble, not a hard
  cap. Bullets should be terse -- one or two lines each, a headline
  plus pointers (to action items, design docs, materials), not
  full status paragraphs. If a bullet keeps growing, content has
  crept in from another section; lift the detail to its proper home
  and leave a pointer. Every time you update any section of
  `_knowledge/STATE.md`, also re-examine the hot list and rewrite it if
  the update changes what matters most. The hot list must always be
  current -- it is the first thing a reader (human or AI) sees.

### Session-end handoff

When a session is wrapping up -- the user signals they are done, the
context window is filling, or the work has produced findings without
landing in the curated layer -- drop a materials file summarising what
was learned, what is still open, and where the next agent should
pick up. Frame it as a handoff. Add an `INDEX.md` entry like any
other materials file. This is the operational form of the "preserve
knowledge across sessions" responsibility from the preamble; do it
without being asked when the conditions hit.

### When asked to consolidate

When the user asks to consolidate, fold in, merge, promote, or
otherwise move materials into the knowledge layer -- in any
phrasing -- do the following:

1. Read the specified materials and the relevant knowledge layer
   files.
2. Identify which insights from the materials are not yet
   captured in the knowledge layer.
3. Route each insight to its correct tier:
   - Operational, in-flight, soon-to-change -> `_knowledge/STATE.md`.
   - Stable architectural commitment, posture, worldview ->
     `_knowledge/IDENTITY.md` (or stage in `_knowledge/STATE.md` if
     `_knowledge/IDENTITY.md` does not exist yet, and suggest the lift).
   - Long-term ambition, reframe, moon shot -> `_knowledge/VISION.md`
     (or stage in `_knowledge/materials/` if `_knowledge/VISION.md` does not
     exist yet, and suggest the lift).
4. Rewrite the affected sections incorporating those insights.
5. Re-examine the `_knowledge/STATE.md` hot list and rewrite it if the
   consolidated insights change what matters most.
6. List which materials are now fully absorbed and can be moved
   to `_knowledge/archive/`. The user typically performs the move.
7. After files are moved (in the same session or a later one),
   remove their entries from `_knowledge/materials/INDEX.md`. The index
   lists only files currently in `_knowledge/materials/`.
8. Flag any files that are only partially absorbed (some aspects
   still in progress, or only some sections promoted to a higher
   tier). Partially absorbed files stay in `_knowledge/materials/` until
   fully absorbed.

### Materials hygiene

Reading materials:

* To find relevant materials, read `_knowledge/materials/INDEX.md`.
  It contains keywords for every materials file. Use it to decide
  which files to open -- do not read all materials to "build
  context".
* Do not treat materials as authoritative. If they conflict with
  the knowledge layer, the knowledge layer wins unless the user
  says otherwise.

Creating and updating materials:

* Use descriptive names with date prefix:
  `YYYY-MM-DD-short-description.md`.
* Every time you create or substantially update a materials file, you
  must also update its entry in `_knowledge/materials/INDEX.md`. This is
  not optional -- the index is how future agents find relevant
  material. A file without an index entry is invisible.
* When a materials file leaves `_knowledge/materials/` -- moved to
  `_knowledge/archive/`, parked in `_knowledge/attic/`, deleted, or
  renamed -- remove or update its entry in `INDEX.md`. The index
  should only list files currently in `_knowledge/materials/`. This
  applies whether you performed the move yourself or noticed
  afterwards that the user or a past agent did; do not wait for an
  audit prompt.
* The entry format is:

```
## <filename>
<keywords, separated by commas -- aim for 10-20 per file, covering the
main topics, names, technical terms, and concepts in the file>
```

### When asked to commit

When the user asks to commit, push, or otherwise capture changes in
git -- in any phrasing -- two rules apply on top of the system's
standard git commit guidance:

* Commit only your own scope. Stage only files YOU edited or
  created in this session, tracked from your own tool-call history.
  Other agents or background tools may have modified files
  concurrently; those are out of scope and stay unstaged. Never use
  `git add .`, `git add -A`, or `git commit -a` -- they sweep up
  out-of-scope changes. If `git status` shows changes you did not
  make, name them in your reply (so the user knows they are still
  pending) but leave them alone. If you cannot reconstruct your
  scope confidently, ask; do not guess from the diff.

* Chain related git commands into single shell calls.
  - Pre-flight inspection: one call
    (`git status; git diff -- <files>; git log --oneline -10`).
  - Commit: one call
    (`git add <files> && git commit -m ... && git status`).
  Keeping the commit as one atomic shell call makes it reviewable
  as a unit and avoids the per-call approval friction some setups
  have.

### Proactive suggestions

* If you notice the user has explored an aspect across multiple
  materials and the understanding seems stable, suggest
  consolidating into the knowledge layer.
* If a knowledge layer section looks stale relative to recent chat
  findings, mention it. If you are working in an area covered by a
  section whose freshness date is old, say so even if the user did
  not ask.
* If your own analysis or evidence from code contradicts something
  in the knowledge layer, say so explicitly and quote the specific
  passage that conflicts, so the user can compare without hunting.
  The knowledge layer is authoritative over materials, but it
  is not infallible -- flag the contradiction and let the user
  decide.
* When creating a materials file that covers ground already in the
  knowledge layer, say which sections overlap and whether the
  materials file adds anything beyond what is already captured. This
  prevents materials from silently accumulating redundant
  material.
* If `_knowledge/STATE.md`'s hot list keeps drifting well past ~5
  bullets because architectural content keeps showing up there,
  suggest introducing `_knowledge/IDENTITY.md` and lifting that
  content out.
* If brainstorm-shaped content keeps accumulating across materials
  without an obvious home, suggest introducing `_knowledge/VISION.md`.
* If you notice a materials file referenced by
  `_knowledge/materials/INDEX.md` is no longer in
  `_knowledge/materials/`, treat the index as out of date and repair
  it the moment you see it -- not only during an audit. Remove the
  entry if the file has moved to `_knowledge/archive/` (insights
  absorbed) or `_knowledge/attic/` (parked work, not surfaced
  proactively). If the file has simply vanished with no trace in
  archive or attic, ask the user before deleting the entry. Apply
  the same logic to cross-references in `_knowledge/STATE.md`,
  `_knowledge/IDENTITY.md`, or `_knowledge/VISION.md` that point at
  a moved or missing file.

### Auditing knowledge layer files

When the user asks to check, audit, or review the knowledge layer
for staleness, contradictions, drift, or accuracy -- in any
phrasing, including indirect prompts like "is this still right?",
"anything outdated here?", or "does this match the code?" -- do the
following:

* Read the specified file(s) in full and check each section for
  internal consistency -- do any sections make claims that
  contradict other sections?
* Check freshness dates. Flag any section that has not been updated
  in a long time, especially if the underlying topic is fast-moving.
* If codebase references are present, spot-check whether key file
  paths, class names, or symbols mentioned still exist in the code.
* For `_knowledge/STATE.md`: check whether the hot list still reflects
  the most important priorities, or whether it has drifted from
  what the sections actually say.
* For `_knowledge/IDENTITY.md`: check whether any section has
  accumulated operational content that should be in
  `_knowledge/STATE.md`, and whether any commitments have been
  silently violated by recent work.
* For `_knowledge/VISION.md`: check whether any of the long-term
  ambitions have drifted into the active roadmap (promote to
  `_knowledge/STATE.md` action items if so), and whether the
  cross-references to `_knowledge/IDENTITY.md` commitments still hold.
* Report what you find. Do not silently rewrite -- present the
  issues and let the user decide what to update.

### Bootstrapping

If `_knowledge/STATE.md` does not exist, follow this procedure to
bootstrap the workspace before doing other operational work:

1. Ask the user what the project or investigation is about.
2. If `_knowledge/materials/` already contains files, offer to read them
   and incorporate their content into the initial
   `_knowledge/STATE.md`.
3. If `_knowledge/materials/INDEX.md` does not exist but
   `_knowledge/materials/` contains files, create the index by reading
   each file and generating its keyword entry.
4. Create `_knowledge/STATE.md` using the skeleton below. Fill in real
   content based on what the user told you -- do not leave
   placeholders. Add more sections as needed, but never remove
   these:

```
# <Project Name> -- Project State

## Hot List

* <up to 5 bullets: the most important facts and priorities right now>

## Purpose (updated YYYY-MM-DD)

<What this project is and why it exists. 1-3 paragraphs.>

## Open Questions (updated YYYY-MM-DD)

* <Things not yet understood or decided>

## Action Items (updated YYYY-MM-DD)

* <What to do next>
```

5. If a top-level `README.md` exists and its content is the
   Project Knowledge Base template's setup documentation (sections
   like "The Problem This Solves", "Core Concepts", "Setting Up a
   New Workspace"), suggest to the user that it can be deleted now
   that the workspace is set up. Do not delete a `README.md` whose
   content is project documentation.

Do not add bootstrap procedures for `_knowledge/IDENTITY.md` or
`_knowledge/VISION.md`. They are introduced manually as the project
earns them; see "When to introduce them" above.
