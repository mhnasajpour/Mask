from rest_framework import serializers
from .models import GeneralUser


class AbstractUserDetailsSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='user.type', read_only=True)
    is_staff = serializers.BooleanField(source='user.is_staff', read_only=True)
    first_name = serializers.CharField(
        source='user.first_name', required=True, max_length=150)
    last_name = serializers.CharField(
        source='user.last_name', required=True, max_length=150)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    national_code = serializers.CharField(
        source='user.national_code', read_only=True)
    phone_number = serializers.CharField(
        source='user.phone_number', required=False)

    def update_user(self, instance, data):
        instance.first_name = data.get('first_name', instance.first_name)
        instance.last_name = data.get('last_name', instance.last_name)
        instance.national_code = data.get(
            'national_code', instance.national_code)
        instance.phone_number = data.get('phone_number', instance.phone_number)
        instance.save()
        return instance

    def validate_phone_number(self, phone_number):
        if len(phone_number) == 11 and phone_number[:2] == '09':
            return phone_number
        raise serializers.ValidationError('Phone number is invalid.')


class GeneralUserSerializer(AbstractUserDetailsSerializer):
    class Meta:
        model = GeneralUser
        fields = ('pk', 'type', 'is_staff', 'status', 'first_name', 'last_name', 'username', 'email',
                  'national_code', 'phone_number', 'birth_date', 'blood_type', 'height', 'weight')

    def update(self, instance, data):
        self.update_user(instance=instance.user, data=data['user'])
        instance.birth_date = data.get('birth_date', instance.birth_date)
        instance.blood_type = data.get('blood_type', instance.blood_type)
        instance.height = data.get('height', instance.height)
        instance.weight = data.get('weight', instance.weight)
        instance.save()
        return instance


class RecordLatestHealthStatusSerializer(serializers.Serializer):
    cough = serializers.BooleanField(default=False)
    fever = serializers.BooleanField(default=False)
    asthma = serializers.BooleanField(default=False)
    pain = serializers.BooleanField(default=False)
    sore_throat = serializers.BooleanField(default=False)
