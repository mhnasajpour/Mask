from django.urls import path
from .views import ChangePlaceStatusView, ListMeetPlaceView

urlpatterns = [
    path('status/', ChangePlaceStatusView.as_view()),
    path('statistics/<int:day>', ListMeetPlaceView.as_view()),
]
