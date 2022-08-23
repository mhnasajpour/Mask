import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from config.settings import WHITEPLACE, REDPLACE
from general_user.models import User, GeneralUser


PLACE_STATUS_CHOICES = (
    (WHITEPLACE, 'White'),
    (REDPLACE, 'Red'),
)


class Place(models.Model):
    name = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    address = models.TextField(max_length=500, blank=True)

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    @property
    def map(self):
        return format_html(f'<iframe src="https://maps.google.com/maps?q={self.latitude},{self.longitude}&hl=en&z=16&amp;output=embed" width="483" height="300"></iframe>')

    def clean(self):
        if len(self.zip_code) != 10 or not self.zip_code.isnumeric():
            raise ValidationError('Zip code is invalid.')
        if Place.objects.filter(zip_code=self.zip_code).exists():
            raise ValidationError('Place with this Zip code already exists.')


class BusinessOwner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, models.CASCADE)
    place = models.OneToOneField(Place, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def status(self):
        try:
            return self.placestatus_set.last().status
        except AttributeError:
            return WHITEPLACE


class PlaceStatus(models.Model):
    TYPE_CHOICES = (
        (1, 'Meet'),
        (2, 'Disinfect'),
        (3, 'Passing time'),
        (4, 'Manually turned red')
    )

    type = models.IntegerField(choices=TYPE_CHOICES)
    place = models.ForeignKey(BusinessOwner, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=PLACE_STATUS_CHOICES)
    effective_factor = models.CharField(max_length=50, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class MeetPlace(models.Model):
    user = models.ForeignKey(GeneralUser, on_delete=models.SET_NULL, null=True)
    place = models.ForeignKey(
        BusinessOwner, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
