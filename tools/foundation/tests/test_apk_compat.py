import unittest
from pathlib import Path


class ApkCompatibilityTests(unittest.TestCase):
    def test_clean_room_progress_bar_contract_exists(self):
        shim = Path("client/Assets/Scripts/Compat/UIProgressBar.cs")
        self.assertTrue(shim.exists(), "clean-room progress bar shim is missing")
        text = shim.read_text()
        self.assertIn("namespace DuloGames.UI", text)
        self.assertIn("class UIProgressBar", text)
        self.assertIn("public float fillAmount", text)
        self.assertNotIn("RPG & MMO UI 6", text)


if __name__ == "__main__":
    unittest.main()
