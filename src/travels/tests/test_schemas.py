from travels.schemas import InfoResolveMixin
from utils.tests import BaseTestCase


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
