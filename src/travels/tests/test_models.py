import shutil
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from travels.models import Language, Info, Image, MainImage, ExtraImage, ImageAndInfoBaseModel, Country, City, PlaceType
from utils.models import BaseModel
from utils.tests import BaseTestCase

TEMP_MEDIA_ROOT: Path = settings.BASE_DIR / 'temp_media'


class PlaceTypeModelTest(BaseTestCase):
    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(PlaceType, BaseModel))

    def test_create_model_instance(self):
        place_type = PlaceType(slug='cafe')
        place_type.full_clean()  # not raise


class CityModelTest(BaseTestCase):
    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(City, ImageAndInfoBaseModel))

    def test_create_model_instance(self):
        country = self.create_test_country()
        city = City(slug='ukraine', country=country)
        city.full_clean()  # not raise


class CountryModelTest(BaseTestCase):
    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(Country, ImageAndInfoBaseModel))

    def test_create_model_instance(self):
        country = Country(slug='ukraine')
        country.full_clean()  # not raise


class ImageAndInfoBaseModelTest(BaseTestCase):
    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(ImageAndInfoBaseModel, BaseModel))


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ExtraImageProxyModelTest(BaseTestCase):
    def setUp(self):
        self.file = SimpleUploadedFile(name='image.png', content=b'imagepng', content_type='image/png')
        self.lang = self.create_test_language()
        self.image = ExtraImage(slug='lang_image', content_obj=self.lang, file=self.file)

    def tearDown(self):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_model_inherit_image(self):
        self.assertTrue(issubclass(ExtraImage, Image))

    def test_model_sets_type_as_MAIN_at_save_time(self):
        self.image.save()
        self.assertEqual(self.image.type, Image.Type.EXTRA)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class MainImageProxyModelTest(BaseTestCase):
    def setUp(self):
        self.file = SimpleUploadedFile(name='image.png', content=b'imagepng', content_type='image/png')
        self.lang = self.create_test_language()
        self.image = MainImage(slug='lang_image', content_obj=self.lang, file=self.file)

    def tearDown(self):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_model_inherit_image(self):
        self.assertTrue(issubclass(MainImage, Image))

    def test_model_sets_type_as_MAIN_at_save_time(self):
        self.image.save()
        self.assertEqual(self.image.type, Image.Type.MAIN)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ImageModelTest(BaseTestCase):
    def setUp(self):
        self.file = SimpleUploadedFile(name='image.png', content=b'imagepng', content_type='image/png')
        self.lang = self.create_test_language()
        self.image = Image(slug='lang_image', content_obj=self.lang, file=self.file)

    def tearDown(self):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(Image, BaseModel))

    def test_file_field_uses_uploader(self):
        self.image.save()
        self.assertEqual(self.image.file.path, str(Path(TEMP_MEDIA_ROOT, 'images/language', f'{self.image.slug}.png')))


class InfoModelTest(BaseTestCase):
    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(Info, BaseModel))

    def test_create_model_instance(self):
        lang = self.lang = self.create_test_language()
        info = Info(slug='info', name='new info', lang=lang, content_obj=lang)
        info.full_clean()  # not raise


class LanguageModelTest(BaseTestCase):
    def setUp(self):
        self.data = dict(slug='ukrainian', code='ua')

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(Language, BaseModel))

    def test_create_model_instance(self):
        lang = Language(**self.data)
        lang.full_clean()  # not raise

    def test_model_representation(self):
        lang = Language(**self.data)
        self.assertEqual(str(lang), f'{lang.slug}, {lang.code}')
