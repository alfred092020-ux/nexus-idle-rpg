import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.foundation.provenance import UpstreamPin, ensure_remote, load_pin, verify_pin


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.DEVNULL).strip()


class ProvenanceTests(unittest.TestCase):
    def make_repo(self, root: Path):
        repo = root / "repo"
        repo.mkdir()
        git(repo, "init", "-b", "main")
        git(repo, "config", "user.email", "test@example.com")
        git(repo, "config", "user.name", "Test")
        (repo / "file.txt").write_text("one\n")
        git(repo, "add", "file.txt")
        git(repo, "commit", "-m", "one")
        return repo, git(repo, "rev-parse", "HEAD")

    def write_pin(self, path: Path, repo_url: str, commit: str):
        path.write_text(json.dumps({
            "repo_url": repo_url, "branch": "main", "commit": commit,
            "code_license": "Apache-2.0", "unity_version": "2021.3.26f1",
            "imported_at": "2026-09-27", "upstream_merges": []
        }))

    def test_load_pin_parses_exact_values(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "pin.json"
            self.write_pin(path, "https://example.invalid/repo.git", "a" * 40)
            self.assertEqual(load_pin(path), UpstreamPin("https://example.invalid/repo.git", "main", "a" * 40, "Apache-2.0"))

    def test_load_pin_requires_import_and_merge_traceability_metadata(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "pin.json"
            path.write_text(json.dumps({
                "repo_url": "https://example.invalid/repo.git",
                "branch": "main", "commit": "a" * 40,
                "code_license": "Apache-2.0", "unity_version": "2021.3.26f1"
            }))
            with self.assertRaises(ValueError):
                load_pin(path)

    def test_verify_pin_accepts_ancestor_and_expected_remote(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); repo, commit = self.make_repo(root)
            ensure_remote(repo, "upstream", "https://example.invalid/repo.git")
            pin = root / "pin.json"; self.write_pin(pin, "https://example.invalid/repo.git", commit)
            self.assertEqual(verify_pin(repo, pin), [])

    def test_verify_pin_reports_missing_commit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); repo, _ = self.make_repo(root)
            ensure_remote(repo, "upstream", "https://example.invalid/repo.git")
            pin = root / "pin.json"; self.write_pin(pin, "https://example.invalid/repo.git", "f" * 40)
            errors = verify_pin(repo, pin)
            self.assertTrue(any("unreachable" in e.lower() or "missing" in e.lower() for e in errors), errors)

    def test_verify_pin_reports_wrong_upstream_url(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); repo, commit = self.make_repo(root)
            ensure_remote(repo, "upstream", "https://wrong.invalid/repo.git")
            pin = root / "pin.json"; self.write_pin(pin, "https://expected.invalid/repo.git", commit)
            errors = verify_pin(repo, pin)
            self.assertTrue(any("url" in e.lower() for e in errors), errors)

    def test_moved_remote_branch_does_not_mutate_reviewed_pin(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); repo, commit = self.make_repo(root)
            remote = root / "remote.git"
            subprocess.check_call(["git", "clone", "--bare", str(repo), str(remote)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            pin = root / "pin.json"; self.write_pin(pin, str(remote), commit)
            ensure_remote(repo, "upstream", str(remote)); before = pin.read_text()
            (repo / "file.txt").write_text("two\n"); git(repo, "add", "file.txt"); git(repo, "commit", "-m", "two")
            git(repo, "push", str(remote), "main"); git(repo, "fetch", "upstream", "main")
            self.assertEqual(verify_pin(repo, pin), [])
            self.assertEqual(pin.read_text(), before)

if __name__ == "__main__":
    unittest.main()
