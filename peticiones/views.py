from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Peticion, Animal
from .serializers import PeticionListSerializer, PeticionCreateSerializer, PeticionUpdateSerializer

# Create your views here.

class IsCompany(permissions.BasePermission):
    """
    Custom permission to only allow companies to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo == 'EMPRESA'

class IsUser(permissions.BasePermission):
    """
    Custom permission to only allow regular users to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo == 'USUARIO'

class PeticionViewSet(viewsets.ModelViewSet):
    queryset = Peticion.objects.all()
    # serializer_class will be determined by get_serializer_class

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return PeticionCreateSerializer
        if self.action in ['update', 'partial_update']:
            return PeticionUpdateSerializer
        return PeticionListSerializer # For 'list', 'retrieve'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        - Users can create ('create') and list/view their own petitions ('list', 'retrieve').
        - Companies can update ('update', 'partial_update'), and list/view petitions for their animals.
        """
        if self.action == 'create':
            self.permission_classes = [IsUser]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsCompany]
        elif self.action == 'destroy':
            self.permission_classes = [IsUser]
        else: # Covers 'list', 'retrieve', etc.
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        """
        This view should return a list of all the petitions
        for the currently authenticated user (if user) or for the
        company's animals (if company). Supports filtering by animal ID.
        """
        user = self.request.user
        queryset = Peticion.objects.none()
        if user.tipo == 'USUARIO':
            queryset = Peticion.objects.filter(usuario=user)
        elif user.tipo == 'EMPRESA':
            queryset = Peticion.objects.filter(animal__empresa=user)
        animal_id = self.request.query_params.get('animal')
        if animal_id:
            queryset = queryset.filter(animal_id=animal_id)
        return queryset

    def perform_create(self, serializer):
        """
        Associate the petition with the logged-in user.
        """
        serializer.save(usuario=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Custom update logic for petitions.
        - A company can update the 'estado' and 'leida' fields.
        - If a petition is accepted, the animal's estado is updated to 'En proceso'.
        """
        peticion = self.get_object()
        user = request.user

        # Security check: ensure the company owns the animal associated with the petition
        if peticion.animal.empresa != user:
            return Response({'error': 'No tiene permiso para modificar esta petición.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(peticion, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        new_estado = serializer.validated_data.get('estado')
        if new_estado == 'Aceptada':
            animal = peticion.animal
            animal.estado = 'En proceso'
            animal.save()
            
        self.perform_update(serializer)
        
        # After updating, return the detailed data using the ListSerializer
        return Response(PeticionListSerializer(peticion).data)

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy logic for petitions.
        - A user can only delete their own petition.
        - A petition can only be deleted if its estado is 'Pendiente'.
        """
        peticion = self.get_object() # This will raise 404 if not found for the user, due to get_queryset

        if peticion.estado != 'Pendiente':
            return Response(
                {'error': 'No se puede cancelar una petición que ya ha sido procesada por la empresa.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(peticion)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_base_queryset(self):
        """
        Base queryset for empresa peticiones with ordering.
        Supports dynamic ordering through query parameters:
        - order_by: field to order by ('fecha_peticion', 'animal__nombre', 'animal__fecha_nacimiento')
        - order_direction: 'asc' or 'desc' (defaults to 'desc' for fecha_peticion, 'asc' for others)
        """
        queryset = self.get_queryset().select_related('animal')
        
        # Get ordering parameters from request
        order_by = self.request.query_params.get('order_by', 'fecha_peticion')
        order_direction = self.request.query_params.get('order_direction', 'desc' if order_by == 'fecha_peticion' else 'asc')
        
        # Validate order_by field
        valid_fields = ['fecha_peticion', 'animal__nombre', 'animal__fecha_nacimiento']
        if order_by not in valid_fields:
            order_by = 'fecha_peticion'  # Default to fecha_peticion if invalid field
        
        # Apply ordering
        prefix = '-' if order_direction == 'desc' else ''
        return queryset.order_by(f'{prefix}{order_by}')

    @action(detail=False, methods=['get'], permission_classes=[IsCompany])
    def default(self, request):
        """
        Shows only Aceptadas or Pendientes peticiones for the empresa.
        Supports ordering through query parameters:
        - order_by: field to order by ('fecha_peticion', 'animal__nombre', 'animal__fecha_nacimiento')
        - order_direction: 'asc' or 'desc'
        """
        queryset = self._get_base_queryset().filter(
            estado__in=['Aceptada', 'Pendiente']
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsCompany])
    def rechazadas(self, request):
        """
        Shows only Rechazadas peticiones for the empresa.
        Supports ordering through query parameters:
        - order_by: field to order by ('fecha_peticion', 'animal__nombre', 'animal__fecha_nacimiento')
        - order_direction: 'asc' or 'desc'
        """
        queryset = self._get_base_queryset().filter(estado='Rechazada')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsCompany])
    def aceptadas(self, request):
        """
        Shows only Aceptadas peticiones for the empresa.
        Supports ordering through query parameters:
        - order_by: field to order by ('fecha_peticion', 'animal__nombre', 'animal__fecha_nacimiento')
        - order_direction: 'asc' or 'desc'
        """
        queryset = self._get_base_queryset().filter(estado='Aceptada')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsCompany])
    def pendientes(self, request):
        """
        Shows only Pendientes peticiones for the empresa.
        Supports ordering through query parameters:
        - order_by: field to order by ('fecha_peticion', 'animal__nombre', 'animal__fecha_nacimiento')
        - order_direction: 'asc' or 'desc'
        """
        queryset = self._get_base_queryset().filter(estado='Pendiente')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
