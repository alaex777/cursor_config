# Git Conventions Reference

## Branch naming

```
feat/<TASK_ID>-<kebab-slug>    # new functionality
fix/<TASK_ID>-<kebab-slug>     # bug fix
```

Examples:
- `feat/ABC-123-return-note-by-id`
- `fix/ABC-456-handle-missing-user-on-login`

Sanitize `TASK_ID` before using it in a branch name:

- Strip a leading `#` (`#42` → `42`)
- Replace any character outside `[A-Za-z0-9._-]` with `-`
- Collapse repeated `-`

Slug: lowercase, hyphens, ≤ 6 words, derived from the task title. No `/` inside the slug.

## Commit message (Conventional Commits)

```
<type>(<scope>): <imperative short description>

<optional body>

Refs: <TASK_ID>
```

- `type`: `feat` / `fix` / `refactor` / `test` / `chore`
- `scope`: service or module name (e.g. `notes`, `billing`, `auth`)
- Subject line: imperative mood, English, ≤ 72 chars
- Body: what and why (not how), wrapped at 72 chars
- Footer always includes `Refs: <TASK_ID>` (original id, including `#` if the user used it)

Examples:
```
feat(notes): return note by id on GET /notes/{note_id}

Add Note entity, async NoteRepository port, SQLAlchemy adapter,
and GetNoteById use case.

Refs: ABC-123
```

```
fix(auth): prevent login with expired token

TokenValidator now checks expiry timestamp before returning
the decoded payload.

Refs: ABC-456
```

## Staging

Stage only source and project files:

```bash
git add -- src tests pyproject.toml README.md scripts .github
```

Never `git add -A`. Never stage `.venv`, `.env`, `.env.*`, caches, secrets, or `uv.lock` changes the task did not require.

## Push

Never commit or push while `HEAD` is `main` or `master`. Create (or switch to) the feature branch first, then verify:

```bash
git branch --show-current   # must not be main/master
git push -u origin HEAD
```

- Never `--force` or `--force-with-lease`
- Never `--no-verify`
- Never `--amend` after push
