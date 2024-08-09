from django.test import TestCase
from travels.models import Language, Info


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
