from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

CustomUser = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles creation of new users, ensuring password is properly hashed.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True, validators=[validate_email]) # Ensure email is validated

    class Meta:
        model = CustomUser
        # Define fields based on your CustomUser model, excluding username if it's derived from email
        fields = ('email', 'password', 'tipo', 'telefono', 'provincia',
                  'nombre', 'biografia', 'nombre_empresa', 'tiene_ninos', 'tiene_otros_animales', 'tipo_vivienda',
                  'prefiere_pequenos', 'disponible_para_paseos', 'acepta_enfermos',
                  'acepta_viejos', 'busca_tranquilo', 'tiene_trabajo', 'animal_estara_solo')
        extra_kwargs = {
            'nombre_empresa': {'required': False, 'allow_blank': True},
            'nombre': {'required': False, 'allow_blank': True},
            'biografia': {'required': False, 'allow_blank': True},
            'tiene_ninos': {'required': False},
            'tiene_otros_animales': {'required': False},
            'tipo_vivienda': {'required': False},
            'prefiere_pequenos': {'required': False},
            'disponible_para_paseos': {'required': False},
            'acepta_enfermos': {'required': False},
            'acepta_viejos': {'required': False},
            'busca_tranquilo': {'required': False},
            'tiene_trabajo': {'required': False},
            'animal_estara_solo': {'required': False},
            'telefono': {'required': False, 'allow_blank': True},
            'provincia': {'required': False, 'allow_blank': True},
        }

    def validate_email(self, value):
        """
        Check if the email is already in use.
        """
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        # Ensure username (which is email) is also checked for uniqueness via model validation
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este email (como username) ya está registrado.")
        return value
    
    def validate_tipo(self, value):
        """
        Validate the 'tipo' field.
        Only 'USUARIO' is allowed for registration via this API endpoint.
        'EMPRESA' accounts are created via the admin panel.
        """
        if value == 'EMPRESA':
            raise serializers.ValidationError(
                "Las empresas no pueden registrarse a través de este formulario. "
                "Las cuentas de empresa se crean desde el panel de administración."
            )
        if value != 'USUARIO': # Ensures only USUARIO, also covers if choices were different
            raise serializers.ValidationError(
                "Tipo de usuario inválido para el registro. Solo se permite 'USUARIO'."
            )
        return value # value will be 'USUARIO'

    def validate(self, attrs):
        """
        Check if passwords match.
        Ensure 'nombre_empresa' is blank for 'USUARIO' type if registration is for 'USUARIO'.
        """
        # tipo should be 'USUARIO' if it passed validate_tipo
        # We check initial_data in case 'nombre_empresa' was sent in the request
        submitted_nombre_empresa = self.initial_data.get('nombre_empresa')
        if submitted_nombre_empresa and submitted_nombre_empresa.strip():
            # This error is raised if nombre_empresa is sent with content for a USUARIO registration
            raise serializers.ValidationError(
                {"nombre_empresa": "El campo 'nombre_empresa' no es aplicable para el tipo 'USUARIO'."}
            )
        
        # Ensure 'nombre_empresa' is set to blank for 'USUARIO' before saving.
        # This handles cases where it might be None or an empty string from the input.
        attrs['nombre_empresa'] = ""

        # The old conditional logic for 'EMPRESA' type is removed as it's blocked by validate_tipo.
        # Fields specific to 'USUARIO' will be handled by the ModelSerializer.

        # Ensure AbstractUser's username (which is email) is set
        attrs['username'] = attrs['email']
        return attrs

    def create(self, validated_data):
        """
        Create and return a new user instance, given the validated data.
        """
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Authenticates users with email and password.
    """
    email = serializers.EmailField(label="Email", write_only=True)
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(label="Token", read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Note: Django's authenticate uses `username` field by default.
            # Since our CustomUser uses email as username, this works directly.
            user = authenticate(request=self.context.get('request'), username=email, password=password)

            if not user:
                msg = 'No se pudo iniciar sesión con las credenciales proporcionadas.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Debe incluir "email" y "contraseña".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying user details.
    Used to show user information after login or for profile views.
    """
    class Meta:
        model = CustomUser
        # List fields you want to expose. Be careful about sensitive data.
        fields = ('id', 'username', 'email', 'tipo', 'telefono', 'provincia', 'nombre', 'biografia', 'nombre_empresa', 'es_aprobada',
                  'tiene_ninos', 'tiene_otros_animales', 'tipo_vivienda', 'prefiere_pequenos',
                  'disponible_para_paseos', 'acepta_enfermos', 'acepta_viejos',
                  'busca_tranquilo', 'tiene_trabajo', 'animal_estara_solo',
                  'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
        read_only_fields = ('id', 'username', 'email', 'es_aprobada', 'is_staff', 'is_active', 'date_joined') # username is email

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile settings.
    Only includes fields that users are allowed to modify.
    """
    class Meta:
        model = CustomUser
        fields = (
            'telefono',
            'provincia',
            'nombre',
            'biografia',
            'tiene_ninos',
            'tiene_otros_animales',
            'tipo_vivienda',
            'prefiere_pequenos',
            'disponible_para_paseos',
            'acepta_enfermos',
            'acepta_viejos',
            'busca_tranquilo',
            'tiene_trabajo',
            'animal_estara_solo'
        )
        extra_kwargs = {
            'telefono': {'required': False, 'allow_blank': True},
            'provincia': {'required': False, 'allow_blank': True},
            'nombre': {'required': False, 'allow_blank': True},
            'biografia': {'required': False, 'allow_blank': True},
            'tiene_ninos': {'required': False},
            'tiene_otros_animales': {'required': False},
            'tipo_vivienda': {'required': False},
            'prefiere_pequenos': {'required': False},
            'disponible_para_paseos': {'required': False},
            'acepta_enfermos': {'required': False},
            'acepta_viejos': {'required': False},
            'busca_tranquilo': {'required': False},
            'tiene_trabajo': {'required': False},
            'animal_estara_solo': {'required': False}
        }

class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_current_password(self, value):
        """
        Check if the current password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value

    def validate_new_password(self, value):
        """
        Validate the new password.
        """
        user = self.context['request'].user
        # Use Django's built-in password validation
        from django.contrib.auth.password_validation import validate_password
        validate_password(value, user)
        return value

    def save(self, **kwargs):
        """
        Save the new password.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
