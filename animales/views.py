from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Animal, Decision
from .serializers import AnimalSerializer, DecisionSerializer
from rest_framework.decorators import action

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
                # Empresas ven todos sus propios animales
                return Animal.objects.filter(empresa=user)
            elif user.tipo == 'USUARIO':
                # Usuarios normales solo ven animales no adoptados que no han visto
                # y que están en su misma provincia
                animales_vistos = Decision.objects.filter(usuario=user).values_list('animal_id', flat=True)
                return Animal.objects.filter(
                    estado='No adoptado',
                    empresa__provincia=user.provincia  # Filtrar por provincia
                ).exclude(
                    id__in=animales_vistos
                )
        # Para usuarios no autenticados, mostrar todos los animales no adoptados
        return Animal.objects.filter(estado='No adoptado')

class DecisionViewSet(viewsets.ModelViewSet):
    serializer_class = DecisionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.tipo == 'EMPRESA':
            # Empresas solo ven decisiones sobre sus propios animales
            return Decision.objects.filter(animal__empresa=user)
        else:
            # Usuarios normales solo ven sus propias decisiones
            return Decision.objects.filter(usuario=user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['delete'])
    def reset_ignorados(self, request):
        """
        Elimina todas las decisiones de tipo 'IGNORAR' del usuario.
        Solo disponible para usuarios normales.
        """
        if request.user.tipo != 'USUARIO':
            return Response(
                {'error': 'Esta acción solo está disponible para usuarios normales.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        Decision.objects.filter(
            usuario=request.user,
            tipo_decision='IGNORAR'
        ).delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
