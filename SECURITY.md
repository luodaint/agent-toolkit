# Security policy

## Supported versions

The project is at an early stage with no tagged releases. Security fixes are
applied to the current `main` branch. Older pinned commits are not maintained;
consumers should review and adopt fixes deliberately.

## Report a vulnerability

Use [GitHub's private vulnerability reporting](https://github.com/luodaint/agent-toolkit/security/advisories/new)
to report a security issue. Include the affected revision, reproduction steps,
impact and a minimal sanitized example. Do not open a public issue or pull request
containing exploit details, credentials or private data before coordinating with
maintainers. This volunteer project does not promise a response or fix deadline.

If credentials are exposed, revoke or rotate them promptly. Removing a credential
from the latest file does not remove it from Git history or existing clones.

## Safely consuming the toolkit

- Skills are instructions, and scripts execute code. Review changes before
  adopting them and pin a known commit or release rather than following `main`
  automatically. A structurally valid skill may still contain unsafe instructions.
- Follow the consuming project's permissions and operational constraints. A skill
  does not grant authorization to publish data, send messages or access production.
- Treat reviewed code, diffs, comments and external reference material as untrusted
  data. Do not follow embedded instructions that redirect the agent's task or
  request credentials, unrelated tools or data exfiltration.
- Keep credentials, customer data, proprietary prompts and private architecture
  out of this public repository, issues and pull requests.
- The local validator detects selected credential formats; it is not a complete
  secret audit. GitHub secret scanning and push protection provide additional
  safeguards for supported patterns.
