from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinLengthValidator
from django.db import models

from travels.services.file_uploader import FileUploader
from utils.models import BaseModel


class Image(BaseModel):
    class Type(models.TextChoices):
        MAIN = 'main', 'main'
        EXTRA = 'extra', 'extra'

    type = models.CharField(
        verbose_name='Type',
        max_length=5,
        choices=Type.choices,
    )
    file = models.ImageField(
        verbose_name='File',
        upload_to=FileUploader('images'),
    )
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.PROTECT,
    )
    object_id = models.UUIDField()
    content_obj = GenericForeignKey()

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return str(self.slug)


class Info(BaseModel):
    name = models.CharField(
        verbose_name='Name',
        max_length=100,
        validators=[MinLengthValidator(2)],
    )
    short_descr = models.CharField(
        verbose_name='Short Description',
        max_length=2048,
        null=True,
        blank=True,
    )
    descr = models.CharField(
        verbose_name='Full Description',
        max_length=4096,
        null=True,
        blank=True,
    )
    lang = models.ForeignKey(
        verbose_name='Localization',
        to='Language',
        on_delete=models.PROTECT,
    )
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.PROTECT,
    )
    object_id = models.UUIDField()
    content_obj = GenericForeignKey()

    class Meta:
        verbose_name = 'Localized Information'
        verbose_name_plural = 'Localized Information'

    def __str__(self):
        return str(self.slug)


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
