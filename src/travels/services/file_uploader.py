from pathlib import Path
from typing import Type

from django.conf import settings
from django.db.models import Model
from django.utils.deconstruct import deconstructible


@deconstructible
class FileUploader:
    def __init__(self, dir: Path | str):
        self._root = settings.MEDIA_ROOT
        self._dir = dir

    def __call__(self, instance: Type[Model], filename: str, *args, **kwargs) -> str:
        filename = self.get_new_filename(filename, instance)
        path = Path(self._dir, self.get_model_name_of_content_obj(instance), filename)
        absolute_path = Path(self._root, path)
        absolute_path.unlink(missing_ok=True)
        return str(path)

    @staticmethod
    def get_new_filename(filename: str, instance: Type[Model]):
        extension = filename.split('.')[-1]
        return f'{instance.slug}.{extension}'

    @staticmethod
    def get_model_name_of_content_obj(instance: Type[Model]):
        return instance.content_type.name.lower()
