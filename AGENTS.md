 Agents Rules

## Workspace Structure

This workspace is organized for knowledge management around an evolving
project.

Project memory lives under `_agents/` at the workspace root. Everything
inside `_agents/` is meta: the project's own state, working notes, and
optional helpers. The repository's product code, research notes, or
analysis sits alongside it under whatever shape the project calls for.

Curated knowledge layer (under `_agents/`):

* `_agents/STATE.md` (always present) -- Current operational state.
  What is in flight, what is unresolved, what comes next. Sections are
  rewritten as understanding matures, never merely appended to.
  Touched every session that produces operational findings.
* `_agents/IDENTITY.md` (optional; introduced for larger / longer-lived
  projects) -- What the project IS. Purpose, architectural
  commitments, posture, non-negotiables. Slow-changing.
* `_agents/VISION.md` (optional; introduced for larger / longer-lived
  projects) -- Where the project is HEADING. Long-term capabilities,
  reframes, moon shots, what the substrate or design enables that has
  not yet been built. Updated occasionally.

Working material (under `_agents/`):

* `_agents/working/` -- Messy exploration files, chat dumps, in-progress
  notes, session summaries, handoffs for future agents. Raw material,
  not reference. May be redundant, contradictory, or stale. Primary
  function: preserve knowledge across short-lived agent sessions, so
  it never lives only inside one chat. Err on the side of dumping --
  lost knowledge is more expensive than a messy file.
* `_agents/working/INDEX.md` -- Keyword index of all working files.
  This is how you find relevant working files without reading all of
  them. See "Working file hygiene".
* `_agents/archive/` -- Working files whose insights have been fully
  absorbed into the knowledge layer, plus raw source material (e.g.
  full meeting transcripts) that backs the summaries in
  `_agents/working/`. You may read files from `_agents/archive/` if
  you need original source detail that a summary does not cover.
  Files are moved here by the user after an agent surfaces a list of
  fully-absorbed working files (see "When asked to consolidate");
  agents do not move files into `_agents/archive/` themselves.
