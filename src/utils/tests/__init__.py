from datetime import timedelta
from typing import Type
from django.test import TestCase

from django.core.files.uploadedfile import UploadedFile
from django.db.models import Model

from travels.models import Language, Info, Image, Country, City, PlaceType, Place, Rout, RoutPoint


class BaseTestCase(TestCase):
    @staticmethod
    def _create_test_model_instance(model: Type[Model], **data):
        return model.objects.create(**data)

    def create_test_language(self, *, slug='language', code='la', **extra_fields) -> Language:
        return self._create_test_model_instance(Language, slug=slug, code=code, **extra_fields)

    def create_test_info(
        self,
        content_obj: Type[Model],
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

    def create_test_image(
        self,
        content_obj: Type[Model],
        *,
        file: Type[UploadedFile],
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

    def create_test_country(self, *, slug='country', **extra_fields) -> Country:
        return self._create_test_model_instance(Country, slug=slug, **extra_fields)

    def create_test_city(self, *, country: Country, slug='city', **extra_fields) -> City:
        return self._create_test_model_instance(City, country=country, slug=slug, **extra_fields)

    def create_test_place_type(self, *, slug='place_type', **extra_fields) -> PlaceType:
        return self._create_test_model_instance(PlaceType, slug=slug, **extra_fields)

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

    def create_test_rout(self, *, slug='rout', duration=timedelta(hours=1), **extra_fields) -> Rout:
        rout = self._create_test_model_instance(Rout, slug=slug, duration=duration, **extra_fields)
        rout.refresh_from_db()
        return rout

    def create_test_rout_point(self, *, rout: Rout, place: Place, **extra_fields) -> RoutPoint:
        return self._create_test_model_instance(RoutPoint, rout=rout, place=place, **extra_fields)
