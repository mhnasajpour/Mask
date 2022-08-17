from rest_framework import serializers
from .models import Hospital


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('name', 'city', 'zip_code',
                  'address', 'longitude', 'latitude')

    def validate_zip_code(self, zip_code):
        if len(zip_code) == 10 and zip_code.isnumeric():
            return zip_code
        raise serializers.ValidationError('Zip code is invalid.')
