import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import patch_gui


class WizardTests(unittest.TestCase):
    def run_wizard(self, accepted=True, source="original.exe", destination="output", failure=None):
        root = MagicMock()
        with patch.object(patch_gui.tk, "Tk", return_value=root), \
             patch.object(patch_gui.messagebox, "askokcancel", return_value=accepted), \
             patch.object(patch_gui.filedialog, "askopenfilename", return_value=source), \
             patch.object(patch_gui.filedialog, "askdirectory", return_value=destination), \
             patch.object(patch_gui, "create_copy", side_effect=failure, return_value=Path("output/DayZServer_x64.exe")) as create, \
             patch.object(patch_gui.messagebox, "showerror") as error, \
             patch.object(patch_gui.messagebox, "showinfo") as success:
            patch_gui.main("pt")
            root.destroy.assert_called_once()
            return create.call_count, error.call_count, success.call_count

    def test_cancel_never_creates_copy(self):
        for args in ({"accepted": False}, {"source": ""}, {"destination": ""}):
            with self.subTest(args=args):
                self.assertEqual(self.run_wizard(**args), (0, 0, 0))

    def test_failed_patch_never_shows_success(self):
        self.assertEqual(self.run_wizard(failure=ValueError("Unsupported executable")), (1, 1, 0))

    def test_success_is_presented(self):
        self.assertEqual(self.run_wizard(), (1, 0, 1))

    def test_invalid_input_preserves_original_and_existing_executable(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "DayZServer_x64.exe"
            source.write_bytes(b"unsupported original")
            with self.assertRaises(ValueError):
                patch_gui.create_copy(source, folder)
            self.assertEqual(source.read_bytes(), b"unsupported original")
            self.assertEqual(list(Path(folder).rglob("*.exe")), [source])


if __name__ == "__main__":
    unittest.main()
