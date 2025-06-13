from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Animal
from .serializers import AnimalSerializer

# Create your views here.

class IsEmpresaUser(permissions.BasePermission):
    """
    Custom permission to only allow users of type 'EMPRESA' to access POST.
    """
    def has_permission(self, request, view):
        # Allow all users to see the list or details of animals
        if view.action in ['list', 'retrieve']:
            return True
        # Only allow companies to create animals
        return request.user.is_authenticated and request.user.tipo == 'EMPRESA'

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owner of an object to edit it.
    Assumes the model instance has an `empresa` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the company that owns the animal.
        return obj.empresa == request.user

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        - Anyone can list or view.
        - Companies can create.
        - Only the owner company can update or delete.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwner]
        elif self.action == 'create':
            self.permission_classes = [IsEmpresaUser]
        else: # list, retrieve
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Automatically set the empresa to the logged-in user."""
        serializer.save(empresa=self.request.user)

    # You can add more custom actions or override other methods here if needed
    # For example, to list only animals created by the current empresa:
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.tipo == 'EMPRESA':
                return Animal.objects.filter(empresa=user)
            elif user.tipo == 'USUARIO': # Or is_staff for admin view all
                return Animal.objects.all() # Allow particulars to see all
        return Animal.objects.all() # Or handle anonymous users as needed
