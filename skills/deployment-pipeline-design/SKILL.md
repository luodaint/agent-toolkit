---
name: deployment-pipeline-design
description: Design or improve multi-stage delivery pipelines, environment promotion, approval gates, progressive rollouts and recovery. Use for requested deployment architecture or troubleshooting promotion gates.
---

# Deployment pipeline design

Adapted from wshobson/agents; see [UPSTREAM.md](UPSTREAM.md) and [LICENSE](LICENSE).

## Establish the delivery contract

Use project evidence to identify the application, CI provider, deployment platform,
environment topology, immutable artifact identity, availability needs, recovery
objectives and monitoring signals. Preserve existing platform choices. Resolve
missing decisions that affect production before finalizing the design; continue
independent design work with clearly stated assumptions.

Choose the smallest stage graph that meets the requirements: build and test,
publish a verified artifact, deploy to staging, validate, gate production, roll out,
verify and recover. Build once and promote the same digest or version. Define each
stage's inputs, outputs, credentials, dependencies, timeout and failure behavior.

For rollout selection, approval semantics and health checks, read
[references/details.md](references/details.md). For multi-region delivery, canary
analysis and schema recovery, read
[references/advanced-strategies.md](references/advanced-strategies.md) only when
relevant. These references replace the upstream worked examples.

## Make promotion and recovery explicit

- State where human approval or automated metrics gate promotion, who owns the
  decision and what missing/invalid signals do. A delay is not an approval, and a
  named environment does not configure protection rules by itself.
- Keep untrusted source execution separate from release credentials and privileged
  runners. Use least privilege and short-lived provider credentials where supported.
- Select rolling, canary or blue-green based on capacity, compatibility, traffic
  control and observability. Don't promise zero downtime without checking readiness,
  connection draining, data migrations and mixed-version behavior.
- Define health signals, observation windows, abort thresholds and recovery steps
  before promotion. Database changes may survive an application rollback; preserve
  backward compatibility or provide a reviewed forward-repair plan.
- Serialise conflicting environment mutations and bound retries. Don't bypass
  failed gates, silence monitoring or repeat deployment attempts without evidence.

## Deliver within authorization

For design requests, deliver the stage graph, rollout rationale, gates, credential
boundaries, monitoring and recovery runbook. For requested implementation, prepare
focused configuration and validate it using the provider's supported tooling and
the project's local checks. Identify environment/provider settings that need
separate configuration and report which checks actually ran.

Designing or editing a pipeline does not itself authorize launching deployments,
promoting traffic, changing protection rules, applying migrations or notifying
external recipients. Follow existing session authorization and project policy for
those actions. For GitHub workflow syntax, optionally use
[github-actions-templates](../github-actions-templates/SKILL.md).
