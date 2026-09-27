import json
import tempfile
import unittest
from pathlib import Path

from tools.foundation.dependencies import scan_dependencies


class DependencyTests(unittest.TestCase):
    def make_repo(self, root: Path, packages=None):
        repo=root / "repo"
        (repo / "client/Packages").mkdir(parents=True)
        (repo / "client/Assets").mkdir(parents=True)
        (repo / "client/Packages/manifest.json").write_text(json.dumps({"dependencies": packages or {}}))
        return repo

    def write_manifest(self, path: Path, entries):
        path.write_text(json.dumps({"dependencies": entries}))

    def test_unknown_license_is_needs_review(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); repo=self.make_repo(root); manifest=root / "deps.json"
            self.write_manifest(manifest, [{"name":"Unknown Asset","kind":"asset","required":False,"license_state":"UNKNOWN","expected_path":"client/Assets/Unknown"}])
            finding=scan_dependencies(repo, manifest)[0]
            self.assertEqual(finding.status, "NEEDS_REVIEW")

    def test_required_missing_asset_is_blocked_dep(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); repo=self.make_repo(root); manifest=root / "deps.json"
            self.write_manifest(manifest, [{"name":"Required Asset","kind":"asset","required":True,"license_state":"ASSET_STORE_REVIEW","expected_path":"client/Assets/ThirdParty/Required"}])
            finding=scan_dependencies(repo, manifest)[0]
            self.assertEqual(finding.status, "BLOCKED_DEP")

    def test_upm_dependency_is_detected_from_unity_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); repo=self.make_repo(root, {"com.example.pkg":"1.2.3"}); manifest=root / "deps.json"
            self.write_manifest(manifest, [{"name":"com.example.pkg","kind":"upm","required":True,"license_state":"UNITY_OR_UPSTREAM_TERMS","expected_path":None}])
            finding=scan_dependencies(repo, manifest)[0]
            self.assertEqual(finding.status, "PRESENT")
            self.assertEqual(finding.source, "client/Packages/manifest.json:1.2.3")

if __name__ == "__main__":
    unittest.main()
