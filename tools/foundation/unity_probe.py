from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path

from tools.foundation.dependencies import scan_dependencies
from tools.foundation.probe_result import ProbeResult

EXPECTED_VERSION = "2021.3.26f1"
REQUIRED_SCENES = ("Overworld", "Battle", "Summon", "Ascension", "KalineTree", "UnitDetail")
COMPILER_ERROR = re.compile(r"\berror\s+CS\d+\b|scripts? have compiler errors|compilation failed", re.IGNORECASE)


def _project_version(project: Path) -> str | None:
    path = project / "ProjectSettings/ProjectVersion.txt"
    if not path.exists():
        return None
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith("m_EditorVersion:"):
            return line.split(":", 1)[1].strip()
    return None


def _unity_version(executable: Path) -> tuple[str | None, str]:
    proc = subprocess.run(
        [str(executable), "-version"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    text = proc.stdout.strip()
    match = re.search(r"\b\d+\.\d+\.\d+[fp]\d+\b", text)
    return (match.group(0) if match else None, text)


def _scene_results(project: Path) -> list[ProbeResult]:
    results: list[ProbeResult] = []
    for name in REQUIRED_SCENES:
        path = project / f"Assets/Scenes/{name}.unity"
        status = "PASS" if path.exists() else "FAIL"
        label = "PRESENT" if path.exists() else "MISSING"
        results.append(ProbeResult(status, ["scene", name], f"{name}: {label}", str(path)))
    return results


def _dependency_results(project: Path) -> list[ProbeResult]:
    repo_root = project.parent
    manifest = repo_root / "config/dependencies/unity-third-party.json"
    if not manifest.exists():
        return [ProbeResult("FAIL", ["dependency-inventory"], f"dependency manifest missing: {manifest}")]
    findings = scan_dependencies(repo_root, manifest)
    results: list[ProbeResult] = []
    for finding in findings:
        if finding.status == "BLOCKED_DEP":
            results.append(ProbeResult(
                "BLOCKED_DEP",
                ["dependency", finding.name],
                f"{finding.name}: required dependency missing at {finding.expected_path or finding.source}",
            ))
        elif finding.status == "NEEDS_REVIEW":
            results.append(ProbeResult(
                "BLOCKED_DEP",
                ["dependency", finding.name],
                f"{finding.name}: license/redistribution review unresolved ({finding.license_state})",
            ))
    return results


def _resolve_unity(unity_executable: Path | None) -> Path | None:
    if unity_executable is not None:
        return unity_executable if unity_executable.is_file() and os.access(unity_executable, os.X_OK) else None
    env = os.environ.get("UNITY_EDITOR")
    if env:
        candidate = Path(env)
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate
    found = shutil.which("Unity") or shutil.which("unity-editor")
    return Path(found) if found else None


def probe_unity(project: Path, output: Path, unity_executable: Path | None = None) -> list[ProbeResult]:
    executable = _resolve_unity(unity_executable)
    if executable is None:
        return [ProbeResult("BLOCKED_DEP", ["Unity"], "Unity editor executable is absent")]

    editor_version, raw_version = _unity_version(executable)
    if editor_version != EXPECTED_VERSION:
        return [ProbeResult(
            "FAIL",
            [str(executable), "-version"],
            f"Unity version mismatch: expected {EXPECTED_VERSION}, got {editor_version or raw_version or 'unrecognized'}",
        )]

    project_version = _project_version(project)
    if project_version != EXPECTED_VERSION:
        return [ProbeResult(
            "FAIL",
            ["project-version"],
            f"project Unity version mismatch: expected {EXPECTED_VERSION}, got {project_version or 'missing'}",
        )]

    results: list[ProbeResult] = [
        ProbeResult("PASS", [str(executable), "-version"], f"Unity editor version {editor_version}"),
        ProbeResult("PASS", ["project-version"], f"project Unity version {project_version}"),
    ]
    scene_results = _scene_results(project)
    results.extend(scene_results)
    dependency_results = _dependency_results(project)
    results.extend(dependency_results)
    if any(result.status != "PASS" for result in scene_results) or dependency_results:
        return results

    output.mkdir(parents=True, exist_ok=True)
    log_path = output / "unity-import.log"
    command = [
        str(executable),
        "-batchmode",
        "-nographics",
        "-quit",
        "-projectPath",
        str(project.resolve()),
        "-logFile",
        str(log_path.resolve()),
    ]
    proc = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if proc.stdout:
        (output / "unity-stdout.log").write_text(proc.stdout)
    if proc.returncode != 0:
        results.append(ProbeResult("FAIL", command, f"Unity import exit {proc.returncode}", str(log_path)))
        return results

    log_text = log_path.read_text(errors="replace") if log_path.exists() else proc.stdout
    if COMPILER_ERROR.search(log_text or ""):
        results.append(ProbeResult("FAIL", command, "Unity import log contains compiler error signature", str(log_path)))
        return results

    results.append(ProbeResult("PASS", command, "Unity batch import/compile exit 0 with no compiler error signature", str(log_path)))
    return results


def render_summary(results: list[ProbeResult]) -> str:
    overall = "FAIL" if any(r.status == "FAIL" for r in results) else ("BLOCKED_DEP" if any(r.status == "BLOCKED_DEP" for r in results) else "PASS")
    runtime = [r for r in results if "-batchmode" in r.command]
    static = [r for r in results if r not in runtime]
    lines = [
        "# Unity Runtime Baseline",
        "",
        f"Required editor: `{EXPECTED_VERSION}`",
        f"Overall: `{overall}`",
        "",
        "## STATIC_ONLY",
        "",
    ]
    for result in static:
        lines.append(f"- {result.status}: {' '.join(result.command)}: {result.reason}")
    lines += ["", "## OBSERVED_RUNTIME", ""]
    if runtime:
        for result in runtime:
            lines.append(f"- {result.status}: {' '.join(result.command)}: {result.reason} artifact={result.artifact or '-'}")
    else:
        lines.append("- No Unity runtime/import command executed because a preflight blocker or failure stopped the probe.")
    lines += ["", "The probe never downloads proprietary or Asset Store dependencies automatically.", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe the pinned Unity client baseline")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--unity", type=Path)
    args = parser.parse_args()
    results = probe_unity(args.project, args.output, args.unity)
    summary_path = Path("docs/baseline/unity-runtime.md")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(render_summary(results))
    for result in results:
        print(f"{result.status}: {' '.join(result.command)}: {result.reason}")
    return 1 if any(r.status == "FAIL" for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
