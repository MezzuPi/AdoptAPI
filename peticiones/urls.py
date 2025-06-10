from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PeticionViewSet

router = DefaultRouter()
router.register(r'peticiones', PeticionViewSet, basename='peticion')

urlpatterns = [
    path('', include(router.urls)),
] 