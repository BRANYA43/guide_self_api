from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile
from ninja.testing import TestClient

from travels.api import router
from travels.models import Country
from travels.schemas import CountrySummarySchema, CountryDetailSchema
from utils.tests import MediaTestCase


class CountryRetrieveAPITest(MediaTestCase):
    def setUp(self):
        self.schema = CountryDetailSchema
        self.client = TestClient(router)
        self.country = self.create_test_country(slug='ukraine')
        self.lang = self.create_test_language(slug='english', code='en')
        self.file = SimpleUploadedFile('main_image.png', b'image', 'image/png')
        self.create_test_info(
            self.country,
            lang=self.lang,
            slug=self.country.slug + '_' + self.lang.code,
            name=self.country.slug.title(),
            full_descr='Full Lorem Text',
        )
        self.create_test_image(
            self.country,
            file=self.file,
            slug=self.country.slug + '_main_image',
        )

    def test_api_returns_country_detail_data(self):
        expected_data = dict(**self.schema.from_orm(self.country).dict(exclude=['id']), id=str(self.country.id))
        response = self.client.get(f'/countries/{self.country.id}', headers={'Accept-Language': 'en'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_data)

    def test_api_returns_404_error(self):
        response = self.client.get(f'/countries/{uuid4()}', headers={'Accept-Language': 'en'})

        self.assertEqual(response.status_code, 404)


class CountryListAPITest(MediaTestCase):
    def setUp(self):
        self.schema = CountrySummarySchema
        self.client = TestClient(router)
        self.country_1 = self.create_test_country(slug='england')
        self.country_2 = self.create_test_country(slug='france')
        self.country_3 = self.create_test_country(slug='ukraine')
        self.countries = Country.objects.all().order_by('slug')

        self.lang = self.create_test_language(slug='english', code='en')
        self.file = SimpleUploadedFile('main_image.png', b'image', 'image/png')

        self.create_info_and_main_image_for_country()

    def create_info_and_main_image_for_country(self):
        short_descr = 'Short Lorem Text'
        for country in self.countries:
            self.create_test_info(
                country,
                lang=self.lang,
                slug=country.slug + '_' + self.lang.code,
                name=country.slug.title(),
                short_descr=short_descr,
            )
            self.create_test_image(
                country,
                file=self.file,
                slug=country.slug + '_main_image',
            )
            country.refresh_from_db()

    def test_api_returns_country_list_data(self):
        expected_data = [
            dict(**self.schema.from_orm(country).dict(exclude=['id']), id=str(country.id)) for country in self.countries
        ]
        response = self.client.get('/countries', headers={'Accept-Language': 'en'})

        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertEqual(response.json(), expected_data)
