from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DependencyFinding:
    name: str
    status: str
    source: str
    expected_path: str | None
    license_state: str


def _needs_review(license_state: str) -> bool:
    state = license_state.strip().upper()
    return state == "UNKNOWN" or state.endswith("_REVIEW") or state == "NEEDS_REVIEW"


def scan_dependencies(repo_root: Path, manifest_path: Path) -> list[DependencyFinding]:
    data = json.loads(manifest_path.read_text())
    entries = data.get("dependencies")
    if not isinstance(entries, list):
        raise ValueError("dependency manifest must contain a dependencies list")
    unity_manifest_path = repo_root / "client/Packages/manifest.json"
    unity_packages = json.loads(unity_manifest_path.read_text()).get("dependencies", {})
    findings: list[DependencyFinding] = []
    for entry in entries:
        name = entry["name"]
        kind = entry["kind"]
        required = entry["required"]
        license_state = entry["license_state"]
        expected_path = entry.get("expected_path")
        if kind == "upm":
            if name not in unity_packages:
                status = "BLOCKED_DEP" if required else "MISSING"
                source = "client/Packages/manifest.json:missing"
            else:
                version = unity_packages[name]
                source = f"client/Packages/manifest.json:{version}"
                status = "NEEDS_REVIEW" if _needs_review(license_state) else "PRESENT"
        elif kind == "asset":
            if not expected_path:
                raise ValueError(f"asset dependency {name} requires expected_path")
            present = (repo_root / expected_path).exists()
            if not present and required:
                status = "BLOCKED_DEP"
            elif _needs_review(license_state):
                status = "NEEDS_REVIEW"
            elif not present:
                status = "MISSING"
            else:
                status = "PRESENT"
            source = expected_path
        else:
            raise ValueError(f"unsupported dependency kind: {kind}")
        findings.append(DependencyFinding(name, status, source, expected_path, license_state))
    return findings


def render_inventory(findings: list[DependencyFinding]) -> str:
    lines = [
        "# Unity Third-Party Dependency Inventory",
        "",
        "Generated from the pinned Nexus Idle foundation. File presence never proves redistribution rights.",
        "",
        "| Dependency | Status | Source / expected path | License state |",
        "| --- | --- | --- | --- |",
    ]
    for item in findings:
        lines.append(f"| {item.name} | {item.status} | `{item.source}` | {item.license_state} |")
    lines += [
        "",
        "Status meanings: PRESENT means detected with an explicit non-review license classification. MISSING means an optional item is absent. BLOCKED_DEP means a required item is absent. NEEDS_REVIEW means content exists but its license/redistribution terms still require review.",
        "",
    ]
    return "\n".join(lines)


def _manifest_is_explicit(manifest_path: Path) -> bool:
    entries = json.loads(manifest_path.read_text()).get("dependencies", [])
    return bool(entries) and all(
        isinstance(e, dict)
        and e.get("kind") in {"asset", "upm"}
        and isinstance(e.get("required"), bool)
        and isinstance(e.get("license_state"), str)
        and bool(e["license_state"].strip())
        for e in entries
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory Unity third-party dependencies")
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--mode", choices=["inventory"], default="inventory")
    args = parser.parse_args()
    if not _manifest_is_explicit(args.manifest):
        print("FAIL: dependency manifest contains unclassified entries")
        return 2
    findings = scan_dependencies(args.repo, args.manifest)
    output = args.repo / "docs/dependencies/unity-third-party.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_inventory(findings))
    counts: dict[str, int] = {}
    for item in findings:
        counts[item.status] = counts.get(item.status, 0) + 1
        print(f"{item.status}: {item.name} [{item.license_state}]")
    print("SUMMARY " + " ".join(f"{k}={counts[k]}" for k in sorted(counts)))
    print(f"WROTE: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
