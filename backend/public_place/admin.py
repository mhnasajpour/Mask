import imp
from django import forms
from django.contrib import admin
from .models import Place, BusinessOwner, PlaceStatus, MeetPlace, WHITEPLACE, REDPLACE
from django_reverse_admin import ReverseModelAdmin


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
