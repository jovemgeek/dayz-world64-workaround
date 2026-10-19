import tempfile
import unittest
from pathlib import Path
import patch_world64 as patcher


class RefusalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "original.exe"
        self.source.write_bytes(b"unsupported input")

    def test_unknown_build_leaves_no_output(self):
        output = self.root / "new.exe"
        with self.assertRaises(ValueError):
            patcher.patch(self.source, output)
        self.assertFalse(output.exists())
        self.assertFalse(output.with_suffix(".manifest.json").exists())
        self.assertEqual(self.source.read_bytes(), b"unsupported input")

    def test_source_collision(self):
        with self.assertRaises(ValueError):
            patcher.patch(self.source, self.source)
        self.assertEqual(self.source.read_bytes(), b"unsupported input")

    def test_existing_output_preserved(self):
        output = self.root / "new.exe"
        output.write_bytes(b"existing")
        with self.assertRaises(ValueError):
            patcher.patch(self.source, output)
        self.assertEqual(output.read_bytes(), b"existing")

    def test_existing_manifest_preserved(self):
        output = self.root / "new.exe"
        manifest = output.with_suffix(".manifest.json")
        manifest.write_text("existing")
        with self.assertRaises(ValueError):
            patcher.patch(self.source, output)
        self.assertEqual(manifest.read_text(), "existing")
        self.assertFalse(output.exists())

    def test_manifest_source_collision(self):
        source = self.root / "new.manifest.json"
        source.write_bytes(b"source")
        with self.assertRaises(ValueError):
            patcher.patch(source, self.root / "new.exe")
        self.assertEqual(source.read_bytes(), b"source")

    def test_manifest_output_collision(self):
        with self.assertRaises(ValueError):
            patcher.patch(self.source, self.root / "new.manifest.json")


if __name__ == "__main__":
    unittest.main()
