from rest_framework.views import APIView
from general_user.permissions import IsGeneralUser, IsQualified, IsPublicPlace
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChangePlaceStatusSerializer, MinorPlaceDetailsSerializer, ListCreateMeetPlaceSerializer
from .models import PublicPlace, PlaceStatus, MeetPlace
from datetime import datetime, timedelta
from config.settings import WHITEPLACE, REDPLACE
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView
from django.db import transaction
from general_user.models import UserStatus


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
    queryset = PublicPlace.objects.filter(~Q(name=''))


class ChangePlaceStatusView(APIView):
    permission_classes = [IsQualified, IsPublicPlace]
    serializer_class = ChangePlaceStatusSerializer

    def get(self, request):
        serializer = ChangePlaceStatusSerializer(request.user.publicplace)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChangePlaceStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        place_status = PlaceStatus()
        place_status.type = 2 if serializer.data.get(
            'status') == WHITEPLACE else 4
        place_status.place = request.user.publicplace
        place_status.status = serializer.data.get('status')
        place_status.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class MeetPlaceStatisticsView(APIView):
    permission_classes = [IsQualified, IsPublicPlace]

    def get(self, request, day):
        codes = [0] * 6
        meetings = request.user.publicplace.meetplace_set \
            .filter(date_created__gt=datetime.now()-timedelta(days=day))

        for meet in meetings:
            codes[meet.status_user] += 1
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
        place_target = PublicPlace.objects.get(pk=serializer.data['place'])
        user_target = request.user.generaluser

        meetings = [obj.place for obj in self.get_queryset()]
        if place_target in meetings:
            return Response({'message': 'You have already saved this appointment.'}, status=status.HTTP_200_OK)

        with transaction.atomic():
            meet_place = MeetPlace()
            meet_place.user = user_target
            meet_place.place = place_target
            meet_place.save()

            status_user = user_target.status
            status_place = place_target.status
            if status_place == REDPLACE and status_user <= 2:
                UserStatus.objects.create(
                    type=3, user=user_target, status=2, effective_factor=place_target.pk)

            elif status_place == WHITEPLACE and status_user == 4:
                PlaceStatus.objects.create(
                    type=1, place=place_target, status=REDPLACE, effective_factor=user_target.pk)

            return Response({'status': request.user.generaluser.status}, status=status.HTTP_201_CREATED)
