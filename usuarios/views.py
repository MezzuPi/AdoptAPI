from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from usuarios.serializers import UserRegistrationSerializer, CompanyRegistrationSerializer, UserLoginSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from usuarios.models import CustomUser


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


# View Registro de empresa
class CompanyRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CompanyRegistrationSerializer
    permission_classes = [AllowAny]


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
            Confirmar contraseña: <input type="password" name="password2" required><br>
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
            'password2': request.POST.get('password2'),
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
            'POST /api/register/user/': 'Registrar usuario adoptante',
            'POST /api/register/company/': 'Registrar empresa/protectora',
            'POST /api/login/': 'Login (devuelve token)',
            'POST /api/logout/': 'Logout (requiere token)',
            'GET /api/profile/': 'Obtener perfil del usuario (requiere token)',
            'GET /registro-prueba/': 'Formulario de prueba HTML',
        },
        'auth_header': 'Authorization: Token tu_token_aqui',
        'example_user_registration': {
            'username': 'user@example.com',
            'password': 'mi_password',
            'password2': 'mi_password',
            'tipo': 'USUARIO',
            'telefono': '123456789',
            'provincia': 'Madrid',
            'tiene_ninos': True,
            'tiene_otros_animales': False,
        },
        'example_company_registration': {
            'username': 'empresa@example.com',
            'password': 'mi_password',
            'password2': 'mi_password',
            'tipo': 'EMPRESA',
            'telefono': '123456789',
            'provincia': 'Madrid',
            'nombre_empresa': 'Mi Protectora',
        },
        'example_login': {
            'username': 'user@example.com',
            'password': 'mi_password',
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
