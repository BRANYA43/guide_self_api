from ninja import ModelSchema, Schema
from pydantic import UUID4

from travels.models import Info, Country


########################################################################################################################
# Resolve Mixins
########################################################################################################################
class InfoResolveMixin(Schema):
    @staticmethod
    def resolve_info(obj) -> Info | None:
        return obj.info.first()


class MainImageResolveMixin(Schema):
    @staticmethod
    def resolve_main_image(obj):
        if (img := obj.main_image.first()) is not None:
            return img.file.url
        return img


########################################################################################################################
# Fields
########################################################################################################################
class InfoSummaryField(ModelSchema):
    class Meta:
        model = Info
        fields = ('name', 'short_descr')


class InfoDetailField(ModelSchema):
    class Meta:
        model = Info
        fields = ('name', 'full_descr')


########################################################################################################################
# CRUD Schemas
########################################################################################################################
class CountrySummarySchema(InfoResolveMixin, MainImageResolveMixin, ModelSchema):
    id: UUID4
    info: InfoSummaryField | None
    main_image: str | None

    class Meta:
        model = Country
        fields = ('id', 'info', 'main_image')
