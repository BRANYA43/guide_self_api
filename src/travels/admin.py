from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline

from travels.models import (
    Language,
    Info,
    MainImage,
    ExtraImage,
    Country,
    City,
    PlaceType,
    Place,
    RoutPoint,
    Rout,
    Journey,
)


########################################################################################################################
# Inlines
########################################################################################################################
class RoutPointInline(OrderableAdmin, admin.TabularInline):
    model = RoutPoint
    fields = ('ordering', 'place', 'updated_at', 'created_at')
    readonly_fields = ('updated_at', 'created_at')
    ordering_field_hide_input = True


class MainImageInline(GenericStackedInline):
    model = MainImage
    fields = ('slug', 'file', 'updated_at', 'created_at')
    readonly_fields = ('updated_at', 'created_at')
    extra = 1
    max_num = 1

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=self.model.Type.MAIN)


class ExtraImageInline(GenericStackedInline):
    model = ExtraImage
    fields = ('slug', 'file', 'updated_at', 'created_at')
    readonly_fields = ('updated_at', 'created_at')
    extra = 1
    per_page = 2

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=self.model.Type.EXTRA)


class InfoInline(GenericTabularInline):
    model = Info
    fields = ('slug', 'lang', 'name', 'updated_at', 'created_at')
    readonly_fields = ('updated_at', 'created_at')
    extra = 1
    show_change_link = True


########################################################################################################################
# Models
########################################################################################################################
@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'updated_at', 'created_at')
    readonly_fields = ('id', 'updated_at', 'created_at')
    fieldsets = (
        ('General Information', dict(fields=('id', 'status', 'user', 'rout', 'point'))),
        ('Dates', dict(fields=('updated_at', 'created_at'))),
    )
    ordering = ('status', '-created_at')
    search_fields = ('rout__slug', 'point__place__slug', 'user__email', 'user__username')
    list_filter = ('status',)


@admin.register(Rout)
class RoutAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'duration', 'updated_at', 'created_at')
    readonly_fields = ('updated_at', 'created_at')
    fieldsets = (
        ('General Information', dict(fields=('slug', 'duration'))),
        ('Dates', dict(fields=('updated_at', 'created_at'))),
    )
    ordering = ('slug',)
    search_fields = ('slug',)
    inlines = (RoutPointInline, MainImageInline, ExtraImageInline, InfoInline)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'type', 'updated_at', 'created_at')
    readonly_fields = ('updated_at', 'created_at')
    fieldsets = (
        ('General Information', dict(fields=('slug', 'type', 'city'))),
        ('GPS Coordinates', dict(fields=('latitude', 'longitude'))),
        ('Dates', dict(fields=('updated_at', 'created_at'))),
    )
    ordering = ('type__slug', 'slug')
    search_fields = ('slug', 'type__slug')
    inlines = (MainImageInline, ExtraImageInline, InfoInline)


@admin.register(PlaceType)
class PlaceTypeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_at', 'created_at')
    readonly_fields = ('updated_at', 'created_at')
    fieldsets = (
        ('General Information', dict(fields=('slug',))),
        ('Dates', dict(fields=('updated_at', 'created_at'))),
    )
    ordering = ('slug',)
    search_fields = ('slug',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_at', 'created_at')
    readonly_fields = ('updated_at', 'created_at')
    fieldsets = (
        ('General Information', dict(fields=('slug',))),
        ('Dates', dict(fields=('updated_at', 'created_at'))),
    )
    ordering = ('slug',)
    search_fields = ('slug',)
    inlines = (MainImageInline, ExtraImageInline, InfoInline)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'country', 'updated_at', 'created_at')
    readonly_fields = ('updated_at', 'created_at')
    fieldsets = (
        ('General Information', dict(fields=('slug', 'country'))),
        ('Dates', dict(fields=('updated_at', 'created_at'))),
    )
    ordering = ('slug', 'country__slug')
    search_fields = ('slug', 'country__slug')
    inlines = (MainImageInline, ExtraImageInline, InfoInline)


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('slug', 'lang', 'updated_at', 'created_at')
    readonly_fields = ('updated_at', 'created_at', 'get_related_obj')
    fieldsets = (
        ('General Information', dict(fields=('get_related_obj', 'slug', 'name', 'short_descr', 'descr', 'lang'))),
        ('Dates', dict(fields=('updated_at', 'created_at'))),
    )
    ordering = ('lang', 'slug')
    search_fields = ('slug', 'lang__slug', 'lang__code')

    @admin.display(description='Related Object')
    def get_related_obj(self, instance: Info):
        return str(instance.content_obj)

    def has_add_permission(self, request):
        return False


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_at', 'created_at')
    readonly_fields = ('updated_at', 'created_at')
    fieldsets = (
        ('General Information', dict(fields=('slug', 'code'))),
        ('Dates', dict(fields=('updated_at', 'created_at'))),
    )
    ordering = ('slug',)
    search_fields = ('slug', 'code')
