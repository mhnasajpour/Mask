from pyexpat import model
from rest_framework.serializers import ModelSerializer
from .models import Hospital


class HospitalSerializer(ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('pk', 'name', 'location', 'region', 'address')
        read_only_fields = ('pk',)
