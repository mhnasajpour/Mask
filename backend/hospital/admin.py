from django.contrib import admin
from django.utils.html import format_html
from .models import Hospital


@admin.register(Hospital)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'zip_code', 'address')
    readonly_fields = ('pk', 'map')

    fieldsets = (
        ('Specifications', {
            'fields': ('pk', 'name', 'city', 'zip_code')
        }),
        ('Address', {
            'fields': ('address', ('latitude', 'longitude'), 'map'),
        }),
    )

    def map(self, obj):
        return format_html(f'<iframe src="https://maps.google.com/maps?q={obj.latitude},{obj.longitude}&hl=en&z=16&amp;output=embed" width="483" height="300"></iframe>')
