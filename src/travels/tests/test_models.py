import shutil
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from travels.models import Language, Info, Image, MainImage, ExtraImage, ImageAndInfoBaseModel, Country, City
from utils.models import BaseModel

TEMP_MEDIA_ROOT: Path = settings.BASE_DIR / 'temp_media'


class CityModelTest(TestCase):
    country_model = Country
    city_model = City

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(self.country_model, ImageAndInfoBaseModel))

    def test_create_model_instance(self):
        country = self.country_model.objects.create(slug='ukraine')
        city = self.city_model(slug='ukraine', country=country)
        city.full_clean()  # not raise


class CountryModelTest(TestCase):
    country_model = Country

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(self.country_model, ImageAndInfoBaseModel))

    def test_create_model_instance(self):
        country = self.country_model(slug='ukraine')
        country.full_clean()  # not raise


class ImageAndInfoBaseModelTest(TestCase):
    base_model = ImageAndInfoBaseModel

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(self.base_model, BaseModel))


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ExtraImageProxyModelTest(TestCase):
    lang_model = Language
    image_model = ExtraImage

    def setUp(self):
        self.file = SimpleUploadedFile(name='image.png', content=b'imagepng', content_type='image/png')
        self.lang = self.lang_model(slug='ukrainian', code='ua')
        self.image = self.image_model(slug='lang_image', content_obj=self.lang, file=self.file)

    def tearDown(self):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(self.image_model, Image))

    def test_model_sets_type_as_MAIN_at_save_time(self):
        self.image.save()
        self.assertEqual(self.image.type, Image.Type.EXTRA)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class MainImageProxyModelTest(TestCase):
    lang_model = Language
    image_model = MainImage

    def setUp(self):
        self.file = SimpleUploadedFile(name='image.png', content=b'imagepng', content_type='image/png')
        self.lang = self.lang_model.objects.create(slug='ukrainian', code='ua')
        self.image = self.image_model(slug='lang_image', content_obj=self.lang, file=self.file)

    def tearDown(self):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(self.image_model, Image))

    def test_model_sets_type_as_MAIN_at_save_time(self):
        self.image.save()
        self.assertEqual(self.image.type, Image.Type.MAIN)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ImageModelTest(TestCase):
    lang_model = Language
    image_model = Image

    def setUp(self):
        self.file = SimpleUploadedFile(name='image.png', content=b'imagepng', content_type='image/png')
        self.lang = self.lang_model.objects.create(slug='ukrainian', code='ua')
        self.image = self.image_model(slug='lang_image', content_obj=self.lang, file=self.file)

    def tearDown(self):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(self.image_model, BaseModel))

    def test_file_field_uses_uploader(self):
        self.image.save()
        self.assertEqual(self.image.file.path, str(Path(TEMP_MEDIA_ROOT, 'images/language', f'{self.image.slug}.png')))


class InfoModelTest(TestCase):
    lang_model = Language
    info_model = Info

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(self.info_model, BaseModel))

    def test_create_model_instance(self):
        lang = self.lang_model.objects.create(slug='ukrainian', code='ua')
        info = self.info_model(slug='info', name='new info', lang=lang, content_obj=lang)
        info.full_clean()  # not raise


class LanguageModelTest(TestCase):
    lang_model = Language

    def setUp(self):
        self.data = dict(slug='ukrainian', code='ua')

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(self.lang_model, BaseModel))

    def test_create_model_instance(self):
        lang = self.lang_model(**self.data)
        lang.full_clean()  # not raise

    def test_model_representation(self):
        lang = self.lang_model(**self.data)
        self.assertEqual(str(lang), f'{lang.slug}, {lang.code}')
