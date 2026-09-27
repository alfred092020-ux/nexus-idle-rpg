from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class UpstreamPin:
    repo_url: str
    branch: str
    commit: str
    code_license: str


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(repo_root), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def load_pin(path: Path) -> UpstreamPin:
    data = json.loads(path.read_text())
    return UpstreamPin(data["repo_url"], data["branch"], data["commit"], data["code_license"])


def ensure_remote(repo_root: Path, name: str, url: str) -> None:
    current = _git(repo_root, "remote", "get-url", name)
    if current.returncode != 0:
        result = _git(repo_root, "remote", "add", name, url)
    elif current.stdout.strip() != url:
        result = _git(repo_root, "remote", "set-url", name, url)
    else:
        return
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())


def verify_pin(repo_root: Path, pin_path: Path, ref: str = "HEAD") -> list[str]:
    pin = load_pin(pin_path); errors: list[str] = []
    remote = _git(repo_root, "remote", "get-url", "upstream")
    if remote.returncode != 0:
        errors.append("upstream remote is missing")
    elif remote.stdout.strip() != pin.repo_url:
        errors.append(f"upstream URL mismatch: expected {pin.repo_url}, got {remote.stdout.strip()}")
    commit = _git(repo_root, "cat-file", "-e", f"{pin.commit}^{{commit}}")
    if commit.returncode != 0:
        errors.append(f"pinned commit is missing or unreachable: {pin.commit}")
        return errors
    if _git(repo_root, "merge-base", "--is-ancestor", pin.commit, ref).returncode != 0:
        errors.append(f"pinned commit {pin.commit} is not an ancestor of {ref}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify pinned Lambda client provenance")
    parser.add_argument("--repo", type=Path, required=True); parser.add_argument("--pin", type=Path, required=True); parser.add_argument("--ref", default="HEAD")
    args = parser.parse_args(); errors = verify_pin(args.repo, args.pin, args.ref)
    if errors:
        for error in errors: print(f"FAIL: {error}")
        return 1
    pin = load_pin(args.pin); print(f"PASS: {pin.repo_url} {pin.commit} is an ancestor of {args.ref}"); return 0

if __name__ == "__main__":
    raise SystemExit(main())
