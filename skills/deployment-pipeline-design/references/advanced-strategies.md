# Progressive delivery and data recovery

Adapted and condensed from wshobson/agents by Luodaint. Use only the sections the
deployment actually needs. No example here authorizes operating a live environment.

## Multi-region promotion

Choose a pilot region and a realistic observation window, then promote to other
regions with a bounded concurrency policy. Verify that the same immutable artifact
and compatible configuration reach every region. Decide whether a pilot failure
halts the entire release or permits a separately approved exception.

Check shared dependencies, replication lag, failover capacity and client routing;
regional isolation is not guaranteed by separate deployment jobs. Keep enough
capacity to serve traffic during recovery. Record which regions changed and the
artifact currently serving in each so a partial release has a concrete runbook.

## Canary analysis

For Argo Rollouts or an equivalent controller, verify the installed API/schema,
traffic-routing integration and analysis provider before generating configuration.
Tie metric queries to service, region and version labels. Compare candidate and
baseline under similar load rather than mixing their metrics into one aggregate.

Define success, failure, inconclusive and evaluation-error behavior. Require a
sample size and reject empty or non-finite results; a ratio with no requests is
not a healthy signal. Set bounded evaluation/rollout timeouts and an abort action.
Exercise those conditions in staging before relying on automatic promotion.

Header-based routing may help internal testing, but user-controlled headers must
not provide access to privileged or less-protected services. Experiments should
state their traffic population and stopping conditions.

## Schema compatibility and recovery

Use expand/contract where practical: add a compatible schema, deploy code that
supports old and new forms, backfill with idempotent resumable operations, then
retire the old form after old application versions and background jobs are gone.
The contraction stage closes the rollback window unless recovery is designed for it.

Reverting an application or switching blue-green traffic does not undo database
changes. Undo scripts are not automatically safe: they can discard data and may
depend on licensed migration-tool features. Prefer backward-compatible application
rollback or a tested forward repair, with recovery ownership and data-loss limits
documented. Backups need a tested restore procedure to be useful recovery evidence.

Check database-specific locking, transaction and replication behavior. For example,
PostgreSQL concurrent index creation has transaction and failure-cleanup constraints;
it is not a universal guarantee of a safe migration. Validate the actual migration
against the target database version and representative data volume.

## Freeze windows and notifications

Use the project's actual calendar, timezone, emergency policy and owners. A local
boolean environment variable is not a trustworthy authorization gate for a freeze
override. Record and restrict any exception through the platform's reviewed policy.

If notifications are requested, use a structured payload and quote/encode event
data. Include the actual serving artifact and result; do not claim rollback occurred
merely because the deployment failed. Redact secrets and keep unrequested messages
out of the workflow.
