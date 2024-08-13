import shutil
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from travels.models import Language, Info, Image, MainImage

TEMP_MEDIA_ROOT: Path = settings.BASE_DIR / 'temp_media'


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class MainImageProxyModelTest(TestCase):
    def setUp(self):
        self.file = SimpleUploadedFile(name='image.png', content=b'imagepng', content_type='image/png')
        self.lang = Language(slug='ukrainian', code='ua')
        self.image = MainImage(slug='lang_image', content_obj=self.lang, file=self.file)

    def tearDown(self):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_model_sets_type_as_MAIN_at_save_time(self):
        self.image.save()
        self.assertEqual(self.image.type, Image.Type.MAIN)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ImageModelTest(TestCase):
    def setUp(self):
        self.file = SimpleUploadedFile(name='image.png', content=b'imagepng', content_type='image/png')
        self.lang = Language(slug='ukrainian', code='ua')
        self.image = Image(slug='lang_image', content_obj=self.lang, file=self.file)

    def tearDown(self):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_model_representation(self):
        self.assertEqual(str(self.image), self.image.slug)

    def test_file_field_uses_uploader(self):
        self.image.save()
        self.assertEqual(self.image.file.path, str(Path(TEMP_MEDIA_ROOT, 'images/language', f'{self.image.slug}.png')))


class InfoModelTest(TestCase):
    def setUp(self):
        self.lang = Language(slug='ukrainian', code='ua')
        self.info = Info(slug='info', name='new info', lang=self.lang, content_obj=self.lang)

    def test_model_representation(self):
        self.assertEqual(str(self.info), self.info.slug)


class LanguageModelTest(TestCase):
    def setUp(self):
        self.lang = Language(slug='ukrainian', code='ua')

    def test_model_representation(self):
        self.assertEqual(str(self.lang), f'{self.lang.slug}, {self.lang.code}')
