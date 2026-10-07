# Pipeline stages, gates and rollout choices

Adapted and condensed from wshobson/agents by Luodaint. These are design patterns;
verify provider-specific configuration against the target's installed versions.

## Stage contracts

| Stage | Required evidence before continuing | Failure behavior |
| --- | --- | --- |
| Build/test | Source revision, lockfiles, relevant test and scan results | Stop before publication or deployment. |
| Publish | Immutable artifact digest, provenance and scan policy satisfied | Do not substitute an older or unverified artifact silently. |
| Staging | Exact artifact deployed, smoke/integration results | Block promotion; record observed failures. |
| Production gate | Authorized decision or valid metric evaluation | Missing approval or evidence blocks promotion. |
| Rollout | Bounded health and traffic checks | Abort or recover according to the runbook. |
| Verify/recover | Serving version, customer-facing health and data compatibility | Report actual recovery state and escalate unresolved impact. |

Each CI job may start on a fresh runner. Checkout code or download the verified
artifact explicitly; previous jobs' files, environment variables and credentials
are not implicitly available. Pass stage outputs through the provider's supported
mechanism and distinguish artifact identity from a mutable tag.

## Approval and metric gates

- GitHub Actions: reference an environment and configure required reviewers,
  deployment branch/tag restrictions and applicable bypass policy in repository
  settings. The YAML reference alone does not enforce review. Confirm feature
  availability for the repository's visibility and plan.
- GitLab: use the platform's manual/protected-environment approval mechanisms as
  required. A delayed job is a timed start, not a human approval. Confirm whether a
  manual job is blocking and who can execute it.
- Azure Pipelines: configure environment/resource checks and approvals. If using
  a manual validation task, verify its supported job type and timeout settings.
- Automated gates: specify the monitored population, query, baseline, observation
  window, sample-size requirement and acceptable error/latency bounds. Missing
  metrics, zero requests, stale data and evaluation errors must not imply success.

For a stalled promotion, inspect whether the job is waiting for an actual reviewer,
an unreachable dependency, an invalid query or insufficient traffic. A missing
reviewer configuration may leave a deployment unprotected; don't assume every
stalled job is an approval problem. Report the exact gate and evidence.

## Choose a rollout

| Strategy | Conditions to check | Recovery limits |
| --- | --- | --- |
| Rolling | Mixed versions compatible; spare capacity; readiness and draining work | Old/new instances coexist; rollback requires another rollout. |
| Blue-green | Capacity for both versions; real traffic-switch mechanism; warm-up verified | Switching back works only if the old environment stays ready and data compatible. |
| Canary | Traffic routing and enough samples; version-labelled metrics; abort mechanism | Small exposure still has real user impact; absent metrics block promotion. |
| Recreate | Downtime acceptable; state and restart behavior understood | Recovery includes startup time and potentially state repair. |
| Feature flag | Both paths supported; flag service reliable; safe default | Disabling a feature does not undo schema changes or repair bad writes. |

Traffic weights, warm-up time and observation periods are project decisions. Do
not import arbitrary percentages or a fixed five-minute window as universal policy.

## Health and operational checks

Distinguish liveness from readiness and post-deployment user-facing verification.
Liveness should detect a stuck process without restarting every instance because
a shared dependency is down. Readiness should reflect whether an instance can
serve traffic. Deployment verification should exercise critical dependencies and
contracts, error rate, latency and the serving revision.

Choose realistic traffic, bounded timeouts and failure signals. A passing shallow
`/ping` endpoint does not prove the deployed application works. Preserve the
previous artifact and any resources needed to recover until the observation window
has completed. Report inconclusive checks instead of automatically promoting.
