from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, PasswordResetSerializer
from general_user.models import User, GeneralUser
from public_place.models import BusinessOwner
from config.settings import GENERAL_USER, BUSINESS_USER
from django.contrib.auth import get_user_model
import re


class CustomRegisterSerializer(RegisterSerializer):
    TYPE_CHOICES = (
        (GENERAL_USER, 'General user'),
        (BUSINESS_USER, 'Business user')
    )

    type = serializers.ChoiceField(choices=TYPE_CHOICES)
    national_code = serializers.CharField()

    def validate(self, data):
        national_code = data['national_code']
        if not re.search(r'^\d{10}$', national_code):
            raise serializers.ValidationError('National code is invalid.')
        check = int(national_code[9])
        s = sum(int(national_code[x]) * (10 - x)
                for x in range(9)) % 11
        if (check == s if s < 2 else check + s == 11):
            if data['type'] == GENERAL_USER and GeneralUser.objects.filter(user__national_code=national_code):
                raise serializers.ValidationError(
                    'A user with that national code already exists.')
            return data
        raise serializers.ValidationError('National code is invalid.')

    def save(self, request):
        user = super().save(request)
        user.national_code = self.validated_data.get('national_code')
        if self.validated_data.get('type') == GENERAL_USER:
            GeneralUser.objects.create(user=user)
        elif self.validated_data.get('type') == BUSINESS_USER:
            BusinessOwner.objects.create(user=user)
        user.save()
        return user


class CustomLoginSerializer(LoginSerializer):
    email = None


class CustomPasswordResetSerializer(PasswordResetSerializer):
    username = serializers.CharField(max_length=127)
    national_code = serializers.CharField(max_length=10)

    def validate(self, data):
        if User.objects.filter(email=data.get('email'),
                               username=data.get('username'),
                               national_code=data.get('national_code')):
            return data
        raise serializers.ValidationError(
            'There is no user with this information.')


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('pk', 'type', 'is_staff', 'first_name', 'last_name',
                  'username', 'email', 'national_code', 'phone_number')
        read_only_fields = fields
