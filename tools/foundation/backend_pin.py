from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BackendPin:
    repo_url: str
    branch: str
    commit: str


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _run(*args: str) -> None:
    result = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())


def load_pin(path: Path) -> BackendPin:
    data = json.loads(path.read_text())
    return BackendPin(data["repo_url"], data["branch"], data["commit"])


def checkout_backend(pin: BackendPin, dest: Path) -> None:
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        _run("git", "clone", "--no-checkout", pin.repo_url, str(dest))
    elif not (dest / ".git").exists():
        raise RuntimeError(f"backend destination exists but is not a Git checkout: {dest}")

    remote = _git(dest, "remote", "get-url", "origin")
    if remote.returncode != 0:
        raise RuntimeError("backend checkout has no origin remote")
    if remote.stdout.strip() != pin.repo_url:
        raise RuntimeError(
            f"backend origin mismatch: expected {pin.repo_url}, got {remote.stdout.strip()}"
        )

    fetch = _git(dest, "fetch", "origin", pin.branch)
    if fetch.returncode != 0:
        raise RuntimeError(fetch.stderr.strip())
    commit = _git(dest, "cat-file", "-e", f"{pin.commit}^{{commit}}")
    if commit.returncode != 0:
        raise RuntimeError(f"pinned backend commit is missing: {pin.commit}")
    checkout = _git(dest, "checkout", "--detach", pin.commit)
    if checkout.returncode != 0:
        raise RuntimeError(checkout.stderr.strip())


def verify_checkout(pin: BackendPin, dest: Path) -> list[str]:
    errors: list[str] = []
    if not (dest / ".git").exists():
        return [f"backend checkout is missing: {dest}"]

    remote = _git(dest, "remote", "get-url", "origin")
    if remote.returncode != 0:
        errors.append("backend origin remote is missing")
    elif remote.stdout.strip() != pin.repo_url:
        errors.append(
            f"backend origin mismatch: expected {pin.repo_url}, got {remote.stdout.strip()}"
        )

    head = _git(dest, "rev-parse", "HEAD")
    if head.returncode != 0:
        errors.append("backend HEAD is unreadable")
    elif head.stdout.strip() != pin.commit:
        errors.append(f"backend HEAD mismatch: expected {pin.commit}, got {head.stdout.strip()}")

    branch = _git(dest, "symbolic-ref", "-q", "HEAD")
    if branch.returncode == 0:
        errors.append(f"backend HEAD must be detached, got {branch.stdout.strip()}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Checkout and verify pinned Mirra backend")
    parser.add_argument("--pin", type=Path, required=True)
    parser.add_argument("--dest", type=Path, required=True)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    pin = load_pin(args.pin)
    checkout_backend(pin, args.dest)
    errors = verify_checkout(pin, args.dest) if args.verify else []
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {pin.repo_url} checked out detached at {pin.commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
