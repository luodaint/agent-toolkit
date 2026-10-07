# Upstream provenance

- Source: [wshobson/agents deployment-pipeline-design](https://github.com/wshobson/agents/tree/46891e7e60da0e52baf1050b7b6391b64e84c6d9/plugins/cicd-automation/skills/deployment-pipeline-design).
- Revision: `46891e7e60da0e52baf1050b7b6391b64e84c6d9`.
- Imported on: 2026-10-07.
- License: [MIT](LICENSE), Copyright (c) 2024 Seth Hobson; copied verbatim from
  the upstream repository root.

## Local adaptations

Luodaint rewrote the entrypoint and condensed both upstream references into focused
stage/gate/rollout guidance and conditional progressive-delivery/data-recovery
patterns. Platform-specific examples with incomplete dependencies, credential
setup or recovery assumptions were replaced with explicit design contracts.

The adaptation distinguishes timed starts from approvals, named environments from
configured protection rules, and application rollback from data recovery. It removes
unconditional zero-downtime claims and arbitrary rollout thresholds, requires valid
metric evidence, and considers mixed versions, capacity, readiness and connection
draining. Multi-region, migration, freeze and notification guidance preserves the
consuming project's requirements and existing authorization.

No provider SDK, deployment script or executable pipeline is bundled. Implementation
must use the consuming project's platform versions, commands and validation tools.

## Updating

Review the upstream entrypoint, both references and license at a chosen revision.
Merge relevant improvements without restoring unsafe assumptions, verify any
provider-specific syntax against current official documentation, and update this
pin. Run toolkit validation and assess a representative delivery design. See the
root README for consuming-submodule updates.
