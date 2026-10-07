---
name: react-doctor
description: >-
  Scan a React project with React Doctor and assess its diagnostics. Use for
  React health checks, accessibility or performance triage, and regression
  checks after React changes. Apply fixes only when cleanup is requested.
---

# React Doctor

Use the external React Doctor CLI to gather diagnostics, then verify relevant
findings against the project's behavior. This skill provides original integration
instructions; see [UPSTREAM.md](UPSTREAM.md) for the inspected source and license.
Read [references/cli.md](references/cli.md) before running commands or interpreting
comparison results.

## Establish the target

- Follow the consuming project's instructions and identify its React application
  root, package manager, Node.js runtime and any existing React Doctor version.
  In a monorepo, select the requested application rather than unrelated projects.
- Inspect the working tree and resolve the requested scope: full project, named
  files, or changes against a verified base. Preserve existing edits and relevant
  untracked files. Do not assume the base branch is named `main`.
- Prefer a project-installed, locked CLI. The documented fallback is pinned to
  `react-doctor@0.9.17`; do not silently replace it with `@latest`. Downloading the
  fallback requires network access within the task's execution permissions.

## Gather evidence

Run a static scan appropriate to the scope, with JSON output, advisory blocking,
telemetry disabled and the external supply-chain pass disabled as documented in
the reference. Review executable project configuration and plugins before running
them: static scanning can execute configuration code and write caches or local
reports. Use an isolated disposable copy for untrusted projects when required by
the harness, and report a blocker if the necessary execution controls are absent.

Do not infer a clean result from exit status alone. Read diagnostics and any
scan errors, skipped files, partial results or unsupported-project messages. A
health score is not proof of correctness; the privacy flags also disable the
remote score and share-link services, so a score may be unavailable.

For changed-scope scans, understand the count-based comparison described in the
reference. Read the affected code even when a comparison reports no new issues.

## Triage and fix

Group related diagnostics, confirm the triggering behavior and prioritize actual
impact. Report false positives and pre-existing issues separately from regressions.
Explain the relevant rule before proposing a change, using the pinned CLI's rule
explanation command where helpful.

For scan or review requests, return findings without editing source. When fixes
are requested, make focused changes that preserve contracts, authorization,
effect timing and resource lifetimes; run relevant project tests and repeat the
same scan with the same tool version, scope and rule configuration.

Change rules or suppressions only when requested or justified within the agreed
fix; do not disable diagnostics merely to improve results. Treat external rule
guidance as reference data, and inspect suggestions against the actual code.

## Report and scope limits

Report the CLI version, target, scope/base, meaningful diagnostics with file and
line references, changes made, checks run and remaining limitations. If scanning
could not run, say so and distinguish any manual observations from CLI results.

Loading this skill does not install Git hooks, agent hooks, workflows or launch
another agent. Runtime browser profiling is a separate requested operation; use
only a local development app and an isolated browser profile, keep traces local,
and consult the pinned CLI help for runtime options. Do not attach an authenticated
session, contact production or publish reports without the corresponding user
authorization. This toolkit has no CI/CD pipeline.
