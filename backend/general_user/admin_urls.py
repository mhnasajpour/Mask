from django.urls import path
from .views import ListUserView, ControlPatientsView

urlpatterns = [
    path('users/', ListUserView.as_view(), name='users_status'),
    path('patient/<int:pk>', ControlPatientsView.as_view(), name='patient')
]
