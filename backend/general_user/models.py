from django.db import models
from django.contrib.auth.models import AbstractUser
from config.settings import GENERAL_USER, BUSINESS_USER


USER_STATUS_CHOICES = (
    (1, 'Healthy'),
    (2, 'Doubtful'),
    (3, 'Perilous'),
    (4, 'Patient'),
    (5, 'Dead')
)


BLOOD_TYPE_CHOICES = (
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('O+', 'O+'), ('O-', 'O-'),
    ('AB+', 'AB+'), ('AB-', 'AB-')
)


class User(AbstractUser):
    national_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=11, blank=True)

    @property
    def type(self):
        if hasattr(self, 'generaluser'):
            return GENERAL_USER
        if hasattr(self, 'businessowner'):
            return BUSINESS_USER


class GeneralUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    blood_type = models.CharField(
        max_length=3, choices=BLOOD_TYPE_CHOICES, null=True)
    height = models.PositiveSmallIntegerField(null=True)
    weight = models.PositiveSmallIntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def status(self):
        try:
            return self.userstatus_set.last().status
        except AttributeError:
            return 1


class UserStatus(models.Model):
    TYPE_CHOICES = (
        (1, 'Test'),
        (2, 'Person'),
        (3, 'Place'),
        (4, 'Got better')
    )

    type = models.IntegerField(choices=TYPE_CHOICES)
    user = models.ForeignKey(GeneralUser, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=USER_STATUS_CHOICES)
    effective_factor = models.CharField(max_length=50, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class MeetPeople(models.Model):
    user1 = models.ForeignKey(
        GeneralUser, on_delete=models.SET_NULL, related_name='meet_people1', null=True)
    user2 = models.ForeignKey(
        GeneralUser, on_delete=models.SET_NULL, related_name='meet_people2', null=True)
    date_created = models.DateTimeField(auto_now_add=True)
