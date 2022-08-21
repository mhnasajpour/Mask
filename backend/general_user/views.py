from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import GeneralUserSerializer, BusinessOwnerSerializer, RecordLatestHealthStatusSerializer, ListUserStatusSerializer, ListCreateMeetPeopleserializers, MinorUserDetailsSerializer, ListUserSerializer, ControlPatientsSerializer
from rest_framework.views import APIView
from .permissions import IsQualified, IsGeneralUser
from rest_framework.response import Response
from rest_framework import status
from .models import GeneralUser, UserStatus, MeetPeople
from datetime import datetime, timedelta
from django.db.models import Q
from public_place.views import meetings_place
from django.db import transaction
from django.shortcuts import get_object_or_404


def update_status(user):
    user_status = user.userstatus_set.last()
    level = (datetime.now().date() - user_status.date_created.date()).days // 7

    if 1 < user_status.status < 4 and level:
        new_status = user_status.status-level
        UserStatus.objects.create(
            type=4, user=user, status=new_status if new_status > 0 else 1)


def meetings_people(user):
    update_status(user)

    if user.status == 4:
        meetings_place(user)

    if user.status > 2:
        persons1 = list(user.meet_people1
                        .filter(date_created__gt=datetime.now()-timedelta(days=7))
                        .values_list('user2', flat=True))

        persons2 = list(user.meet_people2
                        .filter(date_created__gt=datetime.now()-timedelta(days=7))
                        .values_list('user1', flat=True))

        for person in persons1 + persons2:
            if GeneralUser.objects.get(pk=person).status < user.status:
                UserStatus.objects.create(
                    type=2, user_id=person, effective_factor=user.pk, status=user.status-1)
                meetings_people(GeneralUser.objects.get(pk=person))


class UserDetailsView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if hasattr(self.request.user, 'generaluser'):
            return GeneralUserSerializer
        if hasattr(self.request.user, 'businessowner'):
            return BusinessOwnerSerializer

    def get_object(self):
        if hasattr(self.request.user, 'generaluser'):
            return self.request.user.generaluser
        if hasattr(self.request.user, 'businessowner'):
            return self.request.user.businessowner


class MinorPlaceDetailsView(ListAPIView):
    serializer_class = MinorUserDetailsSerializer
    queryset = GeneralUser.objects.filter(
        ~Q(user__first_name='') | ~Q(user__last_name=''))


class RecordLatestHealthStatusView(APIView):
    permission_classes = [IsQualified, IsGeneralUser]
    serializer_class = RecordLatestHealthStatusSerializer

    def post(self, request):
        last_status = request.user.generaluser.userstatus_set \
            .filter(type=1).last()
        if last_status and not datetime.now().date() - last_status.date_created.date():
            return Response({'message': 'You can only test once a day.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = RecordLatestHealthStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        grade = (serializer.data['cough'] * 30) + \
                (serializer.data['fever'] * 20) + \
                (serializer.data['asthma'] * 20) + \
                (serializer.data['pain'] * 15) + \
                (serializer.data['sore_throat'] * 15)

        if grade >= 75:
            health_status = 4
        elif grade >= 50:
            health_status = 3
        elif grade >= 15:
            health_status = 2
        else:
            health_status = 1

        with transaction.atomic():
            if request.user.generaluser.status <= health_status:
                UserStatus.objects.create(
                    type=1, user=request.user.generaluser, status=health_status)
                meetings_people(request.user.generaluser)
                return Response({'status': request.user.generaluser.status}, status=status.HTTP_201_CREATED)

        return Response({'status': request.user.generaluser.status}, status=status.HTTP_200_OK)


class ListUserStatusView(ListAPIView):
    permission_classes = [IsQualified, IsGeneralUser]
    serializer_class = ListUserStatusSerializer

    def get_queryset(self):
        return self.request.user.generaluser.userstatus_set \
            .filter(date_created__gt=datetime.now()-timedelta(days=self.kwargs['day']))[::-1]


class ListCreateMeetPeopleView(ListCreateAPIView):
    permission_classes = [IsQualified, IsGeneralUser]
    serializer_class = ListCreateMeetPeopleserializers

    def get_queryset(self):
        user = self.request.user.generaluser
        return MeetPeople.objects.filter(Q(user1=user) | Q(user2=user)).filter(
            date_created__gt=datetime.now()-timedelta(days=int(self.request.GET.get('day', 1))))[::-1]

    def post(self, request):
        serializer = ListCreateMeetPeopleserializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_target = GeneralUser.objects.get(user=serializer.data['user'])

        queryset = self.get_queryset()
        if queryset:
            meetings = [(obj.user1, obj.user2) for obj in queryset]
            if (request.user.generaluser, user_target) in meetings:
                return Response({'message': 'You have already saved this appointment.'}, status=status.HTTP_200_OK)
            if (user_target, request.user.generaluser) in meetings:
                return Response({'message': 'This meeting has already been saved.'}, status=status.HTTP_200_OK)

        with transaction.atomic():
            meet_people = MeetPeople()
            meet_people.user1 = request.user.generaluser
            meet_people.user2 = user_target
            meet_people.save()

            status1 = request.user.generaluser.status
            status2 = user_target.status
            if (status1 > 2 or status2 > 2) and status1 != status2:
                if status1 > status2:
                    user = user_target
                    factor = request.user.generaluser.pk
                    new_status = status1 - 1
                else:
                    user = request.user.generaluser
                    factor = serializer.data['user']
                    new_status = status2 - 1

                UserStatus.objects.create(
                    type=2, user=user, effective_factor=factor, status=new_status)
                meetings_people(user)

            return Response({'status': request.user.generaluser.status}, status=status.HTTP_201_CREATED)


class StatisticsView(APIView):
    def get(self, request, day):
        meetings = UserStatus.objects.filter(
            date_created__gt=datetime.now()-timedelta(days=day), status__gt=2)

        codes = [0] * 3
        for meet in meetings:
            codes[meet.status-3] += 1
        return Response({'Perilous': codes[0], 'Patient': codes[1], 'Dead': codes[2]}, status=status.HTTP_200_OK)


class ListUserView(ListAPIView):
    permission_classes = [IsQualified, IsAdminUser]
    serializer_class = ListUserSerializer

    def get_queryset(self):
        status = self.request.GET.get('status')
        if not status:
            return GeneralUser.objects.all()
        return [obj for obj in GeneralUser.objects.all() if obj.status == int(status)]


class ControlPatientsView(RetrieveAPIView):
    permission_classes = [IsQualified, IsAdminUser]
    serializer_class = ControlPatientsSerializer

    def get_object(self):
        return get_object_or_404(GeneralUser, pk=self.kwargs['pk'])

    def put(self, request, pk):
        serializer = ControlPatientsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_status = UserStatus()
        user_status.type = 5 if serializer.data['status'] == 5 else 4
        user_status.user_id = pk
        user_status.status = serializer.data['status']
        user_status.save()

        return Response({'status': serializer.data['status']}, status=status.HTTP_201_CREATED)
