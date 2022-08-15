from rest_framework import serializers
from .models import PublicPlace, PLACE_STATUS_CHOICES
from general_user.serializers import AbstractUserDetailsSerializer


class PublicPlaceSerializer(AbstractUserDetailsSerializer):
    name = serializers.CharField(max_length=255, required=True)
    location = serializers.CharField(max_length=255, required=True)
    region = serializers.IntegerField(min_value=0, required=True)

    class Meta:
        model = PublicPlace
        fields = ('pk', 'type', 'is_staff', 'status', 'first_name', 'last_name', 'username', 'email',
                  'national_code', 'phone_number', 'name', 'location', 'region')

    def update(self, instance, data):
        self.update_user(instance=instance.user, data=data['user'])
        instance.name = data.get('name', instance.name)
        instance.location = data.get('location', instance.location)
        instance.region = data.get('region', instance.region)
        instance.save()
        return instance


class ChangePlaceStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=PLACE_STATUS_CHOICES)


class MinorPlaceDetailsSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = PublicPlace
        fields = ('pk', 'status', 'email', 'name', 'location', 'region')
