from django.urls import path
from .views import ListCreateHospitalView, RetrieveUpdateDestroyHospitalView

urlpatterns = [
    path('', ListCreateHospitalView.as_view()),
    path('<int:zip_code>', RetrieveUpdateDestroyHospitalView.as_view()),
]
