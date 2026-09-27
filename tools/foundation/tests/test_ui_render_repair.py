import re
import unittest
from pathlib import Path

ASSET_DIR = Path("client/Assets/Nexus/ReconstructedUI")
EXPECTED = {
    "12dedf54d1cf944e2abfc37f922124d6": "LocationCardBackground.png",
    "7848a178536e4451892d1e82417e65a6": "Barracks.png",
    "b2802606b917448eb9e7c9bba03804f2": "KalineTree.png",
    "fac7bf792e0a74af785a83e345040a84": "Summon.png",
    "93d5491347c3d4e76be9d0358a7e7f0f": "Ascension.png",
    "9683a896ff8204005bb85f575bf25309": "Dungeon.png",
    "8cc285b97c8f14593b8c7f9a5cd5ff5b": "Shop.png",
    "9a63522f968e04ba2b391b224cc0dabb": "Campaign.png",
    "fe025e83f69d0b54f8a4fe3c7c128fd7": "InventoryIcon.png",
    "6013f43a04c8e7848ac69a4e1154b3f5": "Separator.png",
    "6aa9505d7687e57409e2eed29c6ce521": "InventoryBackground.png",
}

class UiRenderRepairTests(unittest.TestCase):
    def test_overworld_missing_sprite_guids_resolve_to_nexus_assets(self):
        for guid, name in EXPECTED.items():
            image = ASSET_DIR / name
            meta = Path(str(image) + ".meta")
            self.assertTrue(image.exists(), f"missing replacement image for {guid}: {name}")
            self.assertTrue(meta.exists(), f"missing meta for {guid}: {name}")
            text = meta.read_text()
            self.assertRegex(text, rf"(?m)^guid: {guid}$")
            self.assertIn("nexus-clean-room-ui", text)

if __name__ == "__main__":
    unittest.main()
