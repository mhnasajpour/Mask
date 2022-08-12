from django.urls import path
from .views import ChangePlaceStatusView, MeetPlaceStatisticsView

urlpatterns = [
    path('status/', ChangePlaceStatusView.as_view()),
    path('statistics/<int:day>', MeetPlaceStatisticsView.as_view()),
]
