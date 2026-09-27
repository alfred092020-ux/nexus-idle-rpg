import unittest
from pathlib import Path

ASSET_DIR = Path("client/Assets/Nexus/ReconstructedUI/Destination")
EXPECTED = {
    "f1542cf5e4ce3424da87a5f60f7c4fca": "ItemDetailPanel.png",
    "fbb369977077e4f568586f50bc16c663": "ScreenBackdrop.png",
    "f59401c5c79564fd1ae3bfb0876455a7": "Blueprints.png",
    "db427fab3e94daf4caa704d9314a77a1": "SummonScrolls.png",
    "b80465d0ff1da6a4eb9bc0510b2cb00a": "DetailPanel.png",
    "1c74d1dcff866ee48a68842355840c90": "SummonBox01.png",
    "806c2f4e4121bd443a535f7551d4fa7c": "SummonBox02.png",
    "d43e220cda833794bb17b6a394b2cb77": "SummonBox03.png",
    "7d0f73aed89f4e146b939c2b5afbcb89": "SummonBox04.png",
    "8e37c55a9648d4442808e911dafdf8f0": "SummonBox05.png",
    "dadfe4db9fb8c594abf23febe42df5ef": "SummonBox06.png",
    "a9ba49af3ee3062498ed2c2881a8a381": "SummonBox07.png",
    "53831ffd2c1064d07b3fcc10982b1e0d": "LevelUpResource.png",
    "6592b916f86b19e428db6f6847c7b6dd": "Fertilizer.png",
    "ae496f5dad56ea645b72d374a0376368": "Experience.png",
    "e7d29a79bc7fae248887c8a08a160303": "ArcaneCrystals.png",
    "1618cb37bcd5144fd923b9697be57d63": "HeroSouls.png",
    "564069f7f2ac56548827d81882b9e469": "TreeLevelPanel.png",
}
EXPECTED.update({
    "0e123cfdc54a3ca4684816a34167a566": "Necklace.png",
    "172774604c1bee84185a69041576525b": "Axe.png",
    "266c6672eaea23248813e9fd4517aa5f": "PurpleGloves.png",
    "2f1eaeeaad36ee5469eff7ff158f37ba": "LeatherArmor.png",
    "31af4c11b0228d142b71af2d3940bbcb": "Invocation.png",
    "4a39cb4b272639541b7bd5ac0649acf7": "Ham.png",
    "4b5c3887b0bad8548a4414947f05a7ba": "EpicSword.png",
    "5fd50594014b70e48bd6993443d46b32": "Sword.png",
    "6fc27c9d7fc2d9448af6851bf935e6d2": "Cape.png",
    "707545fb132aed646bdaf12831b9aaf5": "RedFlower.png",
    "86d0020fc2f114f4ab9fa1d5a5a34c6a": "Boots.png",
    "970324311431c794ca338446ea889948": "Ring.png",
    "a20d322c5e65a6746808e67a31dfe555": "GreenPotion.png",
    "b2afa56667af6a249ba292fc371eb496": "Plant.png",
    "b817779f7fb33f94a85fd94a5df90287": "PurpleCape.png",
    "b97c91e8b348f3f4ebdc11f5c82182cd": "Shield.png",
    "c16d3e5511c9e1341b0bd70dcb31fb81": "Prayer.png",
    "e52ea25af699fd445b7046374f81a5b9": "RedPotion.png",
    "e89ca016d404a6a4687a5ee741e2d2b5": "PlateBoots.png",
})


class DestinationUiRenderRepairTests(unittest.TestCase):
    def test_missing_destination_sprite_guids_resolve_to_nexus_assets(self):
        self.assertGreaterEqual(len(EXPECTED), 30)
        for guid, name in EXPECTED.items():
            image = ASSET_DIR / name
            meta = Path(str(image) + ".meta")
            self.assertTrue(image.exists(), f"missing replacement image for {guid}: {name}")
            self.assertTrue(meta.exists(), f"missing meta for {guid}: {name}")
            text = meta.read_text()
            self.assertIn(f"guid: {guid}\n", text)
            self.assertIn("userData: nexus-clean-room-ui", text)

    def test_kaline_multi_sprite_reference_remains_explicitly_unresolved(self):
        # a304... is referenced with nonstandard internal fileID 1912824793.
        # A normal single-sprite PNG would not safely satisfy that serialized reference.
        self.assertNotIn("a304a4d492f1e9b4cae12eeddfa6dad8", EXPECTED)


if __name__ == "__main__":
    unittest.main()
