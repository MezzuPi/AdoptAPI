from django.urls import path
from .views import ContactFormView

urlpatterns = [
    path('empresa/', ContactFormView.as_view(), name='contacto-empresa'),
] 