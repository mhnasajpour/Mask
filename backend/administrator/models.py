from django.db import models
from general_user.models import User


class Administrator(User):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
