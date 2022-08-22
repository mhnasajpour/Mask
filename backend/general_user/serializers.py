from rest_framework import serializers
from public_place.models import Place, BusinessOwner
from .models import GeneralUser, UserStatus, MeetPeople
from datetime import timedelta
from public_place.serializers import MinorPlaceDetailsSerializer


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
        if len(phone_number) == 11 and phone_number[:2] == '09' and phone_number.isnumeric():
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


class BusinessOwnerSerializer(AbstractUserDetailsSerializer):
    name = serializers.CharField(source='place.name', max_length=150)
    city = serializers.CharField(source='place.city', max_length=150)
    zip_code = serializers.CharField(source='place.zip_code', max_length=10)
    address = serializers.CharField(source='place.address', max_length=500)

    latitude = serializers.FloatField(source='place.latitude')
    longitude = serializers.FloatField(source='place.longitude')

    class Meta:
        model = BusinessOwner
        fields = ('pk', 'type', 'is_staff', 'status', 'first_name', 'last_name', 'username', 'email',
                  'national_code', 'phone_number', 'name', 'city', 'zip_code', 'address', 'latitude', 'longitude')

    def validate_zip_code(self, zip_code):
        if len(zip_code) == 10 and zip_code.isnumeric():
            if Place.objects.filter(zip_code=zip_code):
                raise serializers.ValidationError(
                    'Place with this Zip code already exists.')
            return zip_code
        raise serializers.ValidationError('Zip code is invalid.')

    def update(self, instance, data):
        self.update_user(instance=instance.user, data=data['user'])
        place = instance.place
        data = data['place']
        place.name = data.get('name', data['name'])
        place.city = data.get('city', data['city'])
        place.zip_code = data.get('zip_code', data['zip_code'])
        place.address = data.get('address', data['address'])
        place.longitude = data.get('longitude', data['longitude'])
        place.latitude = data.get('latitude', data['latitude'])
        instance.place.save()
        return instance


class RecordLatestHealthStatusSerializer(serializers.Serializer):
    cough = serializers.BooleanField(default=False)
    fever = serializers.BooleanField(default=False)
    asthma = serializers.BooleanField(default=False)
    pain = serializers.BooleanField(default=False)
    sore_throat = serializers.BooleanField(default=False)


class MinorUserDetailsSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = GeneralUser
        fields = ('first_name', 'last_name', 'email')


class ListUserStatusSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        source='date_created', read_only=True, format='%Y-%m-%d')
    factor = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserStatus
        fields = ('type', 'factor', 'status', 'date')

    def get_factor(self, obj):
        if obj.type == 1:
            return 'Test'
        if obj.type == 2:
            return MinorUserDetailsSerializer(GeneralUser.objects.get(pk=obj.effective_factor)).data
        if obj.type == 3:
            return MinorPlaceDetailsSerializer(BusinessOwner.objects.get(pk=obj.effective_factor)).data
        if obj.type == 4:
            return 'Got better'
        if obj.status == 5:
            return 'Dead'


class ListCreateMeetPeopleserializers(serializers.ModelSerializer):
    user_1 = MinorUserDetailsSerializer(read_only=True, source='user1')
    user_2 = MinorUserDetailsSerializer(read_only=True, source='user2')
    status_user1 = serializers.SerializerMethodField(read_only=True)
    status_user2 = serializers.SerializerMethodField(read_only=True)
    date = serializers.DateTimeField(
        source='date_created', format='%Y-%m-%d', read_only=True)

    email = serializers.EmailField(required=False)

    class Meta:
        model = MeetPeople
        fields = ('email', 'user_1', 'user_2',
                  'status_user1', 'status_user2', 'date')

    def get_status_user1(self, obj):
        try:
            return obj.user1.userstatus_set \
                .filter(date_created__gte=obj.date_created,
                        date_created__lte=obj.date_created + timedelta(days=7)) \
                .last().status
        except:
            return 1

    def get_status_user2(self, obj):
        try:
            return obj.user2.userstatus_set \
                .filter(date_created__gte=obj.date_created,
                        date_created__lte=obj.date_created + timedelta(days=7)) \
                .last().status
        except:
            return 1

    def validate_email(self, email):
        if GeneralUser.objects.filter(user__email=email).exists():
            return email
        raise serializers.ValidationError('There is no user with this email.')


class ListUserSerializer(MinorUserDetailsSerializer):
    national_code = serializers.ReadOnlyField(source='user.national_code')
    date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GeneralUser
        fields = ('pk', 'first_name', 'last_name',
                  'national_code', 'email', 'status', 'date')

    def get_date(self, obj):
        try:
            return obj.userstatus_set.last().date_created.date()
        except:
            pass


class ControlPatientsSerializer(ListUserSerializer):
    STATUS_CHOICES = (
        (2, 'Got better'),
        (5, 'Pass away')
    )
    status = serializers.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = GeneralUser
        fields = ('pk', 'first_name', 'last_name',
                  'national_code', 'email', 'date', 'status')
