import json
import tempfile
import unittest
from pathlib import Path

from tools.foundation.unity_probe import REQUIRED_SCENES, probe_unity


class UnityProbeTests(unittest.TestCase):
    def make_repo(self, root: Path, dependencies=None):
        project = root / "client"
        (project / "ProjectSettings").mkdir(parents=True)
        (project / "Packages").mkdir(parents=True)
        (project / "Assets/Scenes").mkdir(parents=True)
        (root / "config/dependencies").mkdir(parents=True)
        (project / "ProjectSettings/ProjectVersion.txt").write_text(
            "m_EditorVersion: 2021.3.26f1\n"
            "m_EditorVersionWithRevision: 2021.3.26f1 (a16dc32e0ff2)\n"
        )
        (project / "Packages/manifest.json").write_text(json.dumps({"dependencies": {}}))
        (root / "config/dependencies/unity-third-party.json").write_text(
            json.dumps({"dependencies": dependencies or []})
        )
        for scene in REQUIRED_SCENES:
            (project / f"Assets/Scenes/{scene}.unity").write_text("scene\n")
        return project

    def make_unity(self, root: Path, version="2021.3.26f1", body="exit 0"):
        exe = root / "Unity"
        exe.write_text(
            "#!/bin/sh\n"
            f"if [ \"$1\" = \"-version\" ]; then echo '{version}'; exit 0; fi\n"
            + body + "\n"
        )
        exe.chmod(0o755)
        return exe

    def test_absent_unity_executable_is_blocked_dep(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = self.make_repo(root)
            results = probe_unity(project, root / "out", unity_executable=root / "missing")
            self.assertEqual(results[0].status, "BLOCKED_DEP")

    def test_wrong_unity_version_is_fail(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = self.make_repo(root)
            exe = self.make_unity(root, "2022.3.0f1")
            results = probe_unity(project, root / "out", unity_executable=exe)
            self.assertTrue(any(r.status == "FAIL" and "version" in r.reason.lower() for r in results), results)

    def test_missing_required_licensed_asset_is_blocked_dep(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            deps = [{
                "name": "Licensed Asset",
                "kind": "asset",
                "required": True,
                "license_state": "ASSET_STORE_LICENSE_REVIEW",
                "expected_path": "client/Assets/ThirdParty/Licensed",
            }]
            project = self.make_repo(root, deps)
            exe = self.make_unity(root)
            results = probe_unity(project, root / "out", unity_executable=exe)
            self.assertTrue(any(r.status == "BLOCKED_DEP" and "Licensed Asset" in r.reason for r in results), results)

    def test_nonzero_unity_exit_is_fail(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = self.make_repo(root)
            exe = self.make_unity(root, body="exit 7")
            results = probe_unity(project, root / "out", unity_executable=exe)
            self.assertTrue(any(r.status == "FAIL" and "exit 7" in r.reason for r in results), results)

    def test_compiler_error_signature_fails_even_with_exit_zero(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = self.make_repo(root)
            body = '''log=""
prev=""
for arg in "$@"; do
  if [ "$prev" = "-logFile" ]; then log="$arg"; fi
  prev="$arg"
done
printf 'Assets/Test.cs(1,1): error CS1002: ; expected\\n' > "$log"
exit 0'''
            exe = self.make_unity(root, body=body)
            results = probe_unity(project, root / "out", unity_executable=exe)
            self.assertTrue(any(r.status == "FAIL" and "compiler" in r.reason.lower() for r in results), results)

    def test_required_scenes_are_reported_individually(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = self.make_repo(root)
            exe = self.make_unity(root)
            (project / "Assets/Scenes/Battle.unity").unlink()
            results = probe_unity(project, root / "out", unity_executable=exe)
            scene_results = [r for r in results if r.command and r.command[0] == "scene"]
            for name in REQUIRED_SCENES:
                self.assertTrue(any(name in r.reason for r in scene_results), (name, scene_results))
            self.assertTrue(any("Battle" in r.reason and r.status == "FAIL" for r in scene_results), scene_results)


if __name__ == "__main__":
    unittest.main()
