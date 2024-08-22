from django.core.files.uploadedfile import SimpleUploadedFile

from travels.schemas import InfoResolveMixin, MainImageResolveMixin, CountrySummarySchema
from utils.tests import BaseTestCase, MediaTestCase


class CountrySummarySchemaTest(BaseTestCase):
    def setUp(self):
        self.schema = CountrySummarySchema

    def test_schema_inherit_mixins(self):
        self.assertTrue(
            issubclass(
                self.schema,
                (InfoResolveMixin, MainImageResolveMixin),
            )
        )


class MainImageResolveMixinTest(MediaTestCase):
    def setUp(self):
        self.resolver = MainImageResolveMixin
        self.country = self.create_test_country()
        self.file = SimpleUploadedFile('main_image.png', b'image', 'image/png')

    def test_resolver_returns_main_image_file_url(self):
        image = self.create_test_image(content_obj=self.country, file=self.file)
        self.country.refresh_from_db()
        resolved_url = self.resolver.resolve_main_image(self.country)

        self.assertEqual(resolved_url, image.file.url)

    def test_resolver_returns_none(self):
        resolved_url = self.resolver.resolve_main_image(self.country)
        self.assertIsNone(resolved_url)


class InfoResolveMixinTest(BaseTestCase):
    def setUp(self):
        self.resolver = InfoResolveMixin
        self.country = self.create_test_country()
        self.lang = self.create_test_language()

    def test_resolver_returns_info_instance(self):
        info = self.create_test_info(content_obj=self.country, lang=self.lang)
        self.country.refresh_from_db()
        resolved_info = self.resolver.resolve_info(self.country)
        self.assertEqual(resolved_info.id, info.id)

    def test_resolver_returns_none(self):
        resolved_info = self.resolver.resolve_info(self.country)
        self.assertIsNone(resolved_info)
