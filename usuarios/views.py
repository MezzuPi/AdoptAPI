from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from usuarios.serializers import UserRegistrationSerializer, UserLoginSerializer, UserDetailSerializer, UserProfileUpdateSerializer, PasswordChangeSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.authtoken.models import Token
from usuarios.models import CustomUser

CustomUser = get_user_model()

# View Registro de usuario adoptante
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Forzamos que sea tipo USUARIO si no se especifica
        if 'tipo' not in request.data:
            request.data['tipo'] = 'USUARIO'
        return super().post(request, *args, **kwargs)


# View Registro de empresa (Comment out or remove this class)
# class CompanyRegistrationView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CompanyRegistrationSerializer # This serializer is no longer available
#     permission_classes = [AllowAny]


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Vista para login que devuelve un token de autenticación y establece una sesión.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'tipo': user.tipo,
                'username': user.username,
                'es_aprobada': user.es_aprobada if user.tipo == 'EMPRESA' else None
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Credenciales inválidas'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Vista para logout que elimina el token y cierra la sesión.
    """
    try:
        # Eliminar el token del usuario
        if hasattr(request.user, 'auth_token') and request.user.auth_token:
            request.user.auth_token.delete()
        logout(request)
        return Response({
            'message': 'Logout exitoso'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': f'Error al hacer logout: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Vista para obtener el perfil del usuario autenticado
    """
    user = request.user
    data = {
        'id': user.id,
        'username': user.username,
        'tipo': user.tipo,
        'telefono': user.telefono,
        'provincia': user.provincia,
    }
    
    if user.tipo == 'USUARIO':
        data.update({
            'biografia': user.biografia,
            'tiene_ninos': user.tiene_ninos,
            'tiene_otros_animales': user.tiene_otros_animales,
            'tipo_vivienda': user.tipo_vivienda,
            'prefiere_pequenos': user.prefiere_pequenos,
            'disponible_para_paseos': user.disponible_para_paseos,
            'acepta_enfermos': user.acepta_enfermos,
            'acepta_viejos': user.acepta_viejos,
            'busca_tranquilo': user.busca_tranquilo,
            'tiene_trabajo': user.tiene_trabajo,
            'animal_estara_solo': user.animal_estara_solo,
        })
    elif user.tipo == 'EMPRESA':
        data.update({
            'nombre_empresa': user.nombre_empresa,
            'es_aprobada': user.es_aprobada,
        })
    
    return Response(data, status=status.HTTP_200_OK)


