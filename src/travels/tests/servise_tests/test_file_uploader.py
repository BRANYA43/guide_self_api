import os
import shutil
from pathlib import Path
from unittest.mock import MagicMock

from django.conf import settings
from django.test import TestCase, override_settings

from travels.services.file_uploader import FileUploader

TEMP_MEDIA_ROOT: Path = settings.BASE_DIR / 'temp_media'


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FileUploaderTest(TestCase):
    def setUp(self):
        if not TEMP_MEDIA_ROOT.exists():
            os.mkdir(TEMP_MEDIA_ROOT)

        self.dir = 'files'
        self.uploader = FileUploader(self.dir)

        self.content_type = MagicMock()
        self.content_type.name = 'Model'
        self.instance = MagicMock(
            slug='test_file',
            content_type=self.content_type,
        )

    def tearDown(self):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_uploader_returns_path(self):
        self.assertEqual(
            self.uploader(self.instance, 'new_file.txt'),
            str(Path(self.dir, self.instance.content_type.name.lower(), f'{self.instance.slug}.txt')),
        )

    def test_uploader_removes_existed_file(self):
        path = Path(
            TEMP_MEDIA_ROOT,
            self.dir,
            self.instance.content_type.name.lower(),
            f'{self.instance.slug}.txt',
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

        self.assertTrue(path.exists())

        self.uploader(self.instance, 'new_file.txt')

        self.assertFalse(path.exists())
