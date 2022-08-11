from django.urls import path
from .views import ChangePlaceStatusView

urlpatterns = [
    path('status/', ChangePlaceStatusView.as_view()),
]