# View Login Prueba (mantenemos para testing)
@csrf_exempt  # para probar rápido, luego en producción lo mejor es manejar CSRF bien
def registro_prueba(request):
    if request.method == 'GET':
        # Mostrar formulario HTML simple
        html_form = '''
        <form method="post">
            Email: <input type="email" name="username" required><br>
            Contraseña: <input type="password" name="password" required><br>
            Tipo: <select name="tipo" required>
                <option value="USUARIO">Usuario Adoptante</option>
                <option value="EMPRESA">Empresa/Protectora</option>
            </select><br>
            Teléfono: <input type="text" name="telefono"><br>
            Provincia: <select name="provincia">
                <option value="">Selecciona provincia...</option>
                <option value="Madrid">Madrid</option>
                <option value="Barcelona">Barcelona</option>
                <option value="Valencia">Valencia</option>
                <!-- Agrega más provincias según necesites -->
            </select><br>
            
            <div id="usuario-fields">
                <h3>Campos para Adoptantes:</h3>
                Tiene niños: <input type="checkbox" name="tiene_ninos"><br>
                Tiene otros animales: <input type="checkbox" name="tiene_otros_animales"><br>
                Tipo vivienda (grande): <input type="checkbox" name="tipo_vivienda"><br>
                Prefiere pequeños: <input type="checkbox" name="prefiere_pequenos"><br>
                Disponible para paseos: <input type="checkbox" name="disponible_para_paseos"><br>
                Acepta enfermos: <input type="checkbox" name="acepta_enfermos"><br>
                Acepta viejos: <input type="checkbox" name="acepta_viejos"><br>
                Busca tranquilo: <input type="checkbox" name="busca_tranquilo"><br>
                Tiene trabajo: <input type="checkbox" name="tiene_trabajo"><br>
                Animal estará solo: <input type="checkbox" name="animal_estara_solo"><br>
            </div>
            
            <div id="empresa-fields" style="display:none;">
                <h3>Campos para Empresas:</h3>
                Nombre de la empresa: <input type="text" name="nombre_empresa"><br>
            </div>
            
            <button type="submit">Registrar</button>
        </form>
        
        <script>
            document.querySelector('select[name="tipo"]').addEventListener('change', function() {
                const userFields = document.getElementById('usuario-fields');
                const empresaFields = document.getElementById('empresa-fields');
                if (this.value === 'EMPRESA') {
                    userFields.style.display = 'none';
                    empresaFields.style.display = 'block';
                } else {
                    userFields.style.display = 'block';
                    empresaFields.style.display = 'none';
                }
            });
        </script>
        '''
        return HttpResponse(html_form)

    elif request.method == 'POST':
        tipo = request.POST.get('tipo', 'USUARIO')
        
        data = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
            'tipo': tipo,
            'telefono': request.POST.get('telefono', ''),
            'provincia': request.POST.get('provincia', ''),
        }
        
        if tipo == 'USUARIO':
            # Campos específicos para usuarios adoptantes
            data.update({
                'tiene_ninos': bool(request.POST.get('tiene_ninos')),
                'tiene_otros_animales': bool(request.POST.get('tiene_otros_animales')),
                'tipo_vivienda': bool(request.POST.get('tipo_vivienda')),
                'prefiere_pequenos': bool(request.POST.get('prefiere_pequenos')),
                'disponible_para_paseos': bool(request.POST.get('disponible_para_paseos')),
                'acepta_enfermos': bool(request.POST.get('acepta_enfermos')),
                'acepta_viejos': bool(request.POST.get('acepta_viejos')),
                'busca_tranquilo': bool(request.POST.get('busca_tranquilo')),
                'tiene_trabajo': bool(request.POST.get('tiene_trabajo')),
                'animal_estara_solo': bool(request.POST.get('animal_estara_solo')),
            })
            serializer = UserRegistrationSerializer(data=data)
        else:
            # Campos específicos para empresas
            data.update({
                'nombre_empresa': request.POST.get('nombre_empresa', ''),
            })
            serializer = CompanyRegistrationSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            return HttpResponse(f"Usuario registrado correctamente. Tipo: {user.tipo}")
        else:
            return HttpResponse(f"Errores: {serializer.errors}")


@api_view(['GET'])
@permission_classes([AllowAny])
def api_documentation(request):
    """
    Vista que muestra la documentación básica de la API
    """
    documentation = {
        'endpoints': {
            'POST /api/auth/register/': 'Registrar nuevo usuario (solo tipo USUARIO). Campos: email, password, [opcional: tipo=\"USUARIO\", telefono, provincia, y campos de perfil de adoptante].',
            'POST /api/auth/login/': 'Iniciar sesión de usuario (USUARIO o EMPRESA). Campos: email, password. Devuelve token y datos de usuario.',
            'POST /api/auth/logout/': 'Cerrar sesión de usuario (requiere token). Invalida el token en el servidor.',
            'GET /api/auth/profile/': 'Obtener perfil del usuario autenticado (requiere token).',
            'PUT/PATCH /api/auth/profile/': 'Actualizar perfil del usuario autenticado (requiere token).',
            'GET /api/auth/check-email/': 'Verificar disponibilidad de email para registro. Query param: email. Devuelve {available: true/false, email: "email@example.com"}.',
            # Documentación de animales (asumiendo que está en animales.urls y accesible bajo /api/)
            'GET /api/animales/': 'Listar todos los animales (requiere autenticación).',
            'POST /api/animales/': 'Crear un nuevo animal (requiere autenticación y ser tipo EMPRESA).',
            'GET /api/animales/{id}/': 'Obtener detalles de un animal específico (requiere autenticación).',
            'PUT /api/animales/{id}/': 'Actualizar un animal (requiere autenticación, usualmente EMPRESA dueña o admin).',
            'DELETE /api/animales/{id}/': 'Eliminar un animal (requiere autenticación, usualmente EMPRESA dueña o admin).',
            
            # Documentación de Peticiones
            'GET /api/peticiones/': 'Listar peticiones. Para usuarios, lista sus propias peticiones. Para empresas, lista las peticiones de sus animales.',
            'POST /api/peticiones/': 'Crear una nueva petición de adopción para un animal. Requiere ser tipo USUARIO. Campo: animal (ID del animal).',
            'GET /api/peticiones/{id}/': 'Ver el detalle de una petición específica.',
            'PUT/PATCH /api/peticiones/{id}/': 'Actualizar una petición. Requiere ser tipo EMPRESA y dueña del animal. Campos: estado ("Aceptada", "Rechazada"), leida (true/false). Al aceptar, el estado del animal cambia a "En proceso".',
            'DELETE /api/peticiones/{id}/': 'Cancelar (eliminar) una petición. Requiere ser el USUARIO que la creó. Solo se puede cancelar si el estado es "Pendiente".',
            
            'GET /registro-prueba/': 'Formulario de prueba HTML para registro (solo para desarrollo).',
        },
        'auth_header': 'Authorization: Token tu_token_aqui',
        'example_user_registration (POST /api/auth/register/)': {
            'email': 'usuario@example.com',
            'password': 'tu_contraseña_segura',
            'tipo': 'USUARIO', # Este campo es opcional, por defecto es USUARIO. No se permite EMPRESA.
            'telefono': '600112233',
            'provincia': 'Madrid',
            # ... otros campos opcionales de perfil de adoptante ...
        },
        'example_email_check (GET /api/auth/check-email/)': {
            'url': '/api/auth/check-email/?email=usuario@example.com',
            'response_success': {
                'available': True,
                'email': 'usuario@example.com'
            },
            'response_error': {
                'error': 'Email is required'
            }
        },
        'example_login (POST /api/auth/login/)': {
            'email': 'usuario@example.com', # o empresa@example.com
            'password': 'tu_contraseña',
        }
    }
    
    return Response(documentation, status=status.HTTP_200_OK)


