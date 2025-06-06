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
from usuarios.views import api_documentation # Keep if still used

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), # For browsable API login/logout

    # API Documentation
    path('api/docs/', api_documentation, name='api-docs'), # Updated path for API documentation

    # New Authentication Endpoints using include
    path('api/auth/', include('usuarios.urls')), # This will prefix all urls in usuarios.urls with api/auth/

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
