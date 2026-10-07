# Upstream provenance

- Source: [openai/skills gh-fix-ci](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci).
- Revision: `49f948faa9258a0c61caceaf225e179651397431`.
- Imported on: 2026-10-07.
- License: [Apache License 2.0](LICENSE.txt), preserved verbatim from the skill.
  This skill and its local adaptations are distributed under Apache-2.0; the
  toolkit's root MIT license does not replace it. No separate upstream NOTICE file
  was present for this skill or at the repository root in the reviewed revision.

## Local adaptations

Luodaint replaced `SKILL.md` with a concise portable workflow. Diagnosis remains
read-only; an existing fix request authorizes focused repairs without a redundant
approval round. Authentication, sensitive logs, stale runs, external providers and
deployment-capable reruns have explicit handling. Optional upstream plan-skill and
UI/icon dependencies are omitted.

The imported `scripts/inspect_pr_checks.py` retains upstream field and log fallbacks.
Local modifications accept valid check JSON with gh status 1 or 8, preserve JSON
output when no failures exist, include all reported checks, distinguish pending
checks with exit 8, classify cancelled buckets, and restrict log inspection to HTTPS
Actions run URLs on the selected repository and host. Local regression tests cover
these behaviors plus unavailable logs and pending-run job-log fallback.

The helper reads GitHub state only and writes results to stdout/stderr. It does not
redact raw log contents. Inspect output before including excerpts in public issues
or PRs. Exit 0 means no detected failures, not proof all required checks ran.

## Updating

Review changes to the skill, helper and license at a chosen upstream revision.
Merge deliberately with the local modifications, update this pin and notices,
run the inspector's offline tests and toolkit verification, then validate behavior
against a representative PR. Do not replace the helper without preserving URL
scope and check-status handling. See the root README for consuming-submodule updates.
