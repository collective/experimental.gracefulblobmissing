from experimental.gracefulblobmissing import patches
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import subprocess
import sys
import tempfile
import unittest


class MissingBlobTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.filename = Path(self.directory.name) / "nested" / "blob"

    def test_create_missing_blob_and_directory(self):
        patches.create_empty_blob(str(self.filename))
        self.assertTrue(self.filename.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))

    def test_zodb_load_creates_missing_blob(self):
        helper = Mock()
        helper.getBlobFilename.return_value = str(self.filename)
        storage = SimpleNamespace(fshelper=helper)
        self.assertEqual(
            patches.patched_loadBlob_zodb(storage, b"oid", b"serial"),
            str(self.filename),
        )
        helper.getBlobFilename.assert_called_once_with(b"oid", b"serial")
        self.assertTrue(self.filename.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))

    def test_zodb_load_preserves_existing_blob(self):
        self.filename.parent.mkdir()
        self.filename.write_bytes(b"existing content")
        storage = SimpleNamespace(
            fshelper=SimpleNamespace(
                getBlobFilename=lambda oid, serial: str(self.filename)
            )
        )
        self.assertEqual(
            patches.patched_loadBlob_zodb(storage, b"oid", b"serial"),
            str(self.filename),
        )
        self.assertEqual(self.filename.read_bytes(), b"existing content")


class ConfigurationTests(unittest.TestCase):
    def test_zcml_registers_blob_patch(self):
        subprocess.run(
            [
                sys.executable,
                "-c",
                "from zope.configuration import xmlconfig; "
                "import experimental.gracefulblobmissing as package; "
                "from experimental.gracefulblobmissing.patches import patched_blob_init; "
                "from ZODB.blob import BlobFile; "
                "xmlconfig.file('configure.zcml', package); "
                "assert BlobFile.__init__ is patched_blob_init",
            ],
            check=True,
        )
