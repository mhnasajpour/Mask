from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from general_user.permissions import IsAdminOrReadOnly
from .serializers import HospitalSerializer
from .models import Hospital


class ListCreateHospitalView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()


class RetrieveUpdateDestroyHospitalView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()
