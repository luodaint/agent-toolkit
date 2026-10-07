# Third-party notices

## Cloudflare security audit

The documents, schema, validators and tests in `skills/security-audit/` are adapted
from [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill)
at revision `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`.
They are licensed under MIT, Copyright (c) 2025-2026 Cloudflare, Inc.

The complete upstream license is included at
[skills/security-audit/LICENSE](skills/security-audit/LICENSE), and local changes
are recorded in [skills/security-audit/UPSTREAM.md](skills/security-audit/UPSTREAM.md).
Preserve this notice and the upstream license when redistributing that skill.
The repository's own [MIT license](LICENSE) applies to original toolkit material.

## Simplification workflow

[AbdoKnbGit/opencode-simplify](https://github.com/AbdoKnbGit/opencode-simplify)
inspired the general cleanup concept. Its reviewed revision had no license grant;
its text, code and media are not distributed here. The local implementation and
provenance are described in [skills/simplify/UPSTREAM.md](skills/simplify/UPSTREAM.md).

## React Doctor integration

The integration in `skills/react-doctor/` contains original toolkit instructions
for the external [millionco/react-doctor](https://github.com/millionco/react-doctor)
CLI. No upstream code, skill text or assets are bundled. At the inspected revision,
the external tool uses a Modified MIT License with additional restrictions on
AI/ML training/evaluation and certain commercial hosted or managed uses.

The toolkit's MIT license applies to its own integration instructions and does not
override the external tool's license. The source revision, verified package version
and license link are recorded in
[skills/react-doctor/UPSTREAM.md](skills/react-doctor/UPSTREAM.md).

## OpenAI CI troubleshooting

`skills/gh-fix-ci/` is adapted from
[openai/skills](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci)
at revision `49f948faa9258a0c61caceaf225e179651397431`. The skill and its adapted
Python inspector are distributed under the
[Apache License 2.0](skills/gh-fix-ci/LICENSE.txt), with local changes recorded in
[UPSTREAM.md](skills/gh-fix-ci/UPSTREAM.md) and identified in the modified files.
Keep that license and the provenance/modification notices when redistributing it.
The root MIT license does not replace this skill's license.

## wshobson CI/CD skills

`skills/github-actions-templates/` and `skills/deployment-pipeline-design/` are
adapted from [wshobson/agents](https://github.com/wshobson/agents/tree/46891e7e60da0e52baf1050b7b6391b64e84c6d9/plugins/cicd-automation/skills)
at revision `46891e7e60da0e52baf1050b7b6391b64e84c6d9`. Upstream material uses MIT,
Copyright (c) 2024 Seth Hobson. The complete upstream license is preserved in
[github-actions-templates/LICENSE](skills/github-actions-templates/LICENSE) and
[deployment-pipeline-design/LICENSE](skills/deployment-pipeline-design/LICENSE).
Preserve these notices and licenses when redistributing the adaptations. Local
changes are described in each skill's `UPSTREAM.md`.
