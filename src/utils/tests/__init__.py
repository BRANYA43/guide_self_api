from datetime import timedelta
from tempfile import TemporaryDirectory
from typing import TypeVar

from django.conf import settings

from django.core.files.uploadedfile import UploadedFile
from django.db.models import Model
from django.test import override_settings, TestCase

from travels.models import Language, Info, Image, Country, City, PlaceType, Place, Rout, RoutPoint

TModel = TypeVar('TModel', bound=Model)
TUploadedFile = TypeVar('TUploadedFile', bound=UploadedFile)

TEMP_MEDIA_ROOT = TemporaryDirectory(dir=settings.BASE_DIR)


class BaseTestCase(TestCase):
    @staticmethod
    def _create_test_model_instance(model: type[Model], **data):
        return model.objects.create(**data)

    @staticmethod
    async def _acreate_test_model_instance(model: type[Model], **data):
        return await model.objects.acreate(**data)

    def create_test_language(self, *, slug='language', code='la', **extra_fields) -> Language:
        return self._create_test_model_instance(Language, slug=slug, code=code, **extra_fields)

    async def acreate_test_language(self, *, slug='language', code='la', **extra_fields) -> Language:
        return await self._acreate_test_model_instance(Language, slug=slug, code=code, **extra_fields)

    def create_test_info(
        self,
        content_obj: TModel,
        *,
        lang: Language,
        slug='info',
        name='name',
        **extra_fields,
    ) -> Info:
        return self._create_test_model_instance(
            Info,
            content_obj=content_obj,
            lang=lang,
            slug=slug,
            name=name,
            **extra_fields,
        )

    async def acreate_test_info(
        self,
        content_obj: TModel,
        *,
        lang: Language,
        slug='info',
        name='name',
        **extra_fields,
    ) -> Info:
        return await self._acreate_test_model_instance(
            Info,
            content_obj=content_obj,
            lang=lang,
            slug=slug,
            name=name,
            **extra_fields,
        )

    def create_test_image(
        self,
        content_obj: TModel,
        *,
        file: TUploadedFile,
        slug='image',
        type=Image.Type.MAIN,
        **extra_fields,
    ) -> Image:
        return self._create_test_model_instance(
            Image,
            content_obj=content_obj,
            file=file,
            slug=slug,
            type=type,
            **extra_fields,
        )

    async def acreate_test_image(
        self,
        content_obj: TModel,
        *,
        file: TUploadedFile,
        slug='image',
        type=Image.Type.MAIN,
        **extra_fields,
    ) -> Image:
        return await self._acreate_test_model_instance(
            Image,
            content_obj=content_obj,
            file=file,
            slug=slug,
            type=type,
            **extra_fields,
        )

    def create_test_country(self, *, slug='country', **extra_fields) -> Country:
        return self._create_test_model_instance(Country, slug=slug, **extra_fields)

    async def acreate_test_country(self, *, slug='country', **extra_fields) -> Country:
        return await self._acreate_test_model_instance(Country, slug=slug, **extra_fields)

    def create_test_city(self, *, country: Country, slug='city', **extra_fields) -> City:
        return self._create_test_model_instance(City, country=country, slug=slug, **extra_fields)

    async def acreate_test_city(self, *, country: Country, slug='city', **extra_fields) -> City:
        return await self._acreate_test_model_instance(City, country=country, slug=slug, **extra_fields)

    def create_test_place_type(self, *, slug='place_type', **extra_fields) -> PlaceType:
        return self._create_test_model_instance(PlaceType, slug=slug, **extra_fields)

    async def acreate_test_place_type(self, *, slug='place_type', **extra_fields) -> PlaceType:
        return await self._acreate_test_model_instance(PlaceType, slug=slug, **extra_fields)

    def create_test_place(
        self,
        *,
        city: City,
        slug='place',
        latitude=0,
        longitude=0,
        **extra_fields,
    ) -> Place:
        place = self._create_test_model_instance(
            Place,
            city=city,
            slug=slug,
            latitude=latitude,
            longitude=longitude,
            **extra_fields,
        )
        place.refresh_from_db()
        return place

    async def acreate_test_place(
        self,
        *,
        city: City,
        slug='place',
        latitude=0,
        longitude=0,
        **extra_fields,
    ) -> Place:
        place = await self._acreate_test_model_instance(
            Place,
            city=city,
            slug=slug,
            latitude=latitude,
            longitude=longitude,
            **extra_fields,
        )
        await place.arefresh_from_db()
        return place

    def create_test_rout(self, *, slug='rout', duration=timedelta(hours=1), **extra_fields) -> Rout:
        rout = self._create_test_model_instance(Rout, slug=slug, duration=duration, **extra_fields)
        rout.refresh_from_db()
        return rout

    async def acreate_test_rout(self, *, slug='rout', duration=timedelta(hours=1), **extra_fields) -> Rout:
        rout = await self._acreate_test_model_instance(Rout, slug=slug, duration=duration, **extra_fields)
        await rout.arefresh_from_db()
        return rout

    def create_test_rout_point(self, *, rout: Rout, place: Place, **extra_fields) -> RoutPoint:
        return self._create_test_model_instance(RoutPoint, rout=rout, place=place, **extra_fields)

    async def acreate_test_rout_point(self, *, rout: Rout, place: Place, **extra_fields) -> RoutPoint:
        return await self._acreate_test_model_instance(RoutPoint, rout=rout, place=place, **extra_fields)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT.name)
class MediaTestCase(BaseTestCase):
    TEMP_MEDIA_ROOT = TEMP_MEDIA_ROOT

    def tearDown(self):
        self.TEMP_MEDIA_ROOT.cleanup()
