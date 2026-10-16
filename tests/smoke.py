#!/usr/bin/env python3
"""Exercise the installed snap as an ordinary user; no cloud credentials needed."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class SnapSmoke(unittest.TestCase):
    def run_cli(self, *args, data=None, ok=True):
        result = subprocess.run(
            ["snap", "run", "markitdown", *map(str, args)], input=data,
            text=True, capture_output=True, timeout=90,
        )
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def test_help_and_version(self):
        self.assertIn("--output", self.run_cli("--help").stdout)
        self.assertIn("markitdown", self.run_cli("--version").stdout.lower())

    def test_stdin(self):
        html = "<!DOCTYPE html><html><head><title>Test</title></head><body><h1>Snap smoke</h1><p>café <strong>works</strong></p></body></html>"
        for args in [(), ("-x", "html")]:
            with self.subTest(args=args):
                output = self.run_cli(*args, data=html).stdout
                for marker in ["# Snap smoke", "café", "**works**"]:
                    self.assertIn(marker, output)

    def test_home_files_and_output(self):
        with tempfile.TemporaryDirectory(prefix="markitdown-test-", dir=Path.home()) as directory:
            source = Path(directory) / "input with spaces.html"
            destination = Path(directory) / "output with spaces.md"
            source.write_text("<h1>Local document</h1>", encoding="utf-8")
            result = self.run_cli(source, "-o", destination)
            self.assertEqual(result.stdout, "")
            self.assertIn("# Local document", destination.read_text())
            missing = self.run_cli(Path(directory) / "missing.html", ok=False)
            self.assertIn("FileNotFoundError", missing.stderr)

    def test_document_formats(self):
        fixtures = Path(__file__).parent / "fixtures"
        markers = {
            "test.docx": "314b0a30-5b04-470b-b9f7-eed2c2bec74a",
            "test.xlsx": "6ff4173b-42a5-4784-9b19-f49caff4d93d",
            "test.xls": "6ff4173b-42a5-4784-9b19-f49caff4d93d",
            "test.pptx": "2cdda5c8-e50e-4db4-b5f0-9722a649f455",
            "test.pdf": "While there is contemporaneous exploration of multi-agent approaches",
            "test.jpg": "Author: AutoGen Authors",
        }
        with tempfile.TemporaryDirectory(prefix="markitdown-formats-", dir=Path.home()) as directory:
            for name, marker in markers.items():
                with self.subTest(format=name):
                    source = shutil.copy2(fixtures / name, directory)
                    self.assertIn(marker, self.run_cli(source).stdout)

    def test_offline_audio(self):
        with tempfile.TemporaryDirectory(prefix="markitdown-audio-", dir=Path.home()) as directory:
            source = shutil.copy2(Path(__file__).parent / "fixtures/test.mp3", directory)
            code = (
                "import sys; from pydub import AudioSegment; "
                "from speech_recognition import AudioData; "
                "a = AudioSegment.from_mp3(sys.argv[1]).set_channels(1).set_sample_width(2); "
                "assert len(a) > 0; "
                "f = AudioData(a.raw_data, a.frame_rate, a.sample_width).get_flac_data(); "
                "assert f.startswith(b'fLaC')"
            )
            result = subprocess.run(
                ["snap", "run", "--shell", "markitdown", "-c",
                 'exec "$SNAP/bin/python3" -c "$1" "$2"', "audio-test", code, source],
                capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_bundled_tools(self):
        script = '\n'.join([
            'set -eu',
            '"$SNAP/usr/bin/ffmpeg" -version >/dev/null',
            '"$SNAP/usr/bin/ffprobe" -version >/dev/null',
            '"$SNAP/bin/markitdown-exiftool" -ver',
        ])
        result = subprocess.run(
            ["snap", "run", "--shell", "markitdown", "-c", script],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout.strip(), r"^\d+\.\d+")


if __name__ == "__main__":
    unittest.main(verbosity=2)
