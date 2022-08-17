from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from general_user.permissions import IsAdminOrReadOnly
from .serializers import HospitalSerializer
from .models import Hospital


class ListCreateHospitalView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = HospitalSerializer

    def get_queryset(self):
        city = self.request.GET.get('city')
        if city:
            queryset = Hospital.objects.filter(city=city)
        else:
            queryset = Hospital.objects.all()

        latitude = float(self.request.GET.get('lat'))
        longitude = float(self.request.GET.get('lon'))
        if latitude and longitude:
            queryset = list(queryset)
            queryset.sort(
                key=lambda x: (x.latitude-latitude)**2 + (x.longitude-longitude)**2)
        return queryset


class RetrieveUpdateDestroyHospitalView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()
    lookup_field = 'zip_code'
