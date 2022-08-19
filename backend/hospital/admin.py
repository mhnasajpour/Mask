from django.contrib import admin
from django.utils.html import format_html
from .models import Hospital


@admin.register(Hospital)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'zip_code', 'address')
    readonly_fields = ('pk', 'map')
    search_fields = ('name', 'zip_code', 'address')
    list_filter = ('city',)

    fieldsets = (
        ('Specifications', {
            'fields': ('pk', 'name', 'city', 'zip_code')
        }),
        ('Address', {
            'fields': ('address', ('latitude', 'longitude'), 'map'),
        }),
    )
