from django.urls import path
from .views import UserDetailsView, RecordLatestHealthStatusView

urlpatterns = [
    path('', UserDetailsView.as_view(), name='user'),
    path('test/', RecordLatestHealthStatusView.as_view(), name='test'),
]
