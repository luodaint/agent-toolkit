---
name: github-actions-templates
description: Create or improve GitHub Actions workflows for testing, building, reusable jobs and authorized releases. Use when a task calls for workflow configuration or GitHub Actions templates.
---

# GitHub Actions templates

Adapted from wshobson/agents; see [UPSTREAM.md](UPSTREAM.md) and [LICENSE](LICENSE).

## Fit the consuming project

Inspect existing workflows, package scripts, lockfiles, supported runtimes, branch
rules and release process. Reuse the project's real commands. Establish which
events should test code and which trusted events may publish or deploy. A request
for templates authorizes preparing configuration; executing deployments, changing
repository settings or sending notifications requires corresponding authorization.

For concrete testing, reusable-job and publishing patterns, read
[references/workflow-patterns.md](references/workflow-patterns.md). Adapt examples
to the target before proposing them. Adding this skill does not enable a pipeline.

## Preserve trust boundaries

- Give `GITHUB_TOKEN` explicit minimal permissions. Grant package publishing,
  security uploads or `id-token: write` only to the jobs that need them.
- Run untrusted PR tests without deployment credentials or privileged runner
  access. Do not execute PR head code in `pull_request_target` or a privileged
  `workflow_run` context. Use GitHub-hosted runners for public PRs unless the
  project has a reviewed isolation design.
- Pin actions and external reusable workflows to verified full commit SHAs. Check
  supported runner/runtime versions and update pins deliberately. Don't copy an
  old upstream runtime matrix or a floating `latest` release.
- Treat PR text and other event values as untrusted input. Pass them through
  environment variables and quote shell arguments instead of interpolating them
  directly into `run:` scripts. Don't put secrets in caches, artifacts or logs.
- Prefer short-lived OIDC credentials where the deployment platform supports them,
  with a trust policy bound to the intended repository, ref or environment. OIDC
  permission alone does not configure the provider's trust policy.
- Reference protected environments for deployments and report required settings
  separately. `environment: production` alone does not create reviewer gates.
  Serialise production deployments; don't cancel one midway through a mutation.

## Validate and deliver

Check YAML with an Actions-aware linter such as the project's installed actionlint;
ordinary YAML parsing does not validate Actions expressions or job dependencies.
Run affected local commands when practical. Check reusable workflow input/secret
contracts, event/ref filters, artifact handoff and permission boundaries, including
fork PR behavior. Don't claim a remote run passed without observing it.

Deliver focused workflow changes, explain triggering events and required external
settings, and report validation and limits. Separate registry publishing from PR
testing. Choose security scans that fit the project instead of adding every service.
For requested rollout architecture, optionally use the toolkit's
[deployment-pipeline-design](../deployment-pipeline-design/SKILL.md) workflow.
