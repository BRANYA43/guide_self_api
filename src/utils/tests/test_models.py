from django.test import TestCase

from utils.models import BaseModel


class TestModel(BaseModel):
    class Meta:
        managed = False


class BaseModelTest(TestCase):
    def test_create_model_instance(self):
        instance = TestModel(slug='slug')
        self.assertIsNotNone(instance.uuid)
        self.assertEqual(instance.slug, 'slug')
