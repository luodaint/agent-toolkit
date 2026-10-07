# Upstream provenance

- Source: [wshobson/agents github-actions-templates](https://github.com/wshobson/agents/tree/46891e7e60da0e52baf1050b7b6391b64e84c6d9/plugins/cicd-automation/skills/github-actions-templates).
- Revision: `46891e7e60da0e52baf1050b7b6391b64e84c6d9`.
- Imported on: 2026-10-07.
- License: [MIT](LICENSE), Copyright (c) 2024 Seth Hobson; copied verbatim from
  the upstream repository root.

## Local adaptations

Luodaint rewrote and condensed the entrypoint and moved selected testing/reusable
workflow patterns into `references/workflow-patterns.md`. Docker publishing,
Kubernetes deployment, scanners and notifications are conditional design guidance
instead of automatic cloud operations or third-party integrations.

Examples replace dated action tags with verified full commit pins for official
checkout v7.0.1 and setup-node v7.0.0, use the project's declared Node.js version,
explicit read permissions and non-persisted checkout credentials. Trust-boundary
guidance covers fork PRs, privileged triggers/runners, caches/artifacts, shell input,
OIDC and environment protection settings. These are consumer examples; this import
adds no `.github/workflows/` files to the toolkit.

Pins were checked against [checkout's release](https://github.com/actions/checkout/releases/tag/v7.0.1)
and [setup-node's release](https://github.com/actions/setup-node/releases/tag/v7.0.0)
on the import date. Verify action and runner compatibility when adopting them.

## Updating

Review upstream skill and license changes at a chosen revision. Merge relevant
patterns into the local adaptation, independently verify action pins and supported
runtimes, and update this source pin. Validate example workflows with Actions-aware
tooling and toolkit checks. See the root README for consuming-submodule updates.
