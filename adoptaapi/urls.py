"""
URL configuration for adoptaapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Remove old view imports if they are no longer directly used here
# from usuarios.views import UserRegistrationView, CompanyRegistrationView, login_view, logout_view, user_profile, api_documentation
from usuarios.views import UserRegistrationView, UserLoginView, api_documentation # Keep if still used
from rest_framework import routers
from animales.views import AnimalViewSet

router = routers.DefaultRouter()
router.register(r'animales', AnimalViewSet, basename='animales')
# No es necesario registrar UserRegistrationView, ya que es una vista concreta.
# router.register(r'usuarios', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('peticiones.urls')),

    # User management endpoints
    path('api/register/', UserRegistrationView.as_view(), name='user_register'),
    path('api/login/', UserLoginView.as_view(), name='user_login'),

    path('api-auth/', include('rest_framework.urls')), # For browsable API login/logout

    # API Documentation
    path('api/docs/', api_documentation, name='api-docs'),

    # New Authentication Endpoints using include
    path('api/auth/', include('usuarios.urls')), # This will prefix all urls in usuarios.urls with api/auth/

    # Password Reset Endpoints
    path('api/password_reset/', include('django.contrib.auth.urls')), # Adds Django's built-in password reset views

    # Endpoints de autenticación (Old ones - to be commented or removed if replaced)
    # path('api/register/user/', UserRegistrationView.as_view(), name='user-register'),
    # path('api/register/company/', CompanyRegistrationView.as_view(), name='company-register'),
    # path('api/login/', login_view, name='login'),
    # path('api/logout/', logout_view, name='logout'),
    # path('api/profile/', user_profile, name='user-profile'),

    # Animales endpoints
    path('api/', include('animales.urls')),

    # Testing endpoints (Keep if still needed)
    # path('registro-prueba/', registro_prueba, name='registro-prueba'),
    # path('login-prueba/', login_prueba, name='login-prueba'),
]