* `_agents/attic/` -- Discontinued work that may have future
  comparative value (a paused design, a deprecated approach kept for
  reference). Agents do NOT read `_agents/attic/` proactively, do not
  include it in searches, and do not surface its contents -- only
  access it when the user explicitly asks ("look in `_agents/attic/`
  for the old X"). The distinction from `_agents/archive/`: archive
  is consumed history; attic is parked work that may resume or be
  compared against later.

Project context:

* `README.md` -- If the workspace was started from the AI workspace
  template, the initial `README.md` is template setup documentation,
  not project content. Ignore it during normal operation. If it still
  exists alongside `_agents/STATE.md`, suggest deleting it (its top
  banner says the same). After deletion, a future `README.md` is
  project content like any other file.

Implementation directories (project-specific) sit at the workspace
root alongside `_agents/`. Project layout, build / run / test
commands, and key conventions live in `_agents/STATE.md` or
`_agents/IDENTITY.md` (when the latter exists). If you find a project
with substantial implementation but no orientation pointers in either
file, add a brief `## Layout` section to `_agents/STATE.md` -- a few
lines naming each directory and its run command is plenty.

---

## Knowledge Layer Tiers

### What goes where

* `_agents/STATE.md` is for what is HAPPENING now. Hot list, in-flight
  work, open questions, action items, freshly-pinned decisions whose
  rationale is still being absorbed. Operational. Updated every
  session.
* `_agents/IDENTITY.md` is for what the project IS. The mental model
  and worldview. Architectural commitments. Conventions. Constraints
  that cannot be renegotiated cheaply. The "no, you cannot do that"
  rules that guard against shortcuts. Updated when the worldview
  shifts (rare); treated as a deliberate act, not a side-effect of
  feature work.
* `_agents/VISION.md` is for where the project is HEADING. Long-term
  capabilities, reframes, moon shots, ambitions worth preserving so
  they do not get lost in day-to-day work. Updated when reflection
  or brainstorming produces durable new ambitions. Occasional.

When a finding is clean enough for the curated layer, decide which
tier. Will it still be valid in three months? If yes (binding rule,
stable architecture decision, posture commitment) ->
`_agents/IDENTITY.md`. If it is something you want to be true at some
future point -> `_agents/VISION.md`. Otherwise -> `_agents/STATE.md`.
(This is a routing test among curated tiers, not a gate on whether
to capture at all -- findings that are not yet curated-layer-ready
go to `_agents/working/` regardless of how durable they are.)

### When to introduce them

* `_agents/IDENTITY.md`: when a Purpose section or Design Summary
  section in `_agents/STATE.md` has been substantially stable for
  weeks and you find yourself re-explaining its content rather than
  evolving it. Lift those sections out of `_agents/STATE.md` into
  `_agents/IDENTITY.md` and replace with a short cross-reference.
* `_agents/VISION.md`: when a brainstorm session or reflection
  produces long-term ambitions that you want to preserve as
  orientation without driving immediate work. The brainstorm itself
  can stay in `_agents/working/` while the durable distillation
  moves to `_agents/VISION.md`.

If a project has `_agents/IDENTITY.md` but no `_agents/VISION.md`,
that is fine. If a project has `_agents/VISION.md` but no
`_agents/IDENTITY.md`, that is a smell -- vision without grounded
identity tends to drift. Add `_agents/IDENTITY.md` first.

### Cross-references

Each knowledge layer file should open with a short preamble pointing
at the others (whichever exist), so a reader landing on any one of
them can find the rest. The shape:

* `_agents/STATE.md` opens by pointing at `_agents/IDENTITY.md` (for
  what the project is) and `_agents/VISION.md` (for where it is
  heading) and any canonical design doc in `_agents/working/`.
* `_agents/IDENTITY.md` opens by pointing at `_agents/VISION.md` and
  `_agents/STATE.md`.
* `_agents/VISION.md` opens by pointing at `_agents/IDENTITY.md` and
  `_agents/STATE.md`.

### Reading order for context priming

When starting a session:

1. Read `_agents/STATE.md`. The hot list is the most informative thing
   in the workspace.
2. Read `_agents/IDENTITY.md` when the task touches architectural
   decisions, when contemplating a shortcut, when reorienting after a
   long break, or when uncertain whether a proposed change matches
   the project's worldview.
3. Read `_agents/VISION.md` when doing big-picture work,
   prioritisation, reflection, or when asked to think about
   direction.

Do not read all three on every trivial task. Read the cheapest
sufficient subset.

---

## Rules for AI Assistants

Your primary job in this workspace is to keep knowledge from getting
lost across short-lived agent sessions. Two operational forms:

* Maintain the curated layer (`_agents/STATE.md`, plus
  `_agents/IDENTITY.md` and `_agents/VISION.md` when they exist) as a
  reliable, current set of references.
* Capture session-bound knowledge into `_agents/working/` --
  summaries, handoffs, partial findings -- so understanding persists
  when the chat ends.

The curated layer is the project's reference state; working files
are the persistence mechanism that prevents knowledge loss between
agents. Treat both as continuous responsibilities, not periodic
cleanup tasks.

`_agents/IDENTITY.md` and `_agents/VISION.md` exist only when the
project has earned them; do not create them eagerly. When they exist,
route findings to whichever file's role they fit (see "What goes
where" above).

### Markdown files

When writing Markdown files, default to these rules:

* Use one or more leading `#` for sections, not the alternative style
  with separate underlining.
* Use `---` horizontal lines where they make sense.
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
knowledge layer files, and handoff working files.

### Local file operations

Local file operations (Read, Write, StrReplace, Edit) are cheap. Do
not batch them, avoid them, or stage findings in chat awaiting
permission to write them. Read multiple files in parallel when
relevant; write files when you have content to write. The "minimize
tool calls" instinct applies to MCP tools and external shell
commands, not to local file work.

### When producing findings or insights

* When a finding is clean and operational, update `_agents/STATE.md`
  directly. If the topic already has a section, rewrite that section.
  If it is a new aspect, add a section.
* If the finding is binding worldview / posture / architectural
  commitment (and `_agents/IDENTITY.md` exists), route there instead.
  If `_agents/IDENTITY.md` does not exist but the finding clearly
  belongs there, add it to `_agents/STATE.md` and flag that this is a
  candidate for an eventual `_agents/IDENTITY.md` lift.
* If the finding is long-term ambition / reframe / moon shot (and
  `_agents/VISION.md` exists), route there. Otherwise, drop a working
  doc in `_agents/working/`; vision-shaped material benefits from
  staging in working files until it stabilises.
* A finding may have multiple aspects (operational + architectural,
  or near-term + long-term). Split it across tiers and cross-
  reference rather than forcing the whole thing into one home.
* Use a `_agents/working/` file when the finding is preliminary
  (still exploring, conclusion might change), when it is a session
  summary or handoff for future agents, when it captures context
  another agent should not have to rediscover, or when you need a
  staging area before synthesis.
* Capture in the same turn as you produce the finding. Do not
  present analysis and ask "shall I write this up?" -- write the
  file and announce it in the same reply. Objection is cheaper
  than missed capture.
* Inside `_agents/working/`: create freely; name the file and
  summarise its contents in a sentence or two in the same reply.
* Outside `_agents/working/`: never create or move a file without
  explicit confirmation.

### When updating knowledge layer files

* Rewrite the relevant section to reflect current understanding. Do
  not append "update:" blocks or changelog entries -- the document
  should always read as a clean current-state description.
* Preserve sections unrelated to the current task verbatim.
* If a new aspect has emerged that deserves its own section, add it
  and suggest where it fits in the document's structure.
* Freshness markers. Two conventions, depending on the file:
  - `_agents/STATE.md` uses per-section markers
    (`## Technical Status (updated YYYY-MM-DD)`) because its sections
    are rewritten independently. Update the marker on sections you
    actually rewrite; leave others as-is.
  - `_agents/IDENTITY.md` and `_agents/VISION.md` use a single
    top-level marker on the document title
    (`# Title (updated YYYY-MM-DD)`) because the worldview and
    ambitions tend to evolve as a whole. Bump the top-level marker
    on any substantive edit.
  - Working files do not need freshness markers; their dated
    filename is the freshness signal.

`_agents/STATE.md`-specific rule:

* Hot list. `_agents/STATE.md` starts with a `## Hot List` section
  immediately after any preamble. This is a short (typically ~5
  bullets) summary of the most important facts and priorities right
  now. The number is a heuristic for spotting trouble, not a hard
  cap. Bullets should be terse -- one or two lines each, a headline
  plus pointers (to action items, design docs, working files), not
  full status paragraphs. If a bullet keeps growing, content has
  crept in from another section; lift the detail to its proper home
  and leave a pointer. Every time you update any section of
  `_agents/STATE.md`, also re-examine the hot list and rewrite it if
  the update changes what matters most. The hot list must always be
  current -- it is the first thing a reader (human or AI) sees.

### Session-end handoff

When a session is wrapping up -- the user signals they are done, the
context window is filling, or the work has produced findings without
landing in the curated layer -- drop a working file summarising what
was learned, what is still open, and where the next agent should
pick up. Frame it as a handoff. Add an `INDEX.md` entry like any
other working file. This is the operational form of the "preserve
knowledge across sessions" responsibility from the preamble; do it
without being asked when the conditions hit.

### When asked to consolidate

When the user asks to consolidate, fold in, merge, promote, or
otherwise move working-file content into the knowledge layer -- in
any phrasing -- do the following:

1. Read the specified working files and the relevant knowledge layer
   files.
2. Identify which insights from the working files are not yet
   captured in the knowledge layer.
3. Route each insight to its correct tier:
   - Operational, in-flight, soon-to-change -> `_agents/STATE.md`.
   - Stable architectural commitment, posture, worldview ->
     `_agents/IDENTITY.md` (or stage in `_agents/STATE.md` if
     `_agents/IDENTITY.md` does not exist yet, and suggest the lift).
   - Long-term ambition, reframe, moon shot -> `_agents/VISION.md`
     (or stage in `_agents/working/` if `_agents/VISION.md` does not
     exist yet, and suggest the lift).
4. Rewrite the affected sections incorporating those insights.
5. Re-examine the `_agents/STATE.md` hot list and rewrite it if the
   consolidated insights change what matters most.
6. List which working files are now fully absorbed and can be moved
   to `_agents/archive/`. The user typically performs the move.
7. After files are moved (in the same session or a later one),
   remove their entries from `_agents/working/INDEX.md`. The index
   lists only files currently in `_agents/working/`.
8. Flag any files that are only partially absorbed (some aspects
   still in progress, or only some sections promoted to a higher
   tier). Partially absorbed files stay in `_agents/working/` until
   fully absorbed.

### Working file hygiene

Reading working files:

* To find relevant working files, read `_agents/working/INDEX.md`.
  It contains keywords for every working file. Use it to decide
  which files to open -- do not read all working files to "build
  context".
* Do not treat working files as authoritative. If they conflict with
  the knowledge layer, the knowledge layer wins unless the user
  says otherwise.

Creating and updating working files:

* Use descriptive names with date prefix:
  `YYYY-MM-DD-short-description.md`.
* Every time you create or substantially update a working file, you
  must also update its entry in `_agents/working/INDEX.md`. This is
  not optional -- the index is how future agents find relevant
  material. A file without an index entry is invisible.
* When a working file is moved to `_agents/archive/`, remove its
  entry from `INDEX.md`. The index should only list files that are
  currently in `_agents/working/`.
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
  working files and the understanding seems stable, suggest
  consolidating into the knowledge layer.
* If a knowledge layer section looks stale relative to recent chat
  findings, mention it. If you are working in an area covered by a
  section whose freshness date is old, say so even if the user did
  not ask.
* If your own analysis or evidence from code contradicts something
  in the knowledge layer, say so explicitly and quote the specific
  passage that conflicts, so the user can compare without hunting.
  The knowledge layer is authoritative over working files, but it
  is not infallible -- flag the contradiction and let the user
  decide.
* When creating a working file that covers ground already in the
  knowledge layer, say which sections overlap and whether the
  working file adds anything beyond what is already captured. This
  prevents working files from silently accumulating redundant
  material.
* If `_agents/STATE.md`'s hot list keeps drifting well past ~5
  bullets because architectural content keeps showing up there,
  suggest introducing `_agents/IDENTITY.md` and lifting that
  content out.
* If brainstorm-shaped content keeps accumulating across working
  files without an obvious home, suggest introducing
  `_agents/VISION.md`.

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
* For `_agents/STATE.md`: check whether the hot list still reflects
  the most important priorities, or whether it has drifted from
  what the sections actually say.
* For `_agents/IDENTITY.md`: check whether any section has
  accumulated operational content that should be in
  `_agents/STATE.md`, and whether any commitments have been
  silently violated by recent work.
* For `_agents/VISION.md`: check whether any of the long-term
  ambitions have drifted into the active roadmap (promote to
  `_agents/STATE.md` action items if so), and whether the
  cross-references to `_agents/IDENTITY.md` commitments still hold.
* Report what you find. Do not silently rewrite -- present the
  issues and let the user decide what to update.

### Bootstrapping

If `_agents/STATE.md` does not exist, follow this procedure to
bootstrap the workspace before doing other operational work:

1. Ask the user what the project or investigation is about.
2. If `_agents/working/` already contains files, offer to read them
   and incorporate their content into the initial
   `_agents/STATE.md`.
3. If `_agents/working/INDEX.md` does not exist but
   `_agents/working/` contains files, create the index by reading
   each file and generating its keyword entry.
4. Create `_agents/STATE.md` using the skeleton below. Fill in real
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

5. If a top-level `README.md` exists and its content is the AI
   workspace template's setup documentation (sections like
   "The Problem This Solves", "Core Concepts", "Setting Up a New
   Workspace"), suggest to the user that it can be deleted now that
   the workspace is set up. Do not delete a `README.md` whose
   content is project documentation.
6. If the user wants an LF-only repository, point them at the
   "Optional: LF-only Line Endings" section in the template's
   `README.md` and offer to run `python _agents/apply-lf-policy.py`.
   Do not apply the policy silently; `.gitattributes` and
   `.editorconfig` are project policy files, not public-template
   defaults.

Do not add bootstrap procedures for `_agents/IDENTITY.md` or
`_agents/VISION.md`. They are introduced manually as the project
earns them; see "When to introduce them" above.
