from django.contrib import admin
from .models import User, GeneralUser, UserStatus, MeetPeople, GENERAL_USER, BUSINESS_USER


class TypeFilter(admin.SimpleListFilter):
    title = 'type'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return [
            ('A', 'Admin'),
            ('U', 'General User'),
            ('B', 'Business Owner')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'A':
            return queryset.filter(is_staff=True)
        elif self.value() == 'U':
            pks = [obj.pk for obj in queryset
                   if obj.type == GENERAL_USER and obj.is_staff == False]
            return queryset.filter(pk__in=pks)
        elif self.value() == 'B':
            pks = [obj.pk for obj in queryset if obj.type == BUSINESS_USER]
            return queryset.filter(pk__in=pks)
        else:
            return queryset


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email', 'type')
    readonly_fields = ('pk', 'type')
    fieldsets = (
        ('Auth', {
            'fields': ('pk', 'type', 'username', 'email', 'password')
        }),
        ('Identity information', {
            'fields': ('first_name', 'last_name', 'national_code', 'phone_number'),
        }),
        ('Others', {
            'fields': ('is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined')
        })
    )
    list_filter = (TypeFilter, 'date_joined')
    search_fields = ('username', 'email', 'first_name',
                     'last_name', 'national_code', 'phone_number')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.set_password(obj.password)
        obj.save()

    def type(self, obj):
        if obj.is_staff:
            return 'Admin'
        if hasattr(obj, 'generaluser'):
            return 'General user'
        if hasattr(obj, 'businessowner'):
            return 'Business owner'
