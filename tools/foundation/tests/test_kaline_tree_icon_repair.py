import unittest
from pathlib import Path

SCENE = Path("client/Assets/Scenes/KalineTree.unity")
OLD = "objectReference: {fileID: 1912824793, guid: a304a4d492f1e9b4cae12eeddfa6dad8, type: 3}"
NEW = "objectReference: {fileID: 21300000, guid: b2802606b917448eb9e7c9bba03804f2, type: 3}"
META = Path("client/Assets/Nexus/ReconstructedUI/KalineTree.png.meta")


class KalineTreeIconRepairTests(unittest.TestCase):
    def test_afk_rewards_location_icon_uses_nexus_kaline_tree_sprite(self):
        text = SCENE.read_text()
        self.assertNotIn(OLD, text)
        self.assertIn(NEW, text)
        meta = META.read_text()
        self.assertIn("guid: b2802606b917448eb9e7c9bba03804f2", meta)
        self.assertIn("userData: nexus-clean-room-ui", meta)


if __name__ == "__main__":
    unittest.main()
