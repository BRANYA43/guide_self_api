from django.test import TestCase

from utils.models import BaseModel


class TestModel(BaseModel):
    class Meta:
        managed = False


class BaseModelTest(TestCase):
    def test_model_str_representation(self):
        instance = TestModel(slug='slug')
        self.assertEqual(str(instance), instance.slug)
