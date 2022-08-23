from django.urls import path
from .views import (ChangePlaceStatusView,
                    MeetPlaceStatisticsView,
                    MinorPlaceDetailsView,
                    ListCreateMeetPlaceView)

urlpatterns = [
    path('', MinorPlaceDetailsView.as_view(), name='place'),
    path('status/', ChangePlaceStatusView.as_view(), name='change_status'),
    path('statistics/<int:day>/',
         MeetPlaceStatisticsView.as_view(), name='meet_statistics'),
    path('meet/', ListCreateMeetPlaceView.as_view(), name='meet_place'),
]
