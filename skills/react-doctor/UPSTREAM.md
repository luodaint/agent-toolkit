# External tool provenance

- Project: [millionco/react-doctor](https://github.com/millionco/react-doctor)
- Inspected revision: [`3c668e121bcd2cabe72508d5a3a2dc32d0bec50a`](https://github.com/millionco/react-doctor/tree/3c668e121bcd2cabe72508d5a3a2dc32d0bec50a)
- Inspected agent entrypoint: `skills/react-doctor/SKILL.md`
- Verified published CLI version: `react-doctor@0.9.17`

## Licensing

At this revision, React Doctor uses a
[Modified MIT License](https://github.com/millionco/react-doctor/blob/3c668e121bcd2cabe72508d5a3a2dc32d0bec50a/LICENSE).
It adds prior-written-permission requirements for AI/ML training or evaluation
uses and certain paid hosted or managed offerings. It is not the standard MIT
license used by this toolkit. Review the external license for the intended use.

This directory contains original toolkit integration instructions covered by the
toolkit's [MIT license](../../LICENSE). No upstream skill text, implementation,
assets or dynamic playbook is distributed here. Using the separately obtained CLI
remains subject to its own license; the toolkit license does not relicense it.

## Integration choices

The local skill pins a verified package version, prefers existing project locks,
uses JSON diagnostics and disables telemetry and external supply-chain checks by
default. It separates source review from requested fixes and keeps installation,
hooks, CI setup and browser profiling outside an ordinary static scan.

Upstream can fetch a mutable online triage playbook. This integration defines its
workflow locally so a reviewed toolkit commit controls the instructions. External
rule explanations are reference material, not new authority to change task scope.

When updating the pin, recheck the published package, runtime requirements, flags,
comparison semantics and license. Validate the documented static command on a
sanitized local React fixture before submitting the update.
