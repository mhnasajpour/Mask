from django.urls import path, include
from dj_rest_auth import views
from dj_rest_auth.registration import views as reg_views
from .views import CustomUserDetailsView

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user/', CustomUserDetailsView.as_view(), name='user'),
    path('password/reset/',
         views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<slug:uidb64>/<slug:token>/',
         views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/change/',
         views.PasswordChangeView.as_view(), name='password_change'),

    path('registration/account-confirm-email/<str:key>/',
         reg_views.ConfirmEmailView.as_view(), name='account-confirm-email'),
    path('registration/',
         include('dj_rest_auth.registration.urls'), name='registration'),
    path('account-confirm-email/',
         reg_views.VerifyEmailView.as_view(), name='account-confirm-email'),
]
