# AGENTS.md

Instructions for AI agents and automated tooling working in this repository.

## 1. Plan before changing

- **Always plan before making any change.** Present a plan (files to touch,
  approach, expected impact) and obtain **explicit approval** before editing.
- Do **not** modify files until the plan has been explicitly approved. When in
  doubt, ask rather than act.

## 2. Python version compatibility

- This is a library. All code must remain compatible with **every currently
  supported version of Python**.
- The declared floor is `requires-python = ">=3.9"` (see `pyproject.toml`).
  Write code that also runs on all still-supported versions at or above that
  floor — avoid syntax or APIs newer than the lowest supported version.
- Do not introduce version-specific branches, new-er syntax, or dependency
  requirements that drop support for any still-supported Python.

## 3. Keep it clean and lean — but do not delete unused code

- Aim to keep the codebase clean and lean, since this is a library.
- However, **do not remove code that merely appears unused.** Such code is
  intentionally retained (public API, extension points, or general-purpose
  helpers) and may be used by downstream consumers.
- Instead of deleting, **document seemingly unused code as MISC tools**: mark it
  clearly (e.g. a `MISC` section/comment or docstring note) so its purpose is
  discoverable without deleting it.
