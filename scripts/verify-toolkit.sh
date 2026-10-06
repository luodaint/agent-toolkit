#!/usr/bin/env bash
set -euo pipefail

toolkit_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
"${PYTHON:-python3}" - "$toolkit_root" <<'PY'
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    sys.exit("Missing PyYAML: install requirements-dev.txt with your Python interpreter.")

root = Path(sys.argv[1]).resolve()
errors = []

def fail(path, message):
    errors.append(f"{path.relative_to(root)}: {message}")

for name in ("README.md", "AGENTS.template.md"):
    if not (root / name).is_file():
        errors.append(f"Missing {name}")

skills = root / "skills"
skill_dirs = sorted(p for p in skills.iterdir() if p.is_dir()) if skills.is_dir() else []
if not skill_dirs:
    errors.append("No skill directories found under skills/")
for directory in skill_dirs:
    path = directory / "SKILL.md"
    if not path.is_file():
        fail(directory, "missing SKILL.md")
        continue
    try:
        content = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", content, re.S)
        if not match:
            raise ValueError("missing YAML frontmatter")
        metadata = yaml.safe_load(match.group(1))
        if not isinstance(metadata, dict):
            raise ValueError("frontmatter must be a mapping")
        name = metadata.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) >= 64:
            raise ValueError("name must be lowercase, hyphenated and under 64 characters")
        if name != directory.name:
            raise ValueError("name must match the skill directory")
        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("description must be a nonempty string")
        if not content[match.end():].strip():
            raise ValueError("skill body must not be empty")
    except (ValueError, yaml.YAMLError, UnicodeError) as error:
        fail(path, str(error))

ignored = {".git", ".venv", "venv", "__pycache__"}
credentials = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    r"|\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"
    r"|\bgh[pousr]_[A-Za-z0-9]{36,}\b"
    r"|\bgithub_pat_[A-Za-z0-9_]{50,}\b"
    r"|\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{32,}\b"
)
for path in sorted(root.rglob("*")):
    if any(part in ignored for part in path.relative_to(root).parts):
        continue
    if path.is_symlink():
        fail(path, "symlinks are not supported in the shared toolkit")
        continue
    if not path.is_file():
        continue
    if path.stat().st_size > 1024 * 1024:
        fail(path, "file exceeds the 1 MiB toolkit limit")
        continue
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeError:
        fail(path, "unexpected binary or non-UTF-8 file")
        continue
    if credentials.search(content):
        fail(path, "possible credential detected (value withheld)")
    if path.suffix != ".md":
        continue
    for target in re.findall(r"\[[^\]\n]*\]\((<[^>\n]+>|[^)\s]+)(?:\s+\"[^\"\n]*\")?\)", content):
        target = target.strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        resolved = (path.parent / unquote(parsed.path)).resolve()
        if not resolved.is_relative_to(root):
            fail(path, f"file link escapes the toolkit: {target}")
        elif not resolved.exists():
            fail(path, f"broken relative file link: {target}")

if errors:
    print("Toolkit verification failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    sys.exit(1)
print(f"Toolkit verified: {len(skill_dirs)} skill(s); metadata, file links, size and credential checks passed.")
PY
