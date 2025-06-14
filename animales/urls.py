from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimalViewSet, DecisionViewSet

router = DefaultRouter()
router.register(r'animales', AnimalViewSet, basename='animal')
router.register(r'decisiones', DecisionViewSet, basename='decision')

urlpatterns = [
    path('', include(router.urls)),
] 