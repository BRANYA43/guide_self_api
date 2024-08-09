from django.test import TestCase
from travels.models import Language


class LanguageModelTest(TestCase):
    def setUp(self):
        self.lang = Language(slug='ukrainian', code='ua')

    def test_model_representation(self):
        self.assertEqual(str(self.lang), f'{self.lang.slug}, {self.lang.code}')
