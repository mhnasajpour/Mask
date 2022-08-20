from django.contrib import admin
from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'zip_code', 'address')
    readonly_fields = ('pk', 'map')
    list_filter = ('city',)
    fieldsets = (
        ('Specifications', {
            'fields': ('pk', 'name', 'city', 'zip_code')
        }),
        ('Address', {
            'fields': ('address', ('latitude', 'longitude'), 'map'),
        }),
    )

    def has_add_permission(self, request):
        return False
