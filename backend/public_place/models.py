from django.db import models
from general_user.models import User, GeneralUser
from config.settings import WHITEPLACE, REDPLACE
import uuid


PLACE_STATUS_CHOICES = (
    (WHITEPLACE, 'White'),
    (REDPLACE, 'Red'),
)


class PublicPlace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    region = models.PositiveSmallIntegerField(null=True)
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
    place = models.ForeignKey(PublicPlace, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=PLACE_STATUS_CHOICES)
    effective_factor = models.CharField(max_length=50, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class MeetPlace(models.Model):
    user = models.ForeignKey(GeneralUser, on_delete=models.SET_NULL, null=True)
    place = models.ForeignKey(
        PublicPlace, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
