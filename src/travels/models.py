from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinLengthValidator
from django.db import models

from travels.services.file_uploader import FileUploader
from travels.validators import GPSCoordinateValidator
from utils.models import BaseModel


########################################################################################################################
# Abstract Models
########################################################################################################################
class ImageAndInfoBaseModel(BaseModel):
    info = GenericRelation(
        verbose_name='Localized Information',
        to='Info',
    )
    main_image = GenericRelation(
        verbose_name='Main Image',
        to='MainImage',
    )
    extra_images = GenericRelation(
        verbose_name='Extra Images',
        to='ExtraImage',
    )

    class Meta:
        abstract = True


########################################################################################################################
# Models
########################################################################################################################
class Place(ImageAndInfoBaseModel):
    type = models.ForeignKey(
        verbose_name='Type',
        to='PlaceType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    city = models.ForeignKey(
        verbose_name='City',
        to='City',
        on_delete=models.PROTECT,
    )
    latitude = models.DecimalField(
        verbose_name='Latitude',
        max_digits=7,
        decimal_places=5,
        validators=[GPSCoordinateValidator('latitude')],
    )
    longitude = models.DecimalField(
        verbose_name='Longitude',
        max_digits=8,
        decimal_places=5,
        validators=[GPSCoordinateValidator('longitude')],
    )

    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'
        default_related_name = 'places'


class PlaceType(BaseModel):
    class Meta:
        verbose_name = 'Place Type'
        verbose_name_plural = 'Place Types'
        default_related_name = 'types'


class City(ImageAndInfoBaseModel):
    country = models.ForeignKey(
        verbose_name='Country',
        to='Country',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        default_related_name = 'langs'


class Country(ImageAndInfoBaseModel):
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


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


########################################################################################################################
# Polymorph Models
########################################################################################################################
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


########################################################################################################################
# Proxy Models
########################################################################################################################
class MainImage(Image):
    class Meta:
        verbose_name = 'Main Image'
        verbose_name_plural = 'Main Images'
        proxy = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.type != Image.Type.MAIN:
            self.type = Image.Type.MAIN
        super().save(force_insert, force_update, using, update_fields)


class ExtraImage(Image):
    class Meta:
        verbose_name = 'Extra Image'
        verbose_name_plural = 'Extra Images'
        proxy = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.type != Image.Type.EXTRA:
            self.type = Image.Type.EXTRA
        super().save(force_insert, force_update, using, update_fields)
