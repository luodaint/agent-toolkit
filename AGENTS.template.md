# Project instructions

Adapt this file as the consuming project's root `AGENTS.md`. Replace the
placeholders with real project details before use.

## Project context

- Purpose: <what this project does>
- Architecture and boundaries: <key modules and allowed dependencies>
- Runtime and dependency policy: <supported versions and dependency constraints>

## Engineering rules

- Follow the established patterns in the affected module; keep changes focused.
- Preserve documented API contracts and data invariants. Explain intentional
  compatibility changes and any migration required.
- Keep credentials out of source control and sensitive data out of logs.
- Enforce authorization at the trusted server boundary where applicable.
- Add meaningful regression coverage for bug fixes. Validate changed behavior
  with the project's relevant checks; report checks that could not be run.
- Preserve unrelated work in the working tree.

## Commands

- Tests: <project test command>
- Lint and formatting: <project lint command>
- Type checking or build: <project validation command>

## Git and operations

- Contribution policy: <branch, commit and pull request conventions>
- Deployment constraints: <environment-specific restrictions>

## Shared workflows and scoped rules

The shared toolkit is mounted at `.agent/toolkit`. For a code review, read
`.agent/toolkit/skills/code-review/SKILL.md` and follow its workflow. Register it
with the harness if automatic skill discovery is desired.

Use `.agent/toolkit/skills/security-audit/SKILL.md` for requested security reviews
and `.agent/toolkit/skills/simplify/SKILL.md` for requested cleanup. Select these
workflows when relevant; a review alone does not authorize edits or a full audit.

Keep project-specific workflows and knowledge in this repository. Use scoped
`AGENTS.md` files for rules specific to a directory; follow the harness's rules
for instruction precedence. Keep detailed workflows in skills instead of
expanding this file into a procedure manual.
