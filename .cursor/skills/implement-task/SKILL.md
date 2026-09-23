---
name: implement-task
description: Full multi-repo implementation pipeline for a feature or bugfix. Orchestrates repo-sync, planner, implementer (per service), quality loops, audits, git-shipper, and Obsidian docs update. Use when the user says "implement task", "run pipeline", "реализуй задачу", provides a ticket number (ABC-123 / #123), or asks to ship a feature end-to-end.
---

# Implement Task Pipeline

Orchestrates: sync → plan → implement (by waves) → quality → audit → ship → docs.

**You are the orchestrator. You delegate to subagents. You do not write code yourself.**

## Launching subagents

Prefer `Task` with `subagent_type` equal to the agent name (`repo-sync`, `planner`, `implementer`, …).

If that type is **not** in the Task tool's available list:

1. Read `.cursor/agents/<name>.md` from this config repo.
2. Launch `Task` with `subagent_type: generalPurpose`.
3. Set `model` from that file's frontmatter (`composer-2.5-fast` or omit for `inherit`).
4. Put the agent body at the top of the prompt, then the stage inputs.

Every implementer / quality / git prompt must include: **only modify files under this repo path: `<absolute path>`**.

Keep a table of agent IDs per service (`implementer`, `quality-gate`). **Resume** those IDs on rework. Do not spawn a fresh implementer for the same service unless resume fails.

## Before you start

1. Locate `pipeline.yaml` in the workspace root (or a path the user gave). If absent, stop.
2. Validate: `main_branch` (string), `repos` (non-empty list of `{name, path}`). Optional: `obsidian_vault`, `auto_push` (default `false`).
3. Resolve every `repos[].path` to an **absolute** path (relative paths are relative to the directory that contains `pipeline.yaml`). If a path is not a git repo, stop.
4. Extract `TASK_ID` (`ABC-123`, `#123`, …). If absent, ask. Do not ship without it.
5. Determine task type: `feat` (default) or `fix`.

## Pipeline checklist

```
Pipeline run — <TASK_ID>
- [ ] Stage 1: repo-sync
- [ ] Stage 2: planner (save .pipeline/<TASK_ID>.md)
- [ ] Stage 3: implementer waves (resume IDs recorded)
- [ ] Stage 4: quality-gate loop (changed services only, max 5)
- [ ] Stage 5: plan-auditor (max 3; resume implementer)
- [ ] Stage 6: bug-hunter (max 3)
- [ ] Stage 7: task-auditor (max 3)
- [ ] Stage 8: ship confirmation → git-shipper
- [ ] Stage 9: docs-analyst + docs-writer
```

## Stage instructions

### Stage 1 — repo-sync

Invoke `repo-sync` with `pipeline.yaml` and absolute repo paths.
If any repo is dirty, missing `origin`, or `git pull --ff-only` fails — **stop**. Show the full report.

### Stage 2 — planner

Invoke `planner` with the task, Task ID, and absolute repo paths.

Required output:

- `affected_services: [...]`
- `implementation_order:` list of waves (each wave is a list of service names that may run in parallel)
- `## Shared contracts` — HTTP/JSON/events that more than one service depends on (or `none`)
- Per-service plan sections

If `affected_services` is empty, stop and tell the user the task needs no code changes (or the planner could not map it).

Write the full planner output to `.pipeline/<TASK_ID>.md` in the workspace (create `.pipeline/` if needed). Later stages read this file. Do not commit it to service repos.

### Stage 3 — implementer (waves)

For each wave in `implementation_order` (default: one wave = all affected services):

- Launch one `implementer` per service **in that wave**, in parallel.
- Prompt includes: absolute path, per-service plan, **full Shared contracts**, task, Task ID.
- Record the returned agent ID as `implementer[<service>]`.
- Wait for the wave to finish before starting the next wave.

If an implementer reports `IMPLEMENTATION=NO_CHANGES`, skip that service in stages 4–6.

### Stage 4 — quality-gate loop (changed services)

Working directory **must** be the service absolute path (`cd` there, then `bash scripts/run_quality_gate.sh`).

1. Invoke `quality-gate`. Save agent ID as `quality-gate[<service>]`.
2. `QUALITY_GATE=PASS` → Stage 5.
3. `QUALITY_GATE=FAIL` → new `quality-fixer`, then **resume** `quality-gate[<service>]`.
4. Max **5** rounds, then escalate.

### Stage 5 — plan-auditor

1. Invoke `plan-auditor` with `.pipeline/<TASK_ID>.md` (that service's section) and the repo path.
2. `PLAN_AUDIT=PASS` → Stage 6.
3. `PLAN_AUDIT=FAIL` → **resume** `implementer[<service>]` with the gap list (do not start a new implementer). Then rerun Stage 4. Max **3** rounds.

### Stage 6 — bug-hunter

1. Invoke `bug-hunter` with the repo path and changed files.
2. `BUG_HUNT=PASS` → Stage 7.
3. `BUG_HUNT=FIXED` → rerun Stage 4, then continue. Max **3** rounds.

### Stage 7 — task-auditor

Invoke `task-auditor` once with all affected repos, the original task, shared contracts, and `.pipeline/<TASK_ID>.md`.

- `TASK_AUDIT=PASS` → Stage 8.
- `TASK_AUDIT=FAIL` → resume the named service's implementer, rerun Stages 4–6 for that service. Max **3** rounds.

### Stage 8 — git-shipper

Collect repos with a real diff.

Show the user a ship summary:

- Task ID, type, branch name
- Each repo: path, files changed, proposed commit subject

Then:

- If `auto_push: true` in `pipeline.yaml` → run `git-shipper`.
- Otherwise **wait for explicit user approval**. Do not push until they say yes.

Pass to `git-shipper`: Task ID, type, slug, absolute paths, `main_branch`.

If the target branch already exists in a repo, git-shipper must abort that repo (no nested branches, no reuse of an old branch).

### Stage 9 — docs

If `obsidian_vault` is missing, empty, or not a directory → `DOCS=SKIPPED`, done.

Otherwise invoke `docs-analyst`. On `DOCS=UPDATE_NEEDED`, invoke `docs-writer` with that plan only.

## Escalation

When a loop hits its limit, stop and report: stage, service, last failure, what the user must decide. Do not push partial work unless the user asks.

## Additional reference

- [hexagonal.md](hexagonal.md) — layer boundaries, async ports, Note example
- [quality-gates.md](quality-gates.md) — exact commands and pass criteria
- [git-conventions.md](git-conventions.md) — branch, commit, and push rules
- [pipeline-config.md](pipeline-config.md) — pipeline.yaml schema
