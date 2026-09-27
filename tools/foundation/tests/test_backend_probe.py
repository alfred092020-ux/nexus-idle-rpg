import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.foundation.backend_probe import probe_backend, probe_prerequisite, run_probe_command


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.DEVNULL).strip()


class BackendProbeTests(unittest.TestCase):
    def test_missing_devenv_is_blocked_dep(self):
        with tempfile.TemporaryDirectory() as td:
            result = probe_prerequisite("devenv", search_path=td)
            self.assertEqual(result.status, "BLOCKED_DEP")
            self.assertIn("devenv", result.reason)

    def test_wrong_backend_sha_is_fail(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / "backend"
            repo.mkdir()
            git(repo, "init", "-b", "main")
            git(repo, "config", "user.email", "test@example.com")
            git(repo, "config", "user.name", "Test")
            (repo / "README.md").write_text("stub\n")
            git(repo, "add", "README.md")
            git(repo, "commit", "-m", "stub")
            results = probe_backend(repo)
            self.assertEqual(results[0].status, "FAIL")
            self.assertIn("SHA", results[0].reason)

    def test_successful_stub_command_is_pass(self):
        with tempfile.TemporaryDirectory() as td:
            result = run_probe_command(["/bin/sh", "-c", "printf ok"], Path(td))
            self.assertEqual(result.status, "PASS")
            self.assertIn("exit 0", result.reason)

if __name__ == "__main__":
    unittest.main()