@csrf_exempt
def login_prueba(request):
    if request.method == 'GET':
        html_form = """
        <form method="post">
            <h2>Test Login</h2>
            Email: <input type="email" name="username" required><br>
            Contraseña: <input type="password" name="password" required><br>
            <button type="submit">Login</button>
        </form>
        """
        return HttpResponse(html_form)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            response_html = f"""
            <h2>Login Exitoso!</h2>
            <p><strong>Usuario:</strong> {user.username}</p>
            <p><strong>Tipo:</strong> {user.tipo}</p>
            <p><strong>Token:</strong> {token.key}</p>
            <p><a href="/registro-prueba/">Registrar otro</a> | <a href="/login-prueba/">Login otro</a></p>
            """
            return HttpResponse(response_html)
        else:
            error_html = """
            <h2>Error de Login</h2>
            <p>Credenciales inválidas. Inténtalo de nuevo.</p>
            <p><a href="/login-prueba/">Volver a Login</a></p>
            """
            return HttpResponse(error_html, status=401)


class UserLoginView(generics.CreateAPIView):
    """
    API view for user login.
    Allows registered users to log in and obtain an authentication token.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny] # Anyone can attempt to log in

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # For session-based auth, login the user:
            # login(request, user)
            
            # For token-based auth, create or retrieve a token:
            token, created = Token.objects.get_or_create(user=user)
            user_data = UserDetailSerializer(user).data
            return Response({
                "message": "Inicio de sesión correcto.",
                "token": token.key,
                "user": user_data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(generics.CreateAPIView):
    """
    API view for user logout.
    If using token authentication, this typically involves deleting the token on the client-side.
    If using session authentication, this logs the user out of the session.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can log out

    def post(self, request, *args, **kwargs):
        # For token-based authentication, the client should discard the token.
        # If you want to invalidate the token on the server-side (requires custom token handling or Django Rest Knox/dj-rest-auth):
        try:
            # This will delete the user's current token, forcing them to re-authenticate.
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            # Handle cases where the token might not exist or user has no auth_token attribute
            pass # Or log this, depending on your error handling policy

        # For session-based authentication, call Django's logout:
        # logout(request)
        
        return Response({"message": "Cierre de sesión exitoso."}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating the authenticated user's profile.
    """
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        """Return the authenticated user's profile data."""
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Update the authenticated user's profile data."""
        return super().put(request, *args, **kwargs)


class UpdateUserProfileView(generics.UpdateAPIView):
    """
    API view for updating user profile settings.
    Only allows updating specific fields and requires authentication.
    """
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class PasswordChangeView(generics.UpdateAPIView):
    """
    API view for changing user password.
    Requires authentication and current password.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Contraseña actualizada correctamente"
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_email_availability(request):
    """
    Check if an email is available for registration.
    Returns a JSON response indicating if the email is available and the email itself.
    """
    email = request.query_params.get('email')
    
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if email already exists
    exists = CustomUser.objects.filter(username=email).exists()
    
    return Response({
        'available': not exists,
        'email': email
    })
