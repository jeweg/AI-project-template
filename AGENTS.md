# Agents Rules

## Workspace Structure

This workspace is organized for knowledge management around an evolving
project.

Project memory lives under `_knowledge/` at the workspace root. It holds
two layers with different audiences:

* The curated layer -- `STATE.md`, plus `IDENTITY.md` and `VISION.md`
  when introduced. The project's internal scaffolding: operational
  state, posture, ambition. Meta about the project, for the project's
  own agents and contributors. Not exposed externally.
* The materials layer -- `_knowledge/materials/`. The project's
  knowledge namespace: working notes, exploration, session bridges,
  and (for knowledge-heavy projects) durable knowledge artifacts
  that may be the project's deliverable. Holds both lowercase-named
  working files and UPPERCASE canonical artifacts (`INDEX.md`,
  `OVERVIEW.md`) that describe and announce the namespace; the
  contents themselves are not externally exposed by default.

The repository's product code or other deliverables sit alongside
`_knowledge/` under whatever shape the project calls for. For
knowledge-heavy projects, the deliverable may itself live inside
`_knowledge/materials/`; that is the design point, not a violation
of the structure.

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

* `_knowledge/materials/` -- The project's knowledge namespace.
  Contains two kinds of files:

  - Working files (lowercase-named, e.g. `topic-description.md`):
    exploration, chat dumps, in-progress notes, session summaries,
    handoffs for future agents, and -- for knowledge-heavy projects -- durable
    knowledge artifacts (sources, syntheses, entities) that form
    the project's deliverable content. May be redundant,
    contradictory, or stale. Primary function: preserve knowledge
    across short-lived agent sessions, so it never lives only
    inside one chat. Err on the side of dumping -- lost knowledge
    is more expensive than a messy file.
  - Canonical artifacts (UPPERCASE) that describe the namespace:
    `INDEX.md` and `OVERVIEW.md`, detailed below. The UPPERCASE
    casing is the structural marker that distinguishes them from
    working files; future canonical artifacts (if any emerge) follow
    the same pattern.

* `_knowledge/materials/INDEX.md` -- Internal-facing keyword index
  of all working files in `materials/`. This is how agents find
  relevant materials without reading all of them. See "Materials
  hygiene".
* `_knowledge/materials/OVERVIEW.md` -- External-facing
  announcement of what the materials namespace contains. Lets
  external agents and MCP servers discover that the project exists
  and decide whether to ask it about specific topics. Whether and
  how the project actually serves any materials contents to outside
  agents is a separate decision the project makes when it has
  decided what is safe to expose; OVERVIEW.md is the announcement,
  not a license to serve everything. Always present (shipped
  pre-created with a default banner; replaced on first session via
  the bootstrap flow). Describes the contents of `materials/` only
  -- the curated layer (STATE, IDENTITY, VISION) is internal
  scaffolding and is not externally exposed. See "When updating
  OVERVIEW.md".
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

* Template setup material (`README.md`) -- If the workspace was
  started from the Project Knowledge Base template, the initial
  `README.md` is template setup documentation, not project content.
  Ignore it during normal operation. If it still exists alongside a
  bootstrapped project (see "Bootstrap" below), suggest deleting it
  -- the file's purpose was to explain the template, and that job
  is finished once the project is in use. After deletion, a future
  `README.md` is project content like any other file.

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
lost across short-lived agent sessions. The forms vary by project
type:

* Maintain the curated layer (`_knowledge/STATE.md`, plus
  `_knowledge/IDENTITY.md` and `_knowledge/VISION.md` when they exist)
  as a reliable, current set of references for the project itself.
* Capture working knowledge into `_knowledge/materials/` -- session
  summaries, handoffs, partial findings, and (for knowledge-heavy
  projects) durable knowledge artifacts -- so understanding persists
  when the chat ends and is reachable by future agents.
* Keep `_knowledge/materials/OVERVIEW.md` current as the materials
  namespace evolves; it is the project's external-facing
  self-description.

The curated layer is the project's internal reference state.
Materials are both the persistence mechanism that prevents knowledge
loss between agents and (for knowledge-heavy projects) the project's
deliverable knowledge namespace. Treat all of these as continuous
responsibilities, not periodic cleanup tasks.

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
  another agent should not have to rediscover, when you need a
  staging area before synthesis, or -- for knowledge-heavy projects
  -- when capturing durable knowledge artifacts (sources, syntheses,
  entities) that form the project's deliverable content. The latter
  stay in `materials/` permanently; they do not migrate up into the
  curated layer.
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
* Freshness markers. Conventions vary by file type:
  - `_knowledge/STATE.md` uses per-section markers
    (`## Technical Status (updated YYYY-MM-DD)`) because its sections
    are rewritten independently. Update the marker on sections you
    actually rewrite; leave others as-is.
  - `_knowledge/IDENTITY.md` and `_knowledge/VISION.md` use a single
    top-level marker on the document title
    (`# Title (updated YYYY-MM-DD)`) because the worldview and
    ambitions tend to evolve as a whole. Bump the top-level marker
    on any substantive edit.
  - Materials carry no required freshness markers. When a
    long-lived materials file has been substantially revised, an
    inline `(updated YYYY-MM-DD)` marker on its title is useful
    but optional. Filenames do not encode freshness.

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

