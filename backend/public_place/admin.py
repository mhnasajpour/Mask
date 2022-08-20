import imp
from django import forms
from django.contrib import admin
from .models import Place, BusinessOwner, PlaceStatus, MeetPlace, WHITEPLACE, REDPLACE
from django_reverse_admin import ReverseModelAdmin
from django.utils.html import format_html
from general_user.models import GeneralUser


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'zip_code', 'address')
    readonly_fields = ('pk', 'map')
    list_filter = ('city',)
    search_fields = ('name', 'zip_code', 'address')
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


class BusinessOwnerModelForm(forms.ModelForm):
    change = forms.BooleanField(required=False)

    class Meta:
        model = BusinessOwner
        fields = '__all__'


class IsPaidFilter(admin.SimpleListFilter):
    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            (WHITEPLACE, 'WHITE'),
            (REDPLACE, 'RED')
        ]

    def queryset(self, request, queryset):
        if self.value():
            pks = [obj.pk for obj in queryset if obj.status == self.value()]
            return queryset.filter(pk__in=pks)
        else:
            return queryset


@admin.register(BusinessOwner)
class BusinessOwnerAdmin(ReverseModelAdmin):
    form = BusinessOwnerModelForm
    inline_type = 'stacked'
    inline_reverse = (
        ('user', {'fields': (('first_name', 'last_name'), ('username', 'password'),
                             'email', 'national_code', 'phone_number', 'is_staff', 'is_active')}),
        ('place', {'fields': ('name', 'city', 'zip_code',
                              'address', ('latitude', 'longitude'))}),
    )
    list_display = ('pk', 'name', 'zip_code',
                    'first_name', 'last_name', 'email')
    fields = ('pk', 'user_id', 'place_id', ('status', 'change'), 'map')
    readonly_fields = ('pk', 'user_id', 'place_id', 'status', 'map')
    list_filter = (IsPaidFilter,)
    search_fields = ('pk', 'place__name', 'place__city', 'place__zip_code',
                     'user__first_name', 'user__last_name', 'user__email', 'user__national_code')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.user.set_password(obj.user.password)
        if form.cleaned_data['change']:
            PlaceStatus.objects.create(
                place=obj,
                type=2 if obj.status == REDPLACE else 4,
                status=REDPLACE if obj.status == WHITEPLACE else WHITEPLACE)
        obj.user.save()

    def has_add_permission(self, request):
        return False

    def name(self, obj):
        return obj.place.name

    def zip_code(self, obj):
        return obj.place.zip_code

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def email(self, obj):
        return obj.user.email

    def user_id(self, obj):
        return obj.user.pk

    def place_id(self, obj):
        return obj.place.pk

    def map(self, obj):
        return obj.place.map


@admin.register(PlaceStatus)
class PlaceStatusAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('pk', 'place_id', 'name', 'type', 'color')
    readonly_fields = ('pk', 'place', 'name', 'color',
                       'date_created', 'factor')
    fields = ('pk', 'name', 'place', 'type',
              ('status', 'color'), 'date_created', 'factor')
    list_filter = ('type', 'status', 'date_created')
    search_fields = ('place__pk', 'place__place__name', 'effective_factor')

    def has_add_permission(self, request):
        return False

    def place_id(self, obj):
        return obj.place.pk

    def place(self, obj):
        return obj.place.place

    def name(self, obj):
        return obj.place.place.name

    def color(self, obj):
        const = 'color: white; padding: 1px 3px; width: 30px; border-radius: 10px; text-align: center; margin: 0px; font-size: 11px;"'
        style = f'style="background-color: rgb({"220,20,60" if obj.status == REDPLACE else "60,179,113"}); {const}'
        return format_html(f'<p {style}>{"R" if obj.status == REDPLACE else "W"}</p>')

    def factor(self, obj):
        if obj.effective_factor:
            user = GeneralUser.objects.get(pk=obj.effective_factor).user
            return f'name: {user.first_name} {user.last_name}\n' + \
                f'username: {user.username}\n' + \
                f'email: {user.email}\n' + \
                f'national code: {user.national_code}'
        return obj.effective_factor


@admin.register(MeetPlace)
class MeetPlaceAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('pk', 'place_id', 'name',
                    'first_name', 'last_name', 'email')
    readonly_fields = ('pk', 'place', 'general_user', 'name', 'date_created')
    fields = ('pk', 'name', 'place', 'general_user', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('place__pk', 'place__place__name', 'user__user__email')

    def has_add_permission(self, request):
        return False

    def place_id(self, obj):
        return obj.place.pk

    def name(self, obj):
        return obj.place.place.name

    def first_name(self, obj):
        return obj.user.user.first_name

    def last_name(self, obj):
        return obj.user.user.last_name

    def email(self, obj):
        return obj.user.user.email

    def general_user(self, obj):
        user = obj.user.user
        return f'name: {user.first_name} {user.last_name}\n' + \
            f'username: {user.username}\n' + \
            f'email: {user.email}\n' + \
            f'national code: {user.national_code}'

    def place(self, obj):
        return obj.place
