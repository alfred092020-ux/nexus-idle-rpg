import unittest
from pathlib import Path

ASSET_DIR = Path("client/Assets/Nexus/ReconstructedUI/RemainingScreens")
EXPECTED = {
    "0051cf6193c6749e7ab7cef8a48fcf3b": "Supplies.png",
    "026147ae76b744279ad293045c9b1a20": "DungeonBattle.png",
    "0f3d93488882ca641ba1c8ccffca752c": "NavigationHover.png",
    "1d3f324bdbea19b4f940775746d5bb48": "FooterCenter.png",
    "1d9c8fecc73a24c15921bb444d2c3385": "Gems.png",
    "22d0bb8fe978246d6bd8a56e1f452108": "DungeonSettlement.png",
    "30766d868a45a854da64cb40e5cfb75f": "StatPanelNeutral.png",
    "396f1792cb8b55e4dac2b9bb0b216d22": "BattleControlButton.png",
    "3d441f1e30774d348b7f93bd913e6365": "NavigationArrow.png",
    "4217838d18d06c04fbb38361be7b975f": "StatPanelTinted.png",
    "4a0e4b8c2ba8d3241998c7e3a07cdd99": "StatIcon.png",
    "5c5ea64d1e4ea5a45bba661ba57e612b": "VictoryArrow.png",
    "62f1bf233af089747861fe9a5d95d2d9": "UnitNavigationButton.png",
    "7d0db3a719d4ecb4d944bab596d811ab": "Blueprints.png",
    "7dfa9099956c6af418e6a580b9a21ec7": "CloseIcon.png",
}
EXPECTED.update({
    "84008151a12ef4cbfa61099a6c1f99a6": "EquipmentTypeIcon.png",
    "a978391ac066d1b4087e8ec89b4d45d2": "VictorySideBackground.png",
    "b63772f122bd04772981fedb32c6a719": "SettlementPanel.png",
    "b7b41808d78dd8343ae4ed4c5af9cd4d": "UnitNavigationOverlay.png",
    "d1048adea5c732c4b9939a6bb241537a": "VictoryBorder.png",
    "dec8e77f2a338824ea062aaec34570a9": "FooterSide.png",
    "e31106507429ccd4e8529f61a5a2e0e3": "CloseButton.png",
    "e320dde368499e146999c2c45dea728f": "VictoryArrowFill.png",
    "ec06232243b9f4042a06df462dde05e7": "SharedPanelBackground.png",
    "f220907786fd84af7a0a1292ce920468": "Coins.png",
})


class RemainingUiRenderRepairTests(unittest.TestCase):
    def test_remaining_enabled_scene_sprite_guids_resolve_to_nexus_assets(self):
        self.assertEqual(25, len(EXPECTED))
        for guid, name in EXPECTED.items():
            image = ASSET_DIR / name
            meta = Path(str(image) + ".meta")
            self.assertTrue(image.exists(), f"missing replacement image for {guid}: {name}")
            self.assertTrue(meta.exists(), f"missing meta for {guid}: {name}")
            text = meta.read_text()
            self.assertIn(f"guid: {guid}\n", text)
            self.assertIn("userData: nexus-clean-room-ui", text)


if __name__ == "__main__":
    unittest.main()
