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
from django.urls import path
from usuarios.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/', api_documentation, name='api-docs'),
    
    # Endpoints de autenticación
    path('api/register/user/', UserRegistrationView.as_view(), name='user-register'),
    path('api/register/company/', CompanyRegistrationView.as_view(), name='company-register'),
    path('api/login/', login_view, name='login'),
    path('api/logout/', logout_view, name='logout'),
    path('api/profile/', user_profile, name='user-profile'),
    
    # Testing endpoints
    path('registro-prueba/', registro_prueba, name='registro-prueba'),
    path('login-prueba/', login_prueba, name='login-prueba'),
]
