from django.urls import path
from .views import UserDetailsView, RecordLatestHealthStatusView, ListUserStatusView, ListCreateMeetPeopleView

urlpatterns = [
    path('', UserDetailsView.as_view(), name='user'),
    path('test/', RecordLatestHealthStatusView.as_view(), name='test'),
    path('status/<int:day>/', ListUserStatusView.as_view(), name='status'),
    path('meet/person/', ListCreateMeetPeopleView.as_view(), name='meet_person'),
]
