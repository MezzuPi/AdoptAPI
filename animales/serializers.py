from rest_framework import serializers
from .models import Animal, Decision
import cloudinary.uploader

class AnimalSerializer(serializers.ModelSerializer):
    imagen1_file = serializers.ImageField(write_only=True, required=False)
    imagen2_file = serializers.ImageField(write_only=True, required=False)
    imagen3_file = serializers.ImageField(write_only=True, required=False)
    imagen4_file = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Animal
        exclude = ['empresa']  # no se envía desde el frontend
        read_only_fields = ('imagen1', 'imagen2', 'imagen3', 'imagen4')

    def create(self, validated_data):
        images = {}
        for i in range(1, 5):
            image_field_name = f'imagen{i}_file'
            image_file = validated_data.pop(image_field_name, None)
            if image_file:
                try:
                    upload_result = cloudinary.uploader.upload(image_file)
                    images[f'imagen{i}'] = upload_result['secure_url']
                except Exception as e:
                    # Handle upload error, maybe log it or raise a validation error
                    print(f"Error uploading {image_field_name}: {e}") # Or raise serializers.ValidationError
            else:
                images[f'imagen{i}'] = None # Or keep blank=True in model and don't set

        # Assign uploaded image URLs to the model fields
        for i in range(1, 5):
            validated_data[f'imagen{i}'] = images.get(f'imagen{i}')

        animal = Animal.objects.create(**validated_data)
        return animal

class DecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decision
        fields = ['id', 'usuario', 'animal', 'tipo_decision', 'fecha_decision']
        read_only_fields = ['usuario', 'fecha_decision']
