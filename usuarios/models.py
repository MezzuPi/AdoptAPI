from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email


PROVINCIAS_CHOICES = [
    ('Álava', 'Álava'),
    ('Albacete', 'Albacete'),
    ('Alicante', 'Alicante'),
    ('Almería', 'Almería'),
    ('Asturias', 'Asturias'),
    ('Ávila', 'Ávila'),
    ('Badajoz', 'Badajoz'),
    ('Barcelona', 'Barcelona'),
    ('Burgos', 'Burgos'),
    ('Cáceres', 'Cáceres'),
    ('Cádiz', 'Cádiz'),
    ('Castellón', 'Castellón'),
    ('Ciudad Real', 'Ciudad Real'),
    ('Córdoba', 'Córdoba'),
    ('Cuenca', 'Cuenca'),
    ('Gerona', 'Gerona'),
    ('Granada', 'Granada'),
    ('Guadalajara', 'Guadalajara'),
    ('Guipúzcoa', 'Guipúzcoa'),
    ('Huelva', 'Huelva'),
    ('Huesca', 'Huesca'),
    ('Jaén', 'Jaén'),
    ('La Rioja', 'La Rioja'),
    ('Las Palmas', 'Las Palmas'),
    ('León', 'León'),
    ('Lérida', 'Lérida'),
    ('Lugo', 'Lugo'),
    ('Madrid', 'Madrid'),
    ('Málaga', 'Málaga'),
    ('Murcia', 'Murcia'),
    ('Navarra', 'Navarra'),
    ('Orense', 'Orense'),
    ('Palencia', 'Palencia'),
    ('Pontevedra', 'Pontevedra'),
    ('Salamanca', 'Salamanca'),
    ('Segovia', 'Segovia'),
    ('Sevilla', 'Sevilla'),
    ('Soria', 'Soria'),
    ('Tarragona', 'Tarragona'),
    ('Teruel', 'Teruel'),
    ('Toledo', 'Toledo'),
    ('Valencia', 'Valencia'),
    ('Valladolid', 'Valladolid'),
    ('Vizcaya', 'Vizcaya'),
    ('Zamora', 'Zamora'),
    ('Zaragoza', 'Zaragoza'),
]

class CustomUser(AbstractUser):
    # Sobrescribimos username para que sea email
    username = models.EmailField('email address', unique=True, validators=[validate_email])

    USERNAME_FIELD = 'username'  # Usamos email para login
    REQUIRED_FIELDS = []  # username ya es obligatorio


    USER_TYPE_CHOICES = [
        ('USUARIO', 'Usuario'),
        ('EMPRESA', 'Empresa'),
    ]
    tipo = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    # Campos comunes
    telefono = models.CharField(max_length=20, blank=True)
    provincia = models.CharField(max_length=50, choices=PROVINCIAS_CHOICES, blank=True)

    # Solo para usuario adoptante
    nombre = models.CharField(max_length=100, blank=True)    
    tiene_ninos = models.BooleanField(default=False)
    tiene_otros_animales = models.BooleanField(default=False)
    tipo_vivienda = models.BooleanField(default=False)
    prefiere_pequenos = models.BooleanField(default=False)
    disponible_para_paseos = models.BooleanField(default=False)
    acepta_enfermos = models.BooleanField(default=False)
    acepta_viejos = models.BooleanField(default=False)
    busca_tranquilo = models.BooleanField(default=False)
    tiene_trabajo = models.BooleanField(default=False)
    animal_estara_solo = models.BooleanField(default=False)


    # Empresa
    nombre_empresa = models.CharField(max_length=100, blank=True)
    es_aprobada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.tipo})"
