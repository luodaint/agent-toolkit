# Upstream provenance

- Repository: [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill)
- Imported revision: [`c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`](https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8)
- Upstream skill: `skills/security-audit/`
- License: MIT, Copyright (c) 2025-2026 Cloudflare, Inc.; the full original
  notice is preserved in [LICENSE](LICENSE).

## Local adaptation

- Replaced the entrypoint with a concise guide to scope, safety and progressive
  loading. Preserved the full original workflow under
  [references/FULL-AUDIT-WORKFLOW.md](references/FULL-AUDIT-WORKFLOW.md).
- Moved domain and phase documents plus the JSON schema into `references/`.
  References to the original entrypoint's detailed rules now point to the full
  workflow reference. Domain documents continue to use sibling paths.
- Moved both zero-dependency Node.js validators and their tests into `scripts/`.
  Updated schema lookups and documented commands for the new layout; the
  validation logic and upstream test cases are preserved.
- Added an explicit fallback when independent delegation is unavailable. This
  fallback is focused guidance, with no claim of completing the full workflow.
  The original sandbox and evidence requirements remain in force.

The audit workflow belongs to the consuming project. Importing this skill into
the toolkit does not launch an audit or authorize target execution.

## Updates

Review upstream changes against this pinned revision before importing them.
Preserve copyright notices, reapply the layout adaptations, update this revision,
and run toolkit verification plus both validator test suites. Changes that affect
audit evidence contracts or sandbox isolation need a behavioral review as well.
