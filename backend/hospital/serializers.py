from rest_framework import serializers
from .models import Hospital


class HospitalSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)
    city = serializers.CharField(max_length=150)
    zip_code = serializers.CharField(max_length=10)
    address = serializers.CharField(max_length=500)
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

    class Meta:
        model = Hospital
        fields = ('name', 'city', 'zip_code',
                  'address', 'latitude', 'longitude')

    def validate_zip_code(self, zip_code):
        if len(zip_code) == 10 and zip_code.isnumeric():
            return zip_code
        raise serializers.ValidationError('Zip code is invalid.')
