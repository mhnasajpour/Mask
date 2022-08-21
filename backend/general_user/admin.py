from django.contrib import admin
from .models import User, GeneralUser, UserStatus, MeetPeople, GENERAL_USER, BUSINESS_USER
from django.utils.html import format_html
from public_place.models import BusinessOwner


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


class StatusFilter(admin.SimpleListFilter):
    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            (1, 'Healthy'),
            (2, 'Doubtful'),
            (3, 'Perilous'),
            (4, 'Patient'),
            (5, 'Dead')
        ]

    def queryset(self, request, queryset):
        if self.value():
            pks = [obj.pk for obj in queryset if obj.status ==
                   int(self.value())]
            return queryset.filter(pk__in=pks)
        else:
            return queryset


@admin.register(GeneralUser)
class GeneralUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email', 'status')
    readonly_fields = ('user', 'first_name', 'last_name', 'email', 'status')
    fieldsets = (
        ('User', {
            'fields': ('status', 'user', 'first_name', 'last_name', 'email')
        }),
        ('Others', {
            'fields': ('birth_date', 'blood_type', 'height', 'weight')
        })
    )
    list_filter = (StatusFilter, 'date_created')
    search_fields = ('user__username', 'user__email', 'user__first_name',
                     'user__last_name', 'user__national_code', 'user__phone_number')

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def email(self, obj):
        return obj.user.email

    def status(self, obj):
        if obj.status == 1:
            color = '60,179,113'
        if obj.status == 2:
            color = '255,180,51'
        if obj.status == 3:
            color = '225,52,45'
        if obj.status == 4:
            color = '142,15,6'
        if obj.status == 5:
            color = '50,50,50'
        return format_html(f'<p style="background-color: rgb({color}); color: white; padding: 1px 3px; width: 30px; border-radius: 10px; text-align: center; margin: 0px; font-size: 11px;">{obj.status}</p>')


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('pk', 'first_name', 'last_name', 'email', 'type', 'color')
    fieldsets = (
        (None, {
            'fields': ('pk', 'user', 'color', 'status', 'date_created')
        }),
        ('Factor', {
            'fields': ('type', 'effective_factor')
        })
    )
    readonly_fields = ('pk', 'user', 'color', 'date_created')
    list_filter = ('type', StatusFilter, 'date_created')
    search_fields = ('user__user__first_name', 'user__user__last_name',
                     'user__user__email', 'effective_factor')

    def user(self, obj):
        return obj.user

    def first_name(self, obj):
        return obj.user.user.first_name

    def last_name(self, obj):
        return obj.user.user.last_name

    def email(self, obj):
        return obj.user.user.email

    def color(self, obj):
        if obj.status == 1:
            color = '60,179,113'
        if obj.status == 2:
            color = '255,180,51'
        if obj.status == 3:
            color = '225,52,45'
        if obj.status == 4:
            color = '142,15,6'
        if obj.status == 5:
            color = '50,50,50'
        return format_html(f'<p style="background-color: rgb({color}); color: white; padding: 1px 3px; width: 30px; border-radius: 10px; text-align: center; margin: 0px; font-size: 11px;">{obj.status}</p>')


@admin.register(MeetPeople)
class MeetPeopleAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('pk', 'first_name1', 'last_name1',
                    'first_name2', 'last_name2', 'date_created')
    fields = ('pk', 'user1', 'user2', 'date_created')
    readonly_fields = ('pk', 'user1', 'user2', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('user1__user__first_name', 'user2__user__first_name', 'user1__user__last_name',
                     'user2__user__last_name', 'user1__user__email', 'user2__user__email')

    def user1(self, obj):
        return obj.user1

    def user2(self, obj):
        return obj.user2

    def first_name1(self, obj):
        return obj.user1.user.first_name

    def last_name1(self, obj):
        return obj.user1.user.last_name

    def first_name2(self, obj):
        return obj.user2.user.first_name

    def last_name2(self, obj):
        return obj.user2.user.last_name
