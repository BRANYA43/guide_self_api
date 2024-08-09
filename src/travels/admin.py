from django.contrib import admin

from travels.models import Language


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
