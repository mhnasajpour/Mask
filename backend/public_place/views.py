from rest_framework.views import APIView
from general_user.permissions import IsQualified, IsPublicPlace
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlaceStatusSerializer
from .models import PlaceStatus
from datetime import datetime, timedelta


class ChangePlaceStatusView(APIView):
    permission_classes = [IsQualified, IsPublicPlace]
    serializer_class = PlaceStatusSerializer

    def get(self, request):
        serializer = PlaceStatusSerializer(request.user.publicplace)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PlaceStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        place_status = PlaceStatus()
        place_status.place = request.user.publicplace
        place_status.status = serializer.data.get('status')
        place_status.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ListMeetPlaceView(APIView):
    permission_classes = [IsQualified, IsPublicPlace]

    def get(self, request, day):
        codes = [0] * 6
        meetings = request.user.publicplace.meetplace_set \
            .filter(date_created__gt=datetime.now()-timedelta(days=day)) \
            .distinct('user', 'status_user')
        for meet in meetings:
            codes[meet.status_user] += 1
        codes.pop(0)
        return Response({'statistics': codes})
