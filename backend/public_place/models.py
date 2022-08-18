from django.db import models
from general_user.models import User, GeneralUser
from config.settings import WHITEPLACE, REDPLACE
import uuid
from django.core.exceptions import ValidationError


PLACE_STATUS_CHOICES = (
    (WHITEPLACE, 'White'),
    (REDPLACE, 'Red'),
)


class Place(models.Model):
    name = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    zip_code = models.CharField(unique=True, max_length=10, blank=True)
    address = models.TextField(max_length=500, blank=True)

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def clean(self):
        if len(self.zip_code) != 10 or not self.zip_code.isnumeric():
            raise ValidationError('Zip code is invalid.')


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
