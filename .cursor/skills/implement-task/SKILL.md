---
name: implement-task
description: Full multi-repo implementation pipeline for a feature or bugfix. Orchestrates repo-sync, planner, implementer (per service), quality loops, audits, git-shipper, and Obsidian docs update. Use when the user says "implement task", "run pipeline", "реализуй задачу", provides a ticket number (ABC-123 / #123), or asks to ship a feature end-to-end.
---

# Implement Task Pipeline

Orchestrates the full implementation pipeline: sync → plan → implement → quality → audit → ship → docs.

**You are the orchestrator. You delegate to subagents. You do not write code yourself.**

## Launching subagents

Prefer `Task` with `subagent_type` equal to the agent name (`repo-sync`, `planner`, `implementer`, …).

If that type is **not** in the Task tool's available list:

1. Read `.cursor/agents/<name>.md` from this config repo (or the workspace copy).
2. Launch `Task` with `subagent_type: generalPurpose`.
3. Set `model` to the value in that file's frontmatter (`composer-2.5-fast` or omit for `inherit`).
4. Put the agent body at the top of the prompt, then the stage inputs (repo path, plan, task id).

Every implementer / quality / git prompt must include: **only modify files under this repo path: `<absolute path>`**.

## Before you start

1. Locate `pipeline.yaml` in the workspace root. If absent, stop and ask the user to create it (see [pipeline-config.md](pipeline-config.md)).
2. Extract `TASK_ID` from the user's message (`ABC-123`, `#123`, etc.). If absent, ask before proceeding.
3. Determine task type: `feat` (default) or `fix`.

## Pipeline checklist

Copy this checklist and track progress:

```
Pipeline run — <TASK_ID>
- [ ] Stage 1: repo-sync
- [ ] Stage 2: planner
- [ ] Stage 3: implementer (one per service)
- [ ] Stage 4: quality-gate loop (per service, max 5 rounds)
- [ ] Stage 5: plan-auditor (per service, max 3 rounds)
- [ ] Stage 6: bug-hunter (per service, max 3 rounds)
- [ ] Stage 7: task-auditor (all repos, max 3 rounds)
- [ ] Stage 8: git-shipper
- [ ] Stage 9: docs-analyst + docs-writer
```

## Stage instructions

### Stage 1 — repo-sync

Invoke `repo-sync` with the `pipeline.yaml` contents.
If any repo is dirty, **stop** and show the dirty-repo report to the user. Do not proceed until resolved.

### Stage 2 — planner

Invoke `planner` with:
- Task description
- Task ID
- All repo paths from `pipeline.yaml`

Collect `affected_services` list from the output.

### Stage 3 — implementer (parallel per service)

For each service in `affected_services`, invoke `implementer` with:
- Service name and repo path
- The per-service plan section from planner output
- Task description and Task ID

Run implementers in parallel across services.

### Stage 4 — quality-gate loop (per service)

For each service:
1. Invoke `quality-gate` with the repo path.
2. If `QUALITY_GATE=PASS` → move to Stage 5.
3. If `QUALITY_GATE=FAIL`:
   - Invoke `quality-fixer` with the repo path and failure report.
   - Resume `quality-gate` (same agent ID) to recheck.
   - Repeat up to **5 rounds**. If still failing after round 5 → escalate to user.

### Stage 5 — plan-auditor (per service)

For each service:
1. Invoke `plan-auditor` with the plan and repo path.
2. If `PLAN_AUDIT=PASS` → move to Stage 6.
3. If `PLAN_AUDIT=FAIL`:
   - Invoke `implementer` again with the gap list.
   - Rerun `quality-gate` loop (Stage 4) before re-auditing.
   - Repeat up to **3 rounds**. If still failing → escalate to user.

### Stage 6 — bug-hunter (per service)

For each service:
1. Invoke `bug-hunter` with the repo path and changed files list.
2. If `BUG_HUNT=PASS` → move to Stage 7.
3. If `BUG_HUNT=FIXED`:
   - Rerun `quality-gate` loop (Stage 4) before Stage 7.
4. Repeat up to **3 rounds**. If serious bugs persist → escalate to user.

### Stage 7 — task-auditor (all repos)

Invoke `task-auditor` once with all repo paths and the original task.
- If `TASK_AUDIT=PASS` → Stage 8.
- If `TASK_AUDIT=FAIL`: send each gap to the relevant `implementer`, rerun Stage 4–6 for that service. Repeat up to **3 rounds**.

### Stage 8 — git-shipper

Invoke `git-shipper` with:
- Task ID
- Task type (`feat` / `fix`)
- Kebab slug derived from the task title
- Only repos that have a diff

### Stage 9 — docs

1. Invoke `docs-analyst` with vault path, task description, and changes summary.
2. If `DOCS=NO_CHANGES` → done.
3. If `DOCS=UPDATE_NEEDED` → invoke `docs-writer` with the update plan.

## Escalation

When any loop reaches its round limit, stop and report:
- Which stage failed
- Current failure details
- What the user must decide

## Additional reference

- [hexagonal.md](hexagonal.md) — layer boundaries, async ports, Note example
- [quality-gates.md](quality-gates.md) — exact commands and pass criteria
- [git-conventions.md](git-conventions.md) — branch, commit, and push rules
- [pipeline-config.md](pipeline-config.md) — pipeline.yaml schema
