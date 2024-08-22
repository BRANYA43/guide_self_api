from ninja import ModelSchema

from travels.models import Info


########################################################################################################################
# Resolve Mixins
########################################################################################################################
class InfoResolveMixin:
    @staticmethod
    def resolve_info(obj) -> Info | None:
        return obj.info.first()


class MainImageResolveMixin:
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
