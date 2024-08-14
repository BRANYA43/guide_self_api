from django.contrib import admin

from travels.models import Language, Info


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
