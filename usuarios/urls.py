from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, UserLogoutView, 
    UserProfileView, UpdateUserProfileView, PasswordChangeView, 
    check_email_availability, PasswordResetRequestView,
    PasswordResetVerifyView, PasswordResetConfirmView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UpdateUserProfileView.as_view(), name='user-profile-update'),
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
    path('check-email/', check_email_availability, name='check_email_availability'),
    
    # Nuevas URLs para reseteo de contraseña
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/verify/', PasswordResetVerifyView.as_view(), name='password-reset-verify'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
] 