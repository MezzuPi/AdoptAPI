from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Animal
from .serializers import AnimalSerializer

# Create your views here.

class IsEmpresaUser(permissions.BasePermission):
    """
    Custom permission to only allow users of type 'EMPRESA' to create animals.
    """
    def has_permission(self, request, view):
        if request.method == 'POST': # Only check for POST requests (creation)
            return request.user and request.user.is_authenticated and request.user.tipo == 'EMPRESA'
        return True # Allow other methods (GET, PUT, DELETE) for authenticated users

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmpresaUser]

    def perform_create(self, serializer):
        # Automatically set the empresa to the logged-in user
        if self.request.user.is_authenticated and self.request.user.tipo == 'EMPRESA':
            serializer.save(empresa=self.request.user)
        else:
            # This case should ideally be caught by IsEmpresaUser permission
            # but as a fallback:
            return Response({"detail": "User must be an EMPRESA to create an animal."}, status=status.HTTP_403_FORBIDDEN)

    # You can add more custom actions or override other methods here if needed
    # For example, to list only animals created by the current empresa:
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_authenticated and user.tipo == 'EMPRESA':
    #         return Animal.objects.filter(empresa=user)
    #     elif user.is_authenticated and user.tipo == 'PARTICULAR': # Or is_staff for admin view all
    #         return Animal.objects.all() # Allow particulars to see all
    #     return Animal.objects.none() # Or handle anonymous users as needed
