from datetime import timedelta
from pathlib import Path

from admin_ordering.models import OrderableModel
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from travels.models import (
    Language,
    Info,
    Image,
    MainImage,
    ExtraImage,
    ImageAndInfoBaseModel,
    Country,
    City,
    PlaceType,
    Place,
    Rout,
    RoutPoint,
    Journey,
)
from utils.models import BaseModel, UUIDMixin, DatesMixin
from utils.tests import BaseTestCase, MediaTestCase


class JourneyModelTest(BaseTestCase):
    def setUp(self):
        self.country = self.create_test_country()
        self.city = self.create_test_city(country=self.country)
        self.place = self.create_test_place(city=self.city)
        self.rout = self.create_test_rout()
        self.user = get_user_model().objects.create_user(username='rick', password='rick1234')
        self.data = dict(
            user=self.user,
            rout=self.rout,
        )

    def test_model_inherits_mixins(self):
        self.assertTrue(issubclass(RoutPoint, (UUIDMixin, DatesMixin)))

    def test_create_model_instance(self):
        journey = Journey(**self.data)
        journey.full_clean()  # not raise


class RoutPointModelTest(BaseTestCase):
    def setUp(self):
        self.country = self.create_test_country()
        self.city = self.create_test_city(country=self.country)
        self.place = self.create_test_place(city=self.city)
        self.rout = self.create_test_rout()
        self.data = dict(
            rout=self.rout,
            place=self.place,
            ordering=1,
        )

    def test_model_inherits_mixins(self):
        self.assertTrue(issubclass(RoutPoint, (UUIDMixin, DatesMixin, OrderableModel)))

    def test_create_model_instance(self):
        point = RoutPoint(**self.data)
        point.full_clean()  # not raise

    def test_ordering_is_set_for_each_routs_individually_at_saving(self):
        rout_1 = self.create_test_rout(slug='rout_1')
        rout_2 = self.create_test_rout(slug='rout_2')

        point_1_1 = RoutPoint.objects.create(rout=rout_1, place=self.place)
        point_1_2 = RoutPoint.objects.create(rout=rout_1, place=self.place)
        point_2_1 = RoutPoint.objects.create(rout=rout_2, place=self.place)
        point_2_2 = RoutPoint.objects.create(rout=rout_2, place=self.place)

        self.assertEqual(point_1_1.ordering, 10)
        self.assertEqual(point_1_2.ordering, 20)
        self.assertEqual(point_2_1.ordering, 10)
        self.assertEqual(point_2_2.ordering, 20)

    async def test_previous_property_returns_previous_rout_point_or_none(self):
        del self.data['ordering']
        point_1 = await RoutPoint.objects.acreate(**self.data, ordering=10)
        point_2 = await RoutPoint.objects.acreate(**self.data, ordering=20)

        self.assertIsNone(await point_1.previous)
        self.assertEqual((await point_2.previous).id, point_1.id)

    async def test_next_property_returns_next_rout_point_or_none(self):
        del self.data['ordering']
        point_1 = await RoutPoint.objects.acreate(**self.data, ordering=10)
        point_2 = await RoutPoint.objects.acreate(**self.data, ordering=20)

        self.assertEqual((await point_1.next).id, point_2.id)
        self.assertIsNone(await point_2.next)


class RoutModelTest(BaseTestCase):
    def setUp(self):
        self.data = dict(
            slug='pretty_kharkiv',
            duration=timedelta(hours=1),
        )

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(Rout, ImageAndInfoBaseModel))

    def test_create_model_instance(self):
        rout = Rout(**self.data)
        rout.full_clean()  # not raise

    def test_duration_field_cannot_be_less_that_0(self):
        self.data['duration'] = timedelta(seconds=-1)
        rout = Rout(**self.data)

        self.assertRaisesRegex(
            ValidationError,
            r'Ensure this value is greater than or equal to 0:00:00.',
            rout.full_clean,
        )


