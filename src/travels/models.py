from django.core.validators import MinLengthValidator
from django.db import models

from utils.models import BaseModel


class Language(BaseModel):
    code = models.CharField(
        verbose_name='ISO Code',
        max_length=2,
        validators=[MinLengthValidator(2)],
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        default_related_name = 'langs'

    def __str__(self):
        return f'{self.slug}, {self.code}'
