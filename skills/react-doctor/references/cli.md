# CLI use and interpretation

These examples were checked against React Doctor `0.9.17`. Its package supports
Node.js `^20.19.0 || >=22.13.0`. Use the consuming project's package manager and
locked installation when present; confirm its version and help if different.

## Static scans

Run from the React application root. The fallback `npx --yes` may download the
specified package and dependencies into npm's cache; it does not add a dependency
to the project's manifest. The first `--yes` belongs to npm, not React Doctor.
Use it only when package retrieval is permitted. A locally installed binary can
replace `npx --yes react-doctor@0.9.17` in the examples.

Full scan:

```bash
npx --yes react-doctor@0.9.17 . --json --scope full \
  --blocking none --no-telemetry --no-supply-chain
```

Branch or local-change review, with a base that exists in the target repository:

```bash
react_base='<verified-base-ref>'
npx --yes react-doctor@0.9.17 . --json --scope changed --base "$react_base" \
  --include-untracked --blocking none --no-telemetry --no-supply-chain
```

Replace the placeholder before execution. For local edits, use the current branch
name as the base; for a feature branch, use the verified target branch. Confirm the
reported comparison base and scope rather than assuming the CLI selected them.

For named files, replace `.` with their paths and use `--scope full` to inspect
those files without a regression comparison. For workspace projects, point at the
specific application directory or consult `--help` for `--project` selection.

- `--json` emits structured diagnostics and avoids interactive scan prompts.
- `--blocking none` makes diagnostics advisory; it does not establish that the
  scan succeeded. Check the returned errors, diagnostics and completion state.
- `--no-telemetry` disables telemetry, remote scoring and share-link services.
  Do not expect a numeric score with this option.
- `--no-supply-chain` disables external dependency-health checks. This is a
  deliberate coverage limit; the scan is not a supply-chain audit.
- These flags do not create a network sandbox. npm downloads and executable
  project configuration or plugins can still require additional controls.

Keep JSON in the conversation or a permitted local artifact directory if saving
it. Reports may contain private source paths and code details. Do not automatically
upload reports, run the tool's installer or install CI integration.

## Comparison limits

`--scope changed` compares findings grouped by rule and file between the base and
the current scan. It reports increases in each group's count, with matching used
to locate the likely added findings. Replacing a fixed issue with a new issue under
the same rule in the same file can leave the count unchanged and hide a regression.
Use direct code inspection or a full scan when that limitation matters.

Use `--scope lines` for findings on changed lines, or `--scope files` for all findings
in changed files, when those are the desired reporting semantics. Untracked files
require `--include-untracked` in comparison scopes; ignored files remain excluded.

For repeated comparisons, a full JSON report can be supplied using `--baseline`.
Keep the same tool version, rules, scan options and source-dependent filter
settings. A prior comparison result is not a full baseline. Regenerate baselines
after changing configuration and report any partial scans or skips.

## Rules and requested configuration changes

Explain a reported rule:

```bash
npx --yes react-doctor@0.9.17 rules explain react-doctor/no-array-index-as-key \
  --no-telemetry
```

Check that the example rule matches the diagnostic. Rule configuration commands
can write `doctor.config.*` or `package.json`; inspect existing configuration and
use the narrowest requested change. Consult `rules --help` from the same version
before editing. A scan alone does not authorize rule suppression.