### When updating OVERVIEW.md

`_knowledge/materials/OVERVIEW.md` is the project's external-facing
announcement of its knowledge namespace. It exists so external
agents and MCP servers can discover that the project exists and
decide whether to ask it about specific topics. It describes only
the contents of `materials/` -- not STATE, IDENTITY, or VISION
(those are internal scaffolding and are not externally exposed).
OVERVIEW.md is the announcement, not a license to serve any
particular file externally; whether and how to expose any specific
material is a separate decision the project makes when it has
decided what is safe to share, with whatever filtering it then
designs.

OVERVIEW.md is always present. The template ships it pre-created
with a default banner; the bootstrap flow fills it on first session
based on the user's project description. From then on it is
maintained continuously alongside the materials namespace, not
"introduced" -- the introduce-when-earned pattern applies to
IDENTITY.md and VISION.md, not to OVERVIEW.md.

When to update it: maintain it alongside knowledge artifacts in the
same turn. Whenever a materials change shifts the namespace's shape
-- a new topic area, materially deeper coverage of an existing area,
or a retired area -- adjust OVERVIEW.md accordingly:

* Adjust the keyword section if the namespace shape shifted.
* Adjust the coverage section if a topic was added, retired, or
  changed depth.
* Bump the freshness marker on the title.
* Rewrite the one-line summary if the project's scope shifted
  meaningfully.

Keep OVERVIEW.md tight (a paragraph plus the two structured
sections) and free of project-internal operational detail. The
audience is external agents deciding whether to query the project's
knowledge, and agents that have just entered and need to orient --
not the project's own working agents (those have STATE.md and
INDEX.md).

OVERVIEW.md uses plain markdown with no YAML frontmatter. Skeleton:

```
# <Project Name> -- Knowledge Base Overview (updated YYYY-MM-DD)

<One-sentence external-facing description of what this project
knows and what makes the coverage distinctive.>

## Keywords

<comma-separated list of 10-30 keywords covering the project's
topics, named entities, and distinctive characteristics. Same shape
as INDEX.md per-file entries, but project-level rather than
per-file.>

## Coverage

* <topic area>: <depth indicator (e.g. Deep / Working / Light / Partial)
  and one-line description, optionally naming safe-to-reference
  canonical materials>
```

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

For knowledge-heavy projects, recognise that some materials are
durable knowledge artifacts (sources, syntheses, entities) that do
not consolidate upward into the curated layer -- they ARE the
project's reference content and stay in `materials/` permanently.
Apply the consolidation flow only to materials whose insights belong
in STATE / IDENTITY / VISION (operational state, posture commitments,
long-term ambitions about the project itself). Do not propose moving
durable knowledge artifacts to `_knowledge/archive/` just because
they look "settled".

### Materials hygiene

Reading materials:

* To find relevant materials, read `_knowledge/materials/INDEX.md`.
  It contains keywords for every materials file. Use it to decide
  which files to open -- do not read all materials to "build
  context".
* Do not treat materials as authoritative. If they conflict with
  the knowledge layer, the knowledge layer wins unless the user
  says otherwise.

Creating and updating materials (working files):

* Use descriptive lowercase names. The lowercase casing is what
  marks a file as a working file rather than a canonical namespace
  artifact (the UPPERCASE `INDEX.md` and `OVERVIEW.md`). The
  template imposes no fixed naming pattern beyond that; pick names
  that read well in `INDEX.md` and that future agents can scan.
* Optionally prefix a date (`YYYY-MM-DD-topic.md`) when the file is
  anchored to a specific event whose date is genuinely meaningful
  -- a meeting transcript, a dated newsletter capture, a session
  handoff. For files that are designed to evolve over time, omit
  the date; it would only encode creation, not freshness, and the
  inline `(updated YYYY-MM-DD)` marker on the title handles
  freshness for revised content.
* Every time you create or substantially update a working file,
  also update its entry in `_knowledge/materials/INDEX.md`. This is
  not optional -- the index is how future agents find relevant
  material. A file without an index entry is invisible.
* When a working file leaves `_knowledge/materials/` -- moved to
  `_knowledge/archive/`, parked in `_knowledge/attic/`, deleted, or
  renamed -- remove or update its entry in `INDEX.md`. The index
  should only list files currently in `_knowledge/materials/`. This
  applies whether you performed the move yourself or noticed
  afterwards that the user or a past agent did; do not wait for an
  audit prompt.
* The `INDEX.md` entry format is:

```
## <filename>
<keywords, separated by commas -- aim for 10-20 per file, covering the
main topics, names, technical terms, and concepts in the file>
```

* When the working-file change shifts the shape of the materials
  namespace -- a new topic area, materially deeper coverage, or a
  retired area -- update `_knowledge/materials/OVERVIEW.md` in the
  same turn. INDEX.md is per-file metadata (every working file
  change touches it); OVERVIEW.md is project-level (only
  namespace-shape changes touch it). See "When updating
  OVERVIEW.md" for the shape of those updates.

