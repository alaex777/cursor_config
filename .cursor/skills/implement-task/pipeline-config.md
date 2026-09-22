# Pipeline Config Reference

## pipeline.yaml location

Place `pipeline.yaml` in the workspace root (the directory you open in Cursor).

The pipeline will not start without this file.

## Schema

```yaml
main_branch: main          # branch to sync all repos to
obsidian_vault: /absolute/path/to/vault   # path to Obsidian vault for docs stage

repos:
  - name: billing          # human-readable name used in reports
    path: ../billing       # relative to this file, or absolute
  - name: auth
    path: /Users/me/projects/auth
```

## Rules

- `path` is resolved relative to `pipeline.yaml` if it starts with `../` or `./`
- Each path must be a git repository root
- The pipeline touches only the repos listed here
- Obsidian vault path must be absolute

## pipeline.yaml.example

See `pipeline.yaml.example` in the repository root for a ready-to-copy template.
