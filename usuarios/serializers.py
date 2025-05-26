from rest_framework import serializers
from usuarios.models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, label='Confirmar contraseña', style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = [
            'username',  # aquí va el email
            'password',
            'password2',
            'tipo',
            'telefono',
            'provincia',
            # campos solo para usuarios adoptantes
            'tiene_ninos',
            'tiene_otros_animales',
            'tipo_vivienda',
            'prefiere_pequenos',
            'disponible_para_paseos',
            'acepta_enfermos',
            'acepta_viejos',
            'busca_tranquilo',
            'tiene_trabajo',
            'animal_estara_solo',
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        if data.get('tipo') not in ['USUARIO', 'EMPRESA']:
            raise serializers.ValidationError({"tipo": "Tipo de usuario inválido."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CompanyRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, label='Confirmar contraseña', style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'password',
            'password2',
            'tipo',
            'telefono',
            'provincia',
            'nombre_empresa',
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        if data.get('tipo') != 'EMPRESA':
            raise serializers.ValidationError({"tipo": "Este registro es solo para empresas."})
        if not data.get('nombre_empresa'):
            raise serializers.ValidationError({"nombre_empresa": "El nombre de la empresa es obligatorio."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        # Forzamos que sea empresa y requiera aprobación
        validated_data['tipo'] = 'EMPRESA'
        validated_data['es_aprobada'] = False
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField(write_only=True)
