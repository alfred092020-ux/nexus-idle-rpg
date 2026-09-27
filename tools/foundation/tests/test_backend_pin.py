import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.foundation.backend_pin import BackendPin, checkout_backend, verify_checkout


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, stderr=subprocess.DEVNULL
    ).strip()


class BackendPinTests(unittest.TestCase):
    def make_remote(self, root: Path):
        source = root / "source"
        source.mkdir()
        git(source, "init", "-b", "main")
        git(source, "config", "user.email", "test@example.com")
        git(source, "config", "user.name", "Test")
        (source / "README.md").write_text("one\n")
        git(source, "add", "README.md")
        git(source, "commit", "-m", "one")
        commit = git(source, "rev-parse", "HEAD")
        remote = root / "remote.git"
        subprocess.check_call(
            ["git", "clone", "--bare", str(source), str(remote)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return source, remote, commit

    def test_checkout_backend_creates_detached_exact_checkout(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, remote, commit = self.make_remote(root)
            dest = root / "checkout"
            pin = BackendPin(str(remote), "main", commit)
            checkout_backend(pin, dest)
            self.assertEqual(git(dest, "rev-parse", "HEAD"), commit)
            self.assertEqual(git(dest, "rev-parse", "--abbrev-ref", "HEAD"), "HEAD")
            self.assertEqual(verify_checkout(pin, dest), [])

    def test_checkout_backend_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, remote, commit = self.make_remote(root)
            dest = root / "checkout"
            pin = BackendPin(str(remote), "main", commit)
            checkout_backend(pin, dest)
            checkout_backend(pin, dest)
            self.assertEqual(git(dest, "rev-parse", "HEAD"), commit)
            self.assertEqual(verify_checkout(pin, dest), [])

    def test_verify_checkout_rejects_wrong_head(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source, remote, commit = self.make_remote(root)
            dest = root / "checkout"
            pin = BackendPin(str(remote), "main", commit)
            checkout_backend(pin, dest)
            (source / "README.md").write_text("two\n")
            git(source, "add", "README.md")
            git(source, "commit", "-m", "two")
            wrong = git(source, "rev-parse", "HEAD")
            git(source, "push", str(remote), "main")
            git(dest, "fetch", "origin", "main")
            git(dest, "checkout", "--detach", wrong)
            errors = verify_checkout(pin, dest)
            self.assertTrue(any("HEAD" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
