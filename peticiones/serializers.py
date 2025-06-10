from rest_framework import serializers
from .models import Peticion
from usuarios.serializers import UserDetailSerializer

class PeticionListSerializer(serializers.ModelSerializer):
    """Serializer for listing and retrieving petitions, showing nested user details."""
    usuario = UserDetailSerializer(read_only=True)

    class Meta:
        model = Peticion
        fields = ['id', 'animal', 'usuario', 'estado', 'leida', 'fecha_peticion']

class PeticionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new petition. 'estado' and 'leida' are not settable by the user."""
    class Meta:
        model = Peticion
        fields = ['id', 'animal', 'usuario', 'estado', 'leida', 'fecha_peticion']
        read_only_fields = ['usuario', 'fecha_peticion', 'estado', 'leida']

    def validate_animal(self, value):
        """
        Check that the animal is not already adopted or in process.
        """
        if value.estado != 'No adoptado':
            raise serializers.ValidationError("Este animal no está disponible para adopción.")
        return value

class PeticionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for a company to update a petition. Only 'estado' and 'leida' can be changed."""
    class Meta:
        model = Peticion
        fields = ['estado', 'leida'] # Only expose these two fields for update 