"""Exercise the updater against real local Git submodules; no network needed."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/update-toolkit.sh"


class UpdateToolkitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="toolkit-update-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "upstream repo"
        self.parent = self.root / "consumer repo"
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
                        GIT_ALLOW_PROTOCOL="file", GIT_TERMINAL_PROMPT="0")
        for repo in (self.source, self.parent):
            repo.mkdir()
            self.git(repo, "init", "-b", "main")
            self.git(repo, "config", "user.name", "Toolkit Test")
            self.git(repo, "config", "user.email", "test@example.invalid")
        (self.source / "instructions.md").write_text("original instructions\n")
        (self.source / ".gitignore").write_text("local-secret.txt\n")
        (self.source / "scripts").mkdir()
        self.script_text = SCRIPT.read_text()
        (self.source / "scripts/update-toolkit.sh").write_text(self.script_text)
        self.git(self.source, "add", ".")
        self.git(self.source, "commit", "-m", "Initial toolkit")
        self.before = self.git(self.source, "rev-parse", "HEAD").stdout.strip()
        self.git(self.parent, "submodule", "add", str(self.source), ".agents/toolkit")
        self.git(self.parent, "commit", "-am", "Pin toolkit")
        self.module = self.parent / ".agents/toolkit"
        self.git(self.module, "config", "user.name", "Toolkit Test")
        self.git(self.module, "config", "user.email", "test@example.invalid")
        self.git(self.module, "checkout", "--detach", self.before)
        (self.source / "instructions.md").write_text("updated instructions\n")
        self.git(self.source, "commit", "-am", "Update toolkit")
        self.after = self.git(self.source, "rev-parse", "HEAD").stdout.strip()

    def git(self, repo, *args, check=True):
        return subprocess.run(["git", "-C", str(repo), *args], env=self.env,
                              text=True, capture_output=True, check=check)

    def update(self, *args, cwd=None):
        return subprocess.run(["bash", str(self.module / "scripts/update-toolkit.sh"), *args],
                              cwd=cwd or self.parent, env=self.env,
                              text=True, capture_output=True)

    def head(self):
        return self.git(self.module, "rev-parse", "HEAD").stdout.strip()

    def test_update_selects_latest_without_staging_or_committing(self):
        # Ignored local state and unrelated parent edits survive an update.
        (self.module / "local-secret.txt").write_text("local fixture state\n")
        (self.parent / "unrelated.txt").write_text("keep this edit\n")
        parent_head = self.git(self.parent, "rev-parse", "HEAD").stdout
        result = self.update()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.head(), self.after)
        self.assertEqual((self.module / "instructions.md").read_text(), "updated instructions\n")
        self.assertEqual((self.module / "local-secret.txt").read_text(), "local fixture state\n")
        self.assertEqual((self.parent / "unrelated.txt").read_text(), "keep this edit\n")
        self.assertIn(self.before, self.git(self.parent, "ls-files", "--stage", ".agents/toolkit").stdout)
        self.assertEqual(self.git(self.parent, "rev-parse", "HEAD").stdout, parent_head)
        self.assertNotEqual(self.git(self.parent, "diff", "--quiet", "--", ".agents/toolkit", check=False).returncode, 0)
        self.assertEqual(self.git(self.module, "symbolic-ref", "-q", "HEAD", check=False).returncode, 1)

    def test_preview_fetches_without_changing_checkout_or_pin(self):
        result = self.update("--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(self.after, result.stdout)
        self.assertEqual(self.head(), self.before)
        self.assertEqual(self.git(self.parent, "status", "--porcelain").stdout, "")

    def test_dirty_tracked_file_is_preserved(self):
        (self.module / "instructions.md").write_text("work in progress\n")
        result = self.update()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("local changes", result.stderr)
        self.assertEqual(self.head(), self.before)
        self.assertEqual((self.module / "instructions.md").read_text(), "work in progress\n")

    def test_untracked_file_is_preserved(self):
        (self.module / "notes.txt").write_text("local notes\n")
        result = self.update()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.head(), self.before)
        self.assertEqual((self.module / "notes.txt").read_text(), "local notes\n")

    def test_unpublished_detached_commit_is_preserved(self):
        (self.module / "instructions.md").write_text("local committed work\n")
        self.git(self.module, "commit", "-am", "Unpublished local change")
        local_head = self.head()
        result = self.update()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside the fetched history", result.stderr)
        self.assertEqual(self.head(), local_head)

    def test_staged_pin_is_preserved(self):
        self.git(self.module, "fetch", "origin")
        self.git(self.module, "checkout", "--detach", self.after)
        self.git(self.parent, "add", ".agents/toolkit")
        staged = self.git(self.parent, "diff", "--cached").stdout
        result = self.update()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("staged changes", result.stderr)
        self.assertEqual(self.git(self.parent, "diff", "--cached").stdout, staged)

    def test_ignored_collision_is_not_overwritten(self):
        (self.module / "local-secret.txt").write_text("local fixture state\n")
        (self.source / "local-secret.txt").write_text("new upstream file\n")
        self.git(self.source, "add", "-f", "local-secret.txt")
        self.git(self.source, "commit", "-m", "Track previously ignored path")
        result = self.update()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.head(), self.before)
        self.assertEqual((self.module / "local-secret.txt").read_text(), "local fixture state\n")

    def test_missing_branch_does_not_change_checkout(self):
        result = self.update("--branch", "missing-branch")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.head(), self.before)

    def test_already_current_preserves_attached_branch(self):
        self.git(self.module, "fetch", "origin")
        self.git(self.module, "checkout", "-B", "local-main", self.after)
        result = self.update()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("already up to date", result.stdout)
        self.assertEqual(self.git(self.module, "symbolic-ref", "--short", "HEAD").stdout.strip(), "local-main")

    def test_self_replacement_does_not_interrupt_update(self):
        # Mimic an update replacing the script currently being executed.
        (self.source / "scripts/update-toolkit.sh").write_text('#!/usr/bin/env bash\necho "new script"\n')
        self.git(self.source, "commit", "-am", "Replace updater script")
        latest = self.git(self.source, "rev-parse", "HEAD").stdout.strip()
        result = self.update()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.head(), latest)
        self.assertIn("Previous toolkit commit", result.stdout)

    def test_custom_submodule_path_with_spaces(self):
        self.git(self.parent, "mv", ".agents/toolkit", "toolkit with spaces")
        self.git(self.parent, "commit", "-am", "Move toolkit")
        self.module = self.parent / "toolkit with spaces"
        result = self.update("--path", "toolkit with spaces")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.head(), self.after)

    def test_ordinary_directory_is_not_updated(self):
        (self.parent / "ordinary").mkdir()
        (self.parent / "ordinary/file.txt").write_text("ordinary file\n")
        self.git(self.parent, "add", "ordinary")
        result = self.update("--path", "ordinary")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not a registered submodule", result.stderr)
        self.assertEqual(self.head(), self.before)


if __name__ == "__main__":
    unittest.main()
