from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Hospital
from .serializers import HospitalSerializer
from general_user.permissions import IsAdminOrReadOnly


class ListCreateHospitalView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = HospitalSerializer

    def get_queryset(self):
        city = self.request.GET.get('city')
        if city:
            queryset = Hospital.objects.filter(city=city)
        else:
            queryset = Hospital.objects.all()

        latitude = self.request.GET.get('lat')
        longitude = self.request.GET.get('lon')
        if latitude and longitude:
            queryset = list(queryset)
            queryset.sort(
                key=lambda x: (x.latitude-float(latitude))**2 + (x.longitude-float(longitude))**2)
        return queryset


class RetrieveUpdateDestroyHospitalView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()
    lookup_field = 'zip_code'
