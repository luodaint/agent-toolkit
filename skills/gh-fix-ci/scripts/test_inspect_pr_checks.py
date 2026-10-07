# Local regression tests for OpenAI's adapted CI inspector. Apache-2.0.
import argparse
import contextlib
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import inspect_pr_checks as inspector


REPO = Path("/fixture/repo")
REPO_URL = "https://github.com/example/project"
RUN_URL = REPO_URL + "/actions/runs/42/job/7"


class InspectorTests(unittest.TestCase):
    def run_main(self, checks, check_status=0):
        """Exercise the full inspector with only the gh/process boundary replaced."""
        def gh(args, cwd):
            self.assertEqual(cwd, REPO)
            if args[:2] == ["pr", "checks"]:
                return inspector.GhResult(check_status, json.dumps(checks), "")
            if args == ["repo", "view", "--json", "url"]:
                return inspector.GhResult(0, json.dumps({"url": REPO_URL}), "")
            if args[:3] == ["run", "view", "42"]:
                if args[-1] == "--log":
                    return inspector.GhResult(0, "setup ready\nerror: test assertion failed\n", "")
                return inspector.GhResult(0, json.dumps({
                    "headSha": "fixture-revision", "conclusion": "failure", "url": RUN_URL,
                }), "")
            self.fail("Unexpected gh command: " + repr(args))

        args = argparse.Namespace(repo=str(REPO), pr="12", max_lines=160, context=30, json=True)
        stdout = io.StringIO()
        with patch.object(inspector, "parse_args", return_value=args), \
             patch.object(inspector, "find_git_root", return_value=REPO), \
             patch.object(inspector, "ensure_gh_available", return_value=True), \
             patch.object(inspector, "run_gh_command", side_effect=gh), \
             contextlib.redirect_stdout(stdout):
            exit_code = inspector.main()
        return exit_code, json.loads(stdout.getvalue())

    def test_failed_status_json_still_produces_diagnosis(self):
        checks = [{"name": "tests", "state": "FAILURE", "link": RUN_URL, "bucket": "fail"}]
        status, output = self.run_main(checks, check_status=1)
        self.assertEqual(status, 1)
        self.assertEqual(output["checks"], checks)
        result = output["results"][0]
        self.assertEqual(result["run"]["headSha"], "fixture-revision")
        self.assertEqual(result["status"], "ok")
        self.assertIn("test assertion failed", result["logSnippet"])

    def test_pending_checks_do_not_report_success(self):
        for check in ({"bucket": "pending"}, {"state": "IN_PROGRESS"}):
            with self.subTest(check=check):
                status, output = self.run_main([check], check_status=8)
                self.assertEqual(status, 8)
                self.assertEqual(output["results"], [])
                self.assertEqual(output["checks"], [check])

    def test_json_without_failures_preserves_check_evidence(self):
        for checks in ([], [{"state": "SUCCESS", "bucket": "pass"}], [{"bucket": "skipping"}]):
            with self.subTest(checks=checks):
                status, output = self.run_main(checks)
                self.assertEqual(status, 0)
                self.assertEqual(output["checks"], checks)
                self.assertEqual(output["results"], [])

    def test_cancelled_bucket_is_unresolved(self):
        status, output = self.run_main([{"name": "cancelled", "bucket": "cancel"}], 1)
        self.assertEqual(status, 1)
        self.assertEqual(len(output["results"]), 1)

    def test_field_fallback_accepts_failing_and_pending_json(self):
        fields_error = inspector.GhResult(1, "", "Unknown JSON field: conclusion\nAvailable fields:\nname\nstate\nbucket\nlink\n")
        for status, check in ((1, {"bucket": "fail"}), (8, {"bucket": "pending"})):
            with self.subTest(status=status), patch.object(inspector, "run_gh_command", side_effect=[
                fields_error, inspector.GhResult(status, json.dumps([check]), ""),
            ]) as command:
                self.assertEqual(inspector.fetch_checks("12", REPO), [check])
                self.assertEqual(command.call_args.args[0][-1], "name,state,bucket,link")

    def test_api_and_malformed_payload_errors_are_not_empty_success(self):
        failures = (
            inspector.GhResult(1, "", "authentication failed"),
            inspector.GhResult(1, "not JSON", "network failed"),
            inspector.GhResult(2, "[]", "invalid command"),
            inspector.GhResult(0, '{"unexpected": true}', ""),
            inspector.GhResult(0, '["not a check"]', ""),
            inspector.GhResult(0, "", ""),
        )
        for response in failures:
            with self.subTest(response=response.stdout), \
                 patch.object(inspector, "run_gh_command", return_value=response), \
                 contextlib.redirect_stderr(io.StringIO()):
                self.assertIsNone(inspector.fetch_checks("12", REPO))

    def test_external_or_mismatched_urls_never_fetch_logs(self):
        urls = (
            "https://buildkite.com/example/actions/runs/42/job/7",
            "https://github.com/another/project/actions/runs/42/job/7",
            "https://github.com/example/project/runs/42",
            "https://github.com.evil.example/example/project/actions/runs/42",
            "https://user@github.com/example/project/actions/runs/42",
            "http://github.com/example/project/actions/runs/42",
        )
        for url in urls:
            with self.subTest(url=url), patch.object(inspector, "run_gh_command") as command:
                result = inspector.analyze_check({"link": url}, REPO, REPO_URL, 160, 30)
                self.assertEqual(result["status"], "external")
                self.assertEqual(result["detailsUrl"], url)
                command.assert_not_called()

    def test_unknown_repository_scope_never_fetches_logs(self):
        with patch.object(inspector, "run_gh_command") as command:
            result = inspector.analyze_check({"link": RUN_URL}, REPO, None, 160, 30)
        self.assertEqual(result["status"], "external")
        command.assert_not_called()

    def test_enterprise_host_is_scoped_to_selected_repository(self):
        repo_url = "https://git.company.example/team/service"
        self.assertEqual(inspector.extract_run_id(repo_url + "/actions/runs/123", repo_url), "123")
        self.assertIsNone(inspector.extract_run_id(
            "https://github.com/team/service/actions/runs/123", repo_url,
        ))

    def test_pending_run_uses_job_log_fallback(self):
        with patch.object(inspector, "run_gh_command", side_effect=[
            inspector.GhResult(1, "", "run is still in progress"),
            inspector.GhResult(0, '{"nameWithOwner": "example/project"}', ""),
        ]), patch.object(inspector, "run_gh_command_raw", return_value=(0, b"error: job failed\n", "")) as raw:
            log, error, status = inspector.fetch_check_log("42", "7", REPO)
        self.assertEqual((log, error, status), ("error: job failed\n", "", "ok"))
        self.assertEqual(raw.call_args.args[0], ["api", "/repos/example/project/actions/jobs/7/logs"])

    def test_unavailable_logs_preserve_failure_revision(self):
        with patch.object(inspector, "run_gh_command", side_effect=[
            inspector.GhResult(0, '{"headSha": "failed-revision"}', ""),
            inspector.GhResult(1, "", "log expired"),
        ]):
            result = inspector.analyze_check({"link": RUN_URL}, REPO, REPO_URL, 160, 30)
        self.assertEqual(result["status"], "log_unavailable")
        self.assertEqual(result["run"]["headSha"], "failed-revision")
        self.assertEqual(result["error"], "log expired")

    def test_zip_job_log_is_reported_unavailable(self):
        with patch.object(inspector, "fetch_repo_slug", return_value="example/project"), \
             patch.object(inspector, "run_gh_command_raw", return_value=(0, b"PK\x03\x04fixture", "")):
            log, error = inspector.fetch_job_log("7", REPO)
        self.assertEqual(log, "")
        self.assertIn("zip archive", error)


if __name__ == "__main__":
    unittest.main()