### Validation

The template ships `_knowledge/check.py`, an advisory script that
verifies the mechanically-checkable invariants -- the rules above
that are deterministic from file content alone:

* Bootstrap state of the pre-shipped knowledge files (`STATE.md`
  and `OVERVIEW.md`): sentinel banner removed, no `<...>`
  placeholder text or unfilled `YYYY-MM-DD` markers remaining.
* INDEX membership: every working file in `_knowledge/materials/`
  has a `## <filename>` entry in `INDEX.md`, and every entry
  points at a file that exists.

Run with `python3 _knowledge/check.py` from anywhere inside the
project (use `python` instead if your system aliases it that way).
Reports findings, one per line, and exits 0 if clean or 1 if there
are findings. Does not modify any file -- the user or agent fixes
findings deliberately. Useful after substantial knowledge-layer
work, when suspecting bookkeeping drift, before a commit, or as
part of a session-end audit.

If Python is not available on the system, skip this step rather
than attempt to install it. The script is advisory; manual
inspection of `INDEX.md` membership and the pre-shipped files'
banner / placeholder state covers the same rules and is what the
script automates.

If a pre-shipped knowledge file (`STATE.md`, `materials/INDEX.md`,
`materials/OVERVIEW.md`) is missing entirely, the script reports it
with a hint to restore via `git checkout HEAD -- <path>` or to
copy the file back from the template repo. The script does not
attempt to recreate missing files itself; recovery is left to git
or to manual restoration so the script does not have to keep a
duplicate copy of the template defaults in sync with the actual
files.

The script's scope is intentionally narrow: it does not check
whether the hot list reflects current priorities, whether
OVERVIEW.md describes the namespace's actual shape, or whether
freshness markers are honest. Those are agent responsibilities,
not script responsibilities.

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

* Chain related git commands into single compound shell calls.
  - Pre-flight inspection: one call covering status, diff for the
    relevant files, and recent log.
  - Commit: one call covering add, commit, and status.
  Keeping each as one compound call makes it reviewable as a unit
  and avoids the per-call approval friction some setups have. Use
  whatever chaining syntax the active shell accepts.

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
* For `_knowledge/materials/OVERVIEW.md`: check whether the keyword
  and coverage sections still match the actual
  shape of `materials/`. New topic areas in `materials/` that are
  not reflected in the coverage section, or coverage entries that
  point at retired files, are drift signals. Also check whether
  the one-line summary still fits the project's current scope.
* Report what you find. Do not silently rewrite -- present the
  issues and let the user decide what to update.

### Bootstrap

The template ships pre-created knowledge files with sentinel banners
at the top, marking them as template default content. The agent's
job on first session is to detect those banners, interview the user,
and replace the default content with real content based on the
user's project description.

Detection: a knowledge file is unbootstrapped if its first non-empty
line is a blockquote (starting with `>`) containing the phrase
"template default content". The pre-shipped files that carry such
banners are `_knowledge/STATE.md` and `_knowledge/materials/OVERVIEW.md`.
`_knowledge/materials/INDEX.md` ships effectively empty (an HTML
comment placeholder, no banner) and is filled by the agent appending
entries naturally as working files are created -- not via bootstrap.

Partial bootstrap: if a banner is gone but `<...>` placeholder text
or unfilled `YYYY-MM-DD` markers remain, the bootstrap was started
but not finished. Complete it (replace placeholders, set freshness
markers to today's date) rather than treating the file as fully
bootstrapped. Both checks together: banner present means
unbootstrapped; banner absent plus placeholders means broken
bootstrap.

When you find a banner-marked file in a session before the user has
described the project, follow this procedure:

1. Ask the user what the project or investigation is about.
2. If `_knowledge/materials/` already contains working files (the
   user may have placed exploration notes there before opening the
   first chat), read them and incorporate their content into the
   filled `STATE.md` and `OVERVIEW.md`. Add `INDEX.md` entries for
   any pre-existing working files at the same time.
3. For each banner-marked file, replace the default content with
   real content. Keep the structural sections (in `STATE.md`: Hot
   List, Purpose, Open Questions, Action Items; in `OVERVIEW.md`:
   the title summary, Keywords, Coverage). Fill freshness markers
   with today's date. Do not leave any `<...>` placeholder text.
4. Remove the entire `> NOTE: ...` blockquote from each file you
   filled. The banner's job is over once real content is in place.
5. If a top-level `README.md` exists and reads as the Project
   Knowledge Base template's setup material (it documents how to
   use the template, links to a `project-knowledge-base-meta`
   companion repo, and tells readers to delete it after copying),
   suggest deleting it. Its job is finished once the project is in
   use. Do not delete a `README.md` whose content is project
   documentation.

Do not introduce `_knowledge/IDENTITY.md` or `_knowledge/VISION.md`
during bootstrap. They are introduced manually as the project earns
them; see "When to introduce them" above.
