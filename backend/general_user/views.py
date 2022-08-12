from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import GeneralUserSerializer
from public_place.serializers import PublicPlaceSerializer


class UserDetailsView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if hasattr(self.request.user, 'generaluser'):
            return GeneralUserSerializer
        if hasattr(self.request.user, 'publicplace'):
            return PublicPlaceSerializer

    def get_object(self):
        if hasattr(self.request.user, 'generaluser'):
            return self.request.user.generaluser
        if hasattr(self.request.user, 'publicplace'):
            return self.request.user.publicplace
