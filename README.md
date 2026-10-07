# Agent Toolkit

Shared instructions and focused workflows for AI coding agents. The toolkit
includes code review, security auditing and focused code simplification.

Available under the [MIT license](LICENSE). Contributions through
[issues](https://github.com/luodaint/agent-toolkit/issues) and
[pull requests](https://github.com/luodaint/agent-toolkit/pulls) are welcome;
see [CONTRIBUTING.md](CONTRIBUTING.md) and the
[code of conduct](CODE_OF_CONDUCT.md). Report vulnerabilities privately using
the [security policy](SECURITY.md).

## Structure

```text
agent-toolkit/
├── README.md
├── AGENTS.template.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── THIRD_PARTY_NOTICES.md
├── .github/
│   ├── CODEOWNERS
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
├── requirements-dev.txt
├── skills/
│   ├── code-review/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── findings.md
│   ├── security-audit/
│   │   ├── SKILL.md
│   │   ├── LICENSE
│   │   ├── UPSTREAM.md
│   │   ├── references/
│   │   └── scripts/
│   └── simplify/
│       ├── SKILL.md
│       └── UPSTREAM.md
└── scripts/
    └── verify-toolkit.sh
```

## What goes where

- **AGENTS.md:** persistent rules for the consuming project. Adapt
  [AGENTS.template.md](AGENTS.template.md); keep architecture, commands and
  project-specific knowledge in that project. More specific instructions can
  live in `backend/AGENTS.md`, `frontend/AGENTS.md` or other scoped directories.
- **Skills:** repeatable workflows with a focused purpose and trigger description.
- **References:** supporting details read only when relevant. The review skill
  loads its findings reference when preparing the review report.
- **Scripts:** deterministic checks, separate from agent reasoning.

The toolkit uses plain Markdown and YAML metadata. Register skills using your
agent harness's supported discovery mechanism, or explicitly ask the agent to
read a skill. Checking out this repository alone does not activate its skills.

## Available skills

| Skill | Purpose | Output and requirements |
| --- | --- | --- |
| [code-review](skills/code-review/SKILL.md) | Review changes for correctness and regressions. | Read-only findings unless fixes are requested. |
| [security-audit](skills/security-audit/SKILL.md) | Investigate security boundaries or run a comprehensive audit. | Focused guidance is conversational. Full audits require independent subagents, local Node.js and an external writable artifact directory. Target-code execution additionally requires every upstream sandbox control. |
| [simplify](skills/simplify/SKILL.md) | Improve reuse, clarity and efficiency within a requested change. | Applies justified edits when cleanup is requested; preserves behavior and validates relevant contracts. Delegation is optional. |

The security audit skill includes Cloudflare's phase and domain references,
findings schema, deterministic validators and their tests. Its concise entrypoint
loads the full workflow only when appropriate. See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for upstream attribution and
licensing, and each imported or inspired skill's `UPSTREAM.md` for its pinned source
revision and local adaptations.

These workflows compose when the task calls for them. A code review does not
automatically launch a full audit or authorize simplification edits.

## Use in a project

### Git submodule (recommended for explicit version pinning)

```bash
git submodule add https://github.com/luodaint/agent-toolkit.git .agent/toolkit
cp .agent/toolkit/AGENTS.template.md AGENTS.md
```

Adapt the template before use; merge its relevant sections if an `AGENTS.md`
already exists. The parent repository records the exact toolkit commit.
Example prompt:

> Review my current changes using `.agent/toolkit/skills/code-review/SKILL.md`.

Other example prompts:

> Review the authorization change using `.agent/toolkit/skills/security-audit/SKILL.md`.

> Simplify my current change using `.agent/toolkit/skills/simplify/SKILL.md`, preserving behavior.

For a full audit, specify the target, desired scope and a permitted output path
outside the target repository. The workflow keeps unresolved runtime claims as
needing validation when the required sandbox is unavailable.

### Git subtree

```bash
git subtree add --prefix=.agent/toolkit \
  https://github.com/luodaint/agent-toolkit.git <commit-or-tag> --squash
```

Subtrees include the files in normal clones without submodule setup, but require
explicit subtree updates and make upstream contributions less direct. Replace
`<commit-or-tag>` with an actual published revision.

### CI checkout

```bash
git clone https://github.com/luodaint/agent-toolkit.git .agent/toolkit
git -C .agent/toolkit checkout --detach <commit-or-tag>
```

Pin a reviewed commit or published tag. Avoid silently following `main` across
projects: instruction changes can change agent behavior. No release tags are
published by this scaffold; use a commit until releases exist.

Keep project-specific skills in the consuming repository, separate from this
shared toolkit. Shared skills should not embed project secrets or private context.

## Add a skill or reference

1. Create `skills/<lowercase-hyphenated-name>/SKILL.md` with YAML frontmatter
   containing `name` (matching its directory) and a nonempty `description`
   explaining what it does and when to use it.
2. Keep the workflow concise. Add detailed material under that skill's
   `references/` directory only when useful; link it relatively and say when to
   read it. Add shared technology references later if multiple skills need them.
3. Run verification and try the skill on a representative task. Compose workflows
   conditionally when relevant; avoid requiring every skill for every task.

Review shared changes before updating consumers. Use semantic release tags once
releases begin, treating incompatible workflow changes as major versions. Update
consumer pins deliberately through their normal review process.

## Verify

Requires Bash, Python 3.9+ and PyYAML:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
PYTHON=.venv/bin/python ./scripts/verify-toolkit.sh
```

For security-audit validator changes, also run the bundled upstream suites with
Node.js 22 or newer; no npm dependencies are needed:

```bash
node --test skills/security-audit/scripts/validate-findings.test.cjs \
  skills/security-audit/scripts/validate-coverage-ledger.test.cjs
```

Verification checks required files, skill metadata, inline Markdown file links,
files over 1 MiB and common credential patterns. It ignores Git metadata and local
virtual environments. Credential checks are a basic guard, not a comprehensive
secret audit; link checks cover inline file links, not external URLs or anchors.

Checks run locally; this repository has no CI/CD pipeline. Review instructions and
scripts before adopting updates, and keep credentials and private information out
of public contributions. See [SECURITY.md](SECURITY.md) for consumer guidance.

Future workflows and technology references can be added incrementally. Imported
material must have redistribution permission, preserved notices and a recorded
upstream revision; general workflow ideas can be implemented in original wording.
