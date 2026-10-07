# Workflow patterns

Adapted and condensed from wshobson/agents by Luodaint. These are examples for a
consuming project, not enabled toolkit workflows. Action pins were verified on
2026-10-07: checkout v7.0.1 and setup-node v7.0.0. Recheck compatibility and pins
when adopting; these action runtimes require Actions Runner 2.327.1 or newer.

## Test an npm application

Assumes a committed `package-lock.json`, `.nvmrc` selecting a supported Node.js
version, and working `lint` and `test` scripts. Change those inputs to the project's
actual toolchain. This workflow uses no deployment secrets and does not publish.

```yaml
name: Test
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: test-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020 # v7.0.0
        with:
          node-version-file: .nvmrc
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm test
```

Use a runtime/OS matrix only for compatibility the project promises. Give required
checks stable job names, and ensure path filters do not leave required checks
permanently pending. Cache package downloads keyed by the lockfile and runtime;
do not promote cached build output from an untrusted PR to a release job.

## Reusable test workflow

The following example belongs in a consuming project's
`.github/workflows/reusable-test.yml`. It deliberately has no required secrets.

```yaml
name: Reusable test
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020 # v7.0.0
        with:
          node-version: ${{ inputs.node-version }}
          cache: npm
      - run: npm ci
      - run: npm test
```

Call it from a job with `uses: ./.github/workflows/reusable-test.yml` and a
`with.node-version` matching the project. External workflow calls need a verified
commit pin. Pass only explicitly needed secrets; prefer avoiding `secrets: inherit`.

## Build, publish and deploy

For Docker publishing, separate a PR build with `push: false` from a trusted release
build. Pin Docker login, metadata and build-push actions to reviewed commits; give
only the publishing job `packages: write`. Login credentials must not reach PR
builds. Record the pushed image digest as a job output or verified release artifact
and deploy that digest across environments instead of rebuilding or using `latest`.

Before generating Kubernetes/cloud deployment jobs, determine provider, target
cluster/account, namespace, artifact identity and existing deploy command. Include
checkout or artifact download on every fresh runner that needs files. Cloud CLI
authentication, cluster credentials and OIDC provider trust are separate setup
requirements. Prefer the project's existing deployment tooling over invented
cluster names or blanket `kubectl apply` commands.

Use a protected environment with configured reviewer/ref restrictions where
required. Serialise deployment jobs with `cancel-in-progress: false`, use bounded
rollout/health waits and provide a rollback path compatible with schema changes.
Keep security report uploads in appropriately privileged jobs; fork PRs may have
different upload capabilities. External scanners and notification services may
transfer private data and require credentials: include them only within task scope.

Consult [GitHub's secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
for trust boundaries and
[deployment environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
for protection rules. Example configuration is not evidence that those settings
exist in the target repository.
