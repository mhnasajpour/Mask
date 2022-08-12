from django.urls import path
from .views import UserDetailsView

urlpatterns = [
    path('', UserDetailsView.as_view(), name='user'),
]
