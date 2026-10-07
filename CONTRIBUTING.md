# Contributing

Issues and pull requests are welcome. Please follow the
[code of conduct](CODE_OF_CONDUCT.md). Report vulnerabilities privately using
the [security policy](SECURITY.md), rather than a public issue.

## Issues

Search existing issues before opening one. For bugs, include the toolkit revision,
agent harness, reproduction steps and expected versus actual behavior. For new
skills or workflow changes, describe a concrete use case and why it belongs in
the shared toolkit. Remove credentials, private prompts and proprietary code
from examples and logs.

## Pull requests

1. Fork the repository and create a branch from `main`.
2. Keep the change focused. Keep project-specific knowledge in the consuming
   project and register new skills as described in [README.md](README.md).
3. Set up a local environment and run validation:

   ```bash
   python3 -m venv .venv
   .venv/bin/python -m pip install -r requirements-dev.txt
   bash -n scripts/verify-toolkit.sh
   PYTHON=.venv/bin/python ./scripts/verify-toolkit.sh
   git diff --check
   ```

4. For instruction changes, try a representative task and explain how behavior
   changes. For script changes, check both valid input and a relevant failure case.
   Security-audit validator changes also require their bundled Node.js test suites
   listed in [README.md](README.md). CI inspector changes require its offline Python
   suite; GitHub Actions example changes need Actions-aware workflow validation.
   Update-script changes require the local Git fixture suite listed in the README.
5. Open a pull request to `main`, explaining the problem, solution, checks actually
   performed and compatibility implications. Draft PRs are welcome.

There is no CI/CD pipeline. Contributors and maintainers run checks locally.
Changes to `main` normally go through a pull request with one approval and resolved
review conversations. New commits invalidate previous approvals. Repository
administrators retain a bypass for maintenance and urgent fixes; any bypass
should record the reason and validation performed.

Reviewers assess behavior, clarity, scope and safety. A successful structural
check alone does not establish that a skill makes good decisions. Maintainers may
request changes or decline workflows that are too broad or project-specific.

## Licensing and provenance

By contributing, you agree that your contribution is available under the
repository's [MIT license](LICENSE), except contributions to imported material
which must preserve that material's applicable license (Apache-2.0 for
`skills/gh-fix-ci/`). Submit only material you have the right to share. Preserve any
required third-party notices and identify the source and license of incorporated
material; consult [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Do not copy private
instructions or proprietary documentation into the toolkit.

AI-assisted contributions are welcome. Contributors remain responsible for
checking their correctness, provenance and safety.
