# Pipeline Config Reference

## pipeline.yaml location

Place `pipeline.yaml` in the workspace root (the directory you open in Cursor).

The pipeline will not start without this file.

## Schema

```yaml
main_branch: main          # required — branch to sync all repos to
auto_push: false           # optional — if false (default), wait for user OK before git-shipper
obsidian_vault: /absolute/path/to/vault   # optional — skip docs stage if missing

repos:                     # required, non-empty
  - name: billing          # human-readable name used in reports
    path: ../billing       # relative to this file, or absolute
  - name: auth
    path: /Users/me/projects/auth
```

## Rules

- `path` is resolved relative to the **directory containing `pipeline.yaml`**
- Each path must be a git repository root with `origin`
- The pipeline touches only the repos listed here
- `obsidian_vault`, if set, must be an existing directory; otherwise docs are skipped
- `auto_push: true` ships without asking; keep `false` unless you trust unattended push

## Plan artifact

The orchestrator writes `.pipeline/<TASK_ID>.md` in the workspace (not in service repos). Gitignored. Auditors and rework read this file.

## pipeline.yaml.example

See `pipeline.yaml.example` in the repository root.
