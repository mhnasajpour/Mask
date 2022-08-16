from rest_framework import serializers
from .models import PublicPlace, MeetPlace, WHITEPLACE, PLACE_STATUS_CHOICES
from datetime import timedelta


class ChangePlaceStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=PLACE_STATUS_CHOICES)


class MinorPlaceDetailsSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = PublicPlace
        fields = ('pk', 'email', 'name', 'location', 'region')


class ListCreateMeetPlaceSerializer(serializers.ModelSerializer):
    status_user = serializers.SerializerMethodField(read_only=True)
    status_place = serializers.SerializerMethodField(read_only=True)
    date = serializers.DateTimeField(
        source='date_created', format='%Y-%m-%d', read_only=True)

    class Meta:
        model = MeetPlace
        fields = ('place', 'status_user', 'status_place', 'date')

    def get_status_user(self, obj):
        try:
            return obj.user.userstatus_set \
                .filter(date_created__gte=obj.date_created,
                        date_created__lte=obj.date_created + timedelta(days=7)) \
                .last().status
        except:
            return 1

    def get_status_place(self, obj):
        try:
            return obj.place.placestatus_set \
                .filter(date_created__gte=obj.date_created,
                        date_created__lte=obj.date_created + timedelta(days=7)) \
                .last().status
        except:
            return WHITEPLACE
