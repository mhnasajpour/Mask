from rest_framework import serializers
from .models import PublicPlace, PLACE_STATUS_CHOICES
from general_user.serializers import UserDetailsSerializer


class PublicPlaceSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()

    class Meta:
        model = PublicPlace
        fields = ('user', 'status', 'name', 'location', 'region')


class PlaceStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=PLACE_STATUS_CHOICES)
