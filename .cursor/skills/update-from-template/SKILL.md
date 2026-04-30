---
name: update-from-template
description: >-
  Sync the AI workspace template into this project. Use when the user asks to
  update / sync / migrate from the template, to pull in template changes, or
  when template-controlled files (AGENTS.md, CLAUDE.md, .cursor/rules,
  bootstrap skill) appear stale relative to the source. Reads the source
  location from _template/template-source at the project root.
---

# Update from Template

Sync the evolving template into this project: bring template-controlled
files current, lift any project-side pollution out of those files, and
sweep the curated layer (`STATE.md`, `IDENTITY.md`, `VISION.md`) for
implications of rule changes -- without losing knowledge.

This skill is the symmetrical operation of `bootstrap-workspace`:
bootstrap creates the curated layer in a fresh project; this skill keeps
the template-controlled scaffolding current as the template evolves.

## When to run

* The user asks to update, sync, migrate, or pull template changes.
* The user mentions the template has evolved and they want this project
  brought current.
* The user says something like "this project's AGENTS.md looks old" or
  "let's apply the template's new rules here."

## Inputs

Read `_template/template-source` at the project root.

* Format: first non-empty, non-comment line wins. Comments start with `#`.
* Value: either a git URL or a local filesystem path.
* If the file is missing, empty, or has only comment lines: STOP, tell
  the user, do nothing. Do not fall back to a hardcoded default.

Resolve the source:

* URL -> `git clone --depth 1 <url> <tempdir>`. Read tracked files from
  the clone. Clean up the temp dir afterward.
* Local path -> read directly from the filesystem.

## Sanity checks

Before any other work:

* `STATE.md` must exist in the project root. If not, this is not an
  initialized project -- STOP and suggest running the
  `bootstrap-workspace` skill instead.
* The resolved source must contain `AGENTS.md`. If not, the source is
  not a template -- STOP and tell the user.
* If `_template/template-source` is a URL and `git` is not available,
  STOP and suggest installing git or pointing `_template/template-source`
  at a local filesystem path.

## Project folders

Before classifying files, check the project's folder shape:

* `_working/` -- required by this skill (snapshots go here per
  Information Preservation Rule 1). If missing, create it silently
  along with `_working/.gitkeep`.
* `_archive/`, `_attic/` -- optional content folders. The skill never
  reads from or writes to them, but their absence may be intentional
  (the user does not want them) or accidental (project predates the
  convention, or they were deleted). If either is missing, mention it
  in the migration report and offer to create it. Do NOT auto-create
  -- the user may have a deliberate reason for the absence.

## Tracked files

Owned by the template:

* `AGENTS.md`
* `CLAUDE.md`
* All files under `.cursor/rules/`
* All files under `.cursor/skills/bootstrap-workspace/`
* All files under `.cursor/skills/update-from-template/` (this skill)
* `_template/.gitignore`
* `_template/line-endings.md`
* `_template/apply-lf-policy.py`

NOT touched (project-owned content):

* `STATE.md`, `IDENTITY.md`, `VISION.md`
* All files under `_working/`, `_archive/`, `_attic/`
* `_working/INDEX.md`
* Project's `README.md` (if present -- the template's README is deleted
  from projects after bootstrap; any README in a mature project is
  project content)
* `_working/.gitkeep`, `_archive/.gitkeep`, `_attic/.gitkeep`
  (irrelevant once dirs have content; do not propagate)
* `_template/template-source` (project-local template source setting)
* `.gitattributes` and `.editorconfig` (project policy files, created only
  when the user opts in to the LF-only policy)

`_template/` is optional helper material. If a project deleted it on
purpose, do not treat that as a broken workspace; report that template
sync / LF-policy helpers are unavailable unless the user wants them
restored.

## Flow

### Step 1: Classify each tracked file

For each tracked file, compare the source's version against the
project's version:

* IDENTICAL: skip silently.
* TEMPLATE_ONLY (file in source, not in project): propose ADD.
* PROJECT_ONLY (file in project, not in source): the file was removed
  from the template since the project's last sync, or the project was
  bootstrapped against an old shape that named files differently (e.g.
  `follow-agents-md.mdc` later renamed to `workspace-rules.mdc`).
  Propose REMOVE, and if a similar file appears in TEMPLATE_ONLY, note
  the rename hypothesis explicitly.
* DIFF (both exist, content differs): read both fully. Continue with
  Step 2 for each.

### Step 2: For DIFF files, separate template evolution from project pollution

The invariant (per AGENTS.md "Template-Controlled Files"): these files
are not edited per project. Project-side content in a tracked file is a
violation, almost certainly either:

* Old-template-shape content the project was bootstrapped on (e.g. an
  old `AGENTS.md` from before the template grew IDENTITY/VISION rules).
* Pollution: project-specific additions that should never have been in
  a tracked file (e.g. external codebase paths in `AGENTS.md`).

Distinguish by reading both versions:

* Template-style content: matches the template's voice and structure;
  lives in similar sections in the source. Treat as template evolution.
* Project-specific content: clearly project-local (codebase paths,
  project-specific workflows, named entities from the project). Treat
  as pollution.
* Ambiguous content: ASK the user; do not classify silently.

For pollution, propose lifting it to its proper home:

* Codebase paths, run commands, layout -> `STATE.md` (or `IDENTITY.md`
  if it exists and the content is binding architectural commitment).
* Project-specific conventions -> same routing rule.

Pollution is removed from the tracked file as part of the sync.

### Step 3: Identify semantic implications of template evolution

The diff between the project's tracked files and the source's tracked
files IS the template evolution since the project's last sync.

For each substantive rule change, identify implications for the
project's curated layer (`STATE.md`, plus `IDENTITY.md` / `VISION.md`
if they exist) and `_working/`. Examples of the kind of implication to
look for:

