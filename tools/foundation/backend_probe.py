from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path

from tools.foundation.probe_result import ProbeResult

PINNED_SHA = "03ce82842a5d2d36f3a58396e7f22e0a43dfcb86"
PREREQUISITES = ("nix", "devenv", "elixir", "mix", "protoc", "psql")


def probe_prerequisite(name: str, search_path: str | None = None) -> ProbeResult:
    found = shutil.which(name, path=search_path)
    if not found:
        return ProbeResult("BLOCKED_DEP", [name], f"required executable missing: {name}")
    return ProbeResult("PASS", [name], f"found {name} at {found}")


def run_probe_command(command: list[str], cwd: Path, artifact: Path | None = None) -> ProbeResult:
    proc = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    artifact_name = None
    if artifact is not None:
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(proc.stdout)
        artifact_name = str(artifact)
    status = "PASS" if proc.returncode == 0 else "FAIL"
    return ProbeResult(status, command, f"exit {proc.returncode}", artifact_name)


def _head(dest: Path) -> str | None:
    proc = subprocess.run(["git", "-C", str(dest), "rev-parse", "HEAD"], text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return proc.stdout.strip() if proc.returncode == 0 else None


def probe_backend(dest: Path, output: Path | None = None) -> list[ProbeResult]:
    head = _head(dest)
    if head != PINNED_SHA:
        return [ProbeResult("FAIL", ["git", "rev-parse", "HEAD"], f"backend SHA mismatch: expected {PINNED_SHA}, got {head or 'unavailable'}")]
    results = [ProbeResult("PASS", ["git", "rev-parse", "HEAD"], f"backend SHA matches {PINNED_SHA}")]
    prereqs = [probe_prerequisite(name) for name in PREREQUISITES]
    results.extend(prereqs)
    if any(item.status != "PASS" for item in prereqs):
        return results
    compile_artifact = output / "mix-compile.log" if output else None
    compile_result = run_probe_command(["devenv", "shell", "--", "mix", "compile"], dest, compile_artifact)
    results.append(compile_result)
    if compile_result.status != "PASS":
        return results
    test_artifact = output / "mix-test.log" if output else None
    results.append(run_probe_command(["devenv", "shell", "--", "mix", "test"], dest, test_artifact))
    return results


def render_summary(results: list[ProbeResult]) -> str:
    overall = "FAIL" if any(r.status == "FAIL" for r in results) else ("BLOCKED_DEP" if any(r.status == "BLOCKED_DEP" for r in results) else "PASS")
    lines = ["# Mirra Backend Runtime Baseline", "", f"Pinned SHA: `{PINNED_SHA}`", f"Overall: `{overall}`", "", "| Status | Check | Reason | Artifact |", "| --- | --- | --- | --- |"]
    for result in results:
        cmd = " ".join(result.command)
        lines.append(f"| {result.status} | `{cmd}` | {result.reason} | {result.artifact or '-'} |")
    lines += ["", "A missing host prerequisite is BLOCKED_DEP. A wrong checkout or a command/test failure is FAIL. No privileged dependency installation is performed by this probe.", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe the pinned Mirra backend baseline")
    parser.add_argument("--backend", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = probe_backend(args.backend, args.output)
    summary = render_summary(results)
    summary_path = Path("docs/baseline/backend-runtime.md")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(summary)
    for result in results:
        print(f"{result.status}: {' '.join(result.command)}: {result.reason}")
    if any(r.status == "FAIL" for r in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