class PlaceModelTest(BaseTestCase):
    def setUp(self):
        self.country = self.create_test_country()
        self.city = self.create_test_city(country=self.country)
        self.data = dict(
            slug='monument',
            city=self.city,
            latitude=0,
            longitude=0,
        )

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(Place, ImageAndInfoBaseModel))

    def test_create_model_instance(self):
        place = Place(**self.data)
        place.full_clean()

    def test_latitude_field_must_be_in_specified_range(self):
        place = Place(**self.data)

        place.latitude = -90
        place.full_clean()  # not raise

        place.latitude = 90
        place.full_clean()  # not raise

        place.latitude = -90.1
        self.assertRaisesRegex(
            ValidationError,
            r'Latitude must be in the range from -90 to 90 inclusive.',
            place.full_clean,
        )
        place.latitude = 90.1
        self.assertRaisesRegex(
            ValidationError,
            r'Latitude must be in the range from -90 to 90 inclusive.',
            place.full_clean,
        )

    def test_longitude_field_must_be_in_specified_range(self):
        place = Place(**self.data)

        place.longitude = -180
        place.full_clean()  # not raise

        place.longitude = 180
        place.full_clean()  # not raise

        place.longitude = -180.1
        self.assertRaisesRegex(
            ValidationError,
            r'Longitude must be in the range from -180 to 180 inclusive.',
            place.full_clean,
        )
        place.longitude = 180.1
        self.assertRaisesRegex(
            ValidationError,
            r'Longitude must be in the range from -180 to 180 inclusive.',
            place.full_clean,
        )


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


class ExtraImageProxyModelTest(MediaTestCase):
    def setUp(self):
        self.file = SimpleUploadedFile(name='image.png', content=b'imagepng', content_type='image/png')
        self.lang = self.create_test_language()
        self.image = ExtraImage(slug='lang_image', content_obj=self.lang, file=self.file)

    def test_model_inherit_image(self):
        self.assertTrue(issubclass(ExtraImage, Image))

    def test_model_sets_type_as_MAIN_at_save_time(self):
        self.image.save()
        self.assertEqual(self.image.type, Image.Type.EXTRA)


class MainImageProxyModelTest(MediaTestCase):
    def setUp(self):
        self.file = SimpleUploadedFile(name='image.png', content=b'imagepng', content_type='image/png')
        self.lang = self.create_test_language()
        self.image = MainImage(slug='lang_image', content_obj=self.lang, file=self.file)

    def test_model_inherit_image(self):
        self.assertTrue(issubclass(MainImage, Image))

    def test_model_sets_type_as_MAIN_at_save_time(self):
        self.image.save()
        self.assertEqual(self.image.type, Image.Type.MAIN)


class ImageModelTest(MediaTestCase):
    def setUp(self):
        self.file = SimpleUploadedFile(name='image.png', content=b'imagepng', content_type='image/png')
        self.lang = self.create_test_language()
        self.image = Image(slug='lang_image', content_obj=self.lang, file=self.file)

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(Image, BaseModel))

    def test_file_field_uses_uploader(self):
        self.image.save()
        self.assertEqual(
            self.image.file.path, str(Path(self.TEMP_MEDIA_ROOT.name, 'images/language', f'{self.image.slug}.png'))
        )


class InfoModelTest(BaseTestCase):
    def setUp(self):
        self.lang = self.create_test_language()
        self.data = dict(slug='info', name='new info', lang=self.lang, content_obj=self.lang)

    def test_model_inherit_base_model(self):
        self.assertTrue(issubclass(Info, BaseModel))

    def test_create_model_instance(self):
        info = Info(**self.data)
        info.full_clean()  # not raise

    def test_short_descr_field_have_2048_max_length(self):
        self.data['short_descr'] = 'a' * 2048
        info = Info(**self.data)
        info.full_clean()  # not raise

        info.short_descr += 'a'
        self.assertRaisesRegex(
            ValidationError,
            r'Ensure this value has at most 2048 characters \(it has 2049\).',
            info.full_clean,
        )

    def test_full_descr_field_have_4096_max_length(self):
        self.data['full_descr'] = 'a' * 4096
        info = Info(**self.data)
        info.full_clean()  # not raise

        info.full_descr += 'a'
        self.assertRaisesRegex(
            ValidationError,
            r'Ensure this value has at most 4096 characters \(it has 4097\).',
            info.full_clean,
        )


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
