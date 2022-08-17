from django.db import models
from public_place.models import Place


class Hospital(Place):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