* New "Reporting test status" rule -> sweep curated layer for stale
  test counts; propose rewriting per the new rule.
* Introduction of IDENTITY.md / VISION.md tier system -> if the project
  has architectural-flavored content in `STATE.md`, propose lifting per
  the cross-tier rules below (Information Preservation, Rule 3).
* Changed working-file naming convention -> sweep `_working/` for
  non-conformant names.
* New consolidation / audit / handoff rules -> usually no immediate
  sweep; inform the user about the new agent behaviors.

### Step 4: Present the plan

Compile the plan with three classes of items:

1. Structural file changes (ADDs, REMOVEs, file overwrites for DIFFs).
2. Pollution lifts (project-specific content moved out of tracked
   files into the curated layer; tracked file then cleaned).
3. Semantic sweeps (proposed rewrites of curated-layer sections per
   the new rules).

Show each item with enough detail for the user to approve or reject.
Get approval per item or wholesale.

### Step 5: Apply

Apply approved items in this order:

1. Snapshots (per Information Preservation, Rule 1).
2. Pollution lifts FIRST: move project-specific content out of tracked
   files into the curated layer. Must happen before file overwrites,
   otherwise an overwrite would lose the pollution before it is preserved.
3. Structural file changes: overwrite tracked files with source
   versions, add new files, remove obsolete files.
4. Semantic sweeps: apply curated-layer rewrites per the Information
   Preservation rules below.

### Step 6: Report

At the end, produce a summary:

* Files changed (added / removed / overwritten).
* Pollution lifted (what was in which tracked file, where it now lives).
* Curated-layer sections rewritten.
* Snapshot files created (per Information Preservation, Rule 1).
* Any items the user deferred or rejected.

Tell the user explicitly that the snapshot files in `_working/` are
recovery insurance and can be deleted once they are satisfied nothing
was lost.

---

## Information Preservation

The agent's natural restructuring tendency is to "improve" wording,
drop "redundant" detail, and match the destination tier's tone when
promoting content. Each of these silently loses knowledge. Real
evidence: on a prior project, a similar migration agent dropped
substantial detail when promoting STATE content to IDENTITY/VISION;
recovery required a second agent reading both old and new and
re-extracting what was lost.

LLM behavior is non-deterministic but is steerable. Apply ALL of the
following rules during Step 5 semantic sweeps. They overlap on
purpose.

### Rule 1: Snapshot before any change to STATE / IDENTITY / VISION

Before modifying `STATE.md`, copy its current content to:

* `_working/YYYY-MM-DD-state-pre-migration.md` (current date)

Same for `IDENTITY.md` and `VISION.md` if they will be modified.

Add an entry to `_working/INDEX.md` for each snapshot. Mention the
snapshot files in the final report so the user knows they exist.

### Rule 2: Restructuring is information-preserving

* Moving and rephrasing are allowed.
* Summarizing and condensing are NOT allowed.
* Every nuance in the original must be carried into the new version.
* This skill is migration, not editorial cleanup.

### Rule 3: Cross-tier promotions are SPLIT operations, not CONDENSE

Moving content from STATE to IDENTITY/VISION is the highest-risk
operation because the destination's natural register is more abstract.
Agents tend to "match the new tier" and drop low-level specifics. This
is forbidden.

A cross-tier promotion is a SPLIT:

* Identify what fits the destination tier (high-level architectural
  framing for IDENTITY, ambition framing for VISION).
* Identify what does NOT fit (engineering specifics, current
  operational state, examples, quirks, context-dependent details).
* The fitting content goes to the destination.
* The non-fitting content STAYS in `STATE.md` (or routes to a working
  file if it is preliminary or context-bound).
* Nothing is dropped on the way up.

Example: lifting an "Architecture" section from `STATE.md` to
`IDENTITY.md`. The architectural commitment ("we use a single-page
state document with optional tier extensions") goes up. The specific
quirk ("tool X hits context limits around 50KB so we keep state under
that") stays in `STATE.md`.

### Rule 4: Inventory-and-route discipline

For any restructure (in-tier or cross-tier), first write an inventory
of the source content as discrete items: every fact, claim, example,
constraint, nuance, detail.

Route each item to a destination:

* -> `STATE.md` (operational, current)
* -> `IDENTITY.md` (architectural commitment)
* -> `VISION.md` (long-term ambition)
* -> `_working/<filename>.md` (preliminary or context-bound)
* -> DROP (with explicit reason; needs separate user approval per item)

The inventory may be temporarily written to a working file for
transparency. Never silently merge or omit items.

### Rule 5: Default is keep, never silently drop

The agent does not unilaterally decide a detail is "stale" or
"redundant". Every proposed drop is a separate user approval.

### Rule 6: Section by section, never bulk

Apply changes one section at a time, with approval per section. No
bulk apply across multiple sections. This limits blast radius.

### Rule 7: Post-apply diff against snapshot

After all sweeps are applied, do a final pass:

* Re-read each snapshot (pre-migration version).
* Re-read the new versions across all tiers (and any new working
  files created during the sync).
* For each item from the snapshot, confirm it appears in the new
  version, in another tier, or in a working file.
* Surface anything that does not appear anywhere; ask the user:
  "this looks lost -- confirm intentional drop or restore?"

This is the safety net. Even if earlier rules are imperfectly applied,
the post-apply check catches losses.

---

## Posture

This skill is conservative by design. Surface lots, ask often, never
apply without approval. The cost of an extra question is much smaller
than the cost of lost knowledge.

A dry-run mode is implicitly available: when the user asks to "see what
would change" or similar, perform Steps 1-4 and present the plan
without applying anything. Apply only when the user gives an explicit
go-ahead.
