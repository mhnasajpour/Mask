from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from .models import BusinessOwner, PlaceStatus, MeetPlace
from .serializers import ChangePlaceStatusSerializer, MinorPlaceDetailsSerializer, ListCreateMeetPlaceSerializer
from config.settings import WHITEPLACE, REDPLACE
from general_user.models import GeneralUser, UserStatus
from general_user.permissions import IsGeneralUser, IsQualified, IsPublicPlace


def meetings_place(user):
    if user.status == 4:
        places = user.meetplace_set \
            .filter(date_created__gt=datetime.now()-timedelta(days=7)) \
            .values_list('place', flat=True)

        for place in places:
            PlaceStatus.objects.create(
                type=1, place=place, status=REDPLACE, effective_factor=user.pk)


class MinorPlaceDetailsView(ListAPIView):
    serializer_class = MinorPlaceDetailsSerializer
    queryset = BusinessOwner.objects.filter(~Q(place__name=''))


class ChangePlaceStatusView(APIView):
    permission_classes = [IsQualified, IsPublicPlace]
    serializer_class = ChangePlaceStatusSerializer

    def get(self, request):
        serializer = ChangePlaceStatusSerializer(request.user.businessowner)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChangePlaceStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        place_status = PlaceStatus()
        place_status.type = 2 if serializer.data \
            .get('status') == WHITEPLACE else 4
        place_status.place = request.user.businessowner
        place_status.status = serializer.data.get('status')
        place_status.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class MeetPlaceStatisticsView(APIView):
    permission_classes = [IsQualified, IsPublicPlace]

    def get(self, request, day):
        if day > 7:
            return Response({'error': 'Day should be lower than 7.'}, status=status.HTTP_400_BAD_REQUEST)

        codes = [0] * 6
        meetings = request.user.businessowner.meetplace_set \
            .filter(date_created__gt=datetime.now()-timedelta(days=day)).values_list('user', flat=True)
        users = GeneralUser.objects.filter(pk__in=meetings)

        for user in users:
            meet_status = user.userstatus_set \
                .filter(date_created__gte=datetime.now()-timedelta(days=int(day)+7)).last().status
            codes[meet_status] += 1
        codes.pop(0)
        return Response({'statistics': codes}, status=status.HTTP_200_OK)


class ListCreateMeetPlaceView(ListCreateAPIView):
    permission_classes = [IsQualified, IsGeneralUser]
    serializer_class = ListCreateMeetPlaceSerializer

    def get_queryset(self):
        return self.request.user.generaluser.meetplace_set \
            .filter(date_created__gt=datetime.now()-timedelta(days=int(self.request.GET.get('day', 1))))[::-1]

    def post(self, request):
        serializer = ListCreateMeetPlaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        place_target = BusinessOwner.objects.get(pk=serializer.data['place'])
        user_target = request.user.generaluser

        meetings = [obj.place for obj in self.get_queryset()]
        if place_target in meetings:
            return Response({'message': 'You have already saved this meeting.'}, status=status.HTTP_200_OK)

        with transaction.atomic():
            status_user = user_target.status
            status_place = place_target.status
            if status_place == REDPLACE and status_user <= 2:
                UserStatus.objects.create(
                    type=3, user=user_target, status=2, effective_factor=place_target.pk)

            elif status_place == WHITEPLACE and status_user == 4:
                PlaceStatus.objects.create(
                    type=1, place=place_target, status=REDPLACE, effective_factor=user_target.pk)

            meet_place = MeetPlace()
            meet_place.user = user_target
            meet_place.place = place_target
            meet_place.save()

            return Response({'status': request.user.generaluser.status}, status=status.HTTP_201_CREATED)
