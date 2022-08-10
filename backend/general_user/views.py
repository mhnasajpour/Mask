from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserDetailsSerializer, GeneralUserSerializer, PublicPlaceSerializer


class CustomUserDetailsView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if hasattr(self.request.user, 'generaluser'):
            return GeneralUserSerializer
        if hasattr(self.request.user, 'publicplace'):
            return PublicPlaceSerializer
        if hasattr(self.request.user, 'administrator'):
            return UserDetailsSerializer

    def get_object(self):
        if hasattr(self.request.user, 'generaluser'):
            return self.request.user.generaluser
        if hasattr(self.request.user, 'publicplace'):
            return self.request.user.publicplace
        if hasattr(self.request.user, 'administrator'):
            return self.request.user
