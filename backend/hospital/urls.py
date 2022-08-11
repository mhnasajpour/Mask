from django.urls import path
from .views import ListCreateHospitalView, RetrieveUpdateDestroyHospitalView

urlpatterns = [
    path('', ListCreateHospitalView.as_view()),
    path('<int:pk>', RetrieveUpdateDestroyHospitalView.as_view()),
]
