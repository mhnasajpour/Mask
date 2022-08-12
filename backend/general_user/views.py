from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import GeneralUserSerializer, RecordLatestHealthStatusSerializer, ListUserStatusSerializer
from public_place.serializers import PublicPlaceSerializer
from rest_framework.views import APIView
from .permissions import IsQualified, IsGeneralUser
from rest_framework.response import Response
from rest_framework import status
from .models import UserStatus
from datetime import datetime, timedelta


class UserDetailsView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if hasattr(self.request.user, 'generaluser'):
            return GeneralUserSerializer
        if hasattr(self.request.user, 'publicplace'):
            return PublicPlaceSerializer

    def get_object(self):
        if hasattr(self.request.user, 'generaluser'):
            return self.request.user.generaluser
        if hasattr(self.request.user, 'publicplace'):
            return self.request.user.publicplace


class RecordLatestHealthStatusView(APIView):
    permission_classes = [IsQualified, IsGeneralUser]
    serializer_class = RecordLatestHealthStatusSerializer

    def post(self, request):
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

        if request.user.generaluser.status <= health_status:
            UserStatus.objects.create(
                user=request.user.generaluser, status=health_status)

        return Response({'status': request.user.generaluser.status}, status=status.HTTP_200_OK)


class ListUserStatusView(ListAPIView):
    permission_classes = [IsQualified, IsGeneralUser]
    serializer_class = ListUserStatusSerializer

    def get_queryset(self):
        return self.request.user.generaluser.userstatus_set \
            .filter(date_created__gt=datetime.now()-timedelta(days=self.kwargs['day'])) \
            .distinct('date_created__date', 'status')[::-1]
