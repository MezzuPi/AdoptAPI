from django.db import models
from usuarios.models import CustomUser
from django.conf import settings

class Animal(models.Model):
    ESPECIE_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
    ]

    GENERO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]

    TAMANO_CHOICES = [
        ('pequeño', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
    ]

    APTITUD_NINOS = [
        ('excelente', 'Excelente'),
        ('bueno', 'Bueno'),
        ('precaucion', 'Precaución'),
        ('noRecomendado', 'No recomendado'),
        ('desconocido', 'Desconocido')
    ]

    COMPATIBILIDAD = [
        ('excelente', 'Excelente'),
        ('bienConPerros', 'Bien con perros'),
        ('bienConGatos', 'Bien con gatos'),
        ('selectivo', 'Selectivo'),
        ('prefiereSolo', 'Prefiere estar solo'),
        ('desconocido', 'Desconocido')
    ]
    
    APTITUD_ESPACIO = [
        ('ideal', 'Ideal'),
        ('bueno', 'Bueno'),
        ('requiereEspacio', 'Requiere espacio'),
        ('soloConJardin', 'Solo con jardín'),
        ('desconocido', 'Desconocido')
    ]

    ESTADO_CHOICES = [
        ('No adoptado', 'No adoptado'),
        ('En proceso', 'En proceso'),
        ('Adoptado', 'Adoptado'),
    ]

    empresa = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'tipo': 'EMPRESA'}, related_name='animales') 
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=10, choices=ESPECIE_CHOICES)
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES)
    fecha_nacimiento = models.DateField()
    tamano = models.CharField(max_length=10, choices=TAMANO_CHOICES)
    raza = models.CharField(max_length=100)
    temperamento = models.TextField()
    historia = models.TextField()
    apto_ninos = models.CharField(max_length=20, choices=APTITUD_NINOS)
    compatibilidad_mascotas = models.CharField(max_length=20, choices=COMPATIBILIDAD)
    apto_piso_pequeno = models.CharField(max_length=20, choices=APTITUD_ESPACIO)
    esterilizado = models.BooleanField()
    problema_salud = models.BooleanField(default=False)
    descripcion_salud = models.CharField(max_length=255, blank=True)

    imagen1 = models.URLField(blank=True, null=True)
    imagen2 = models.URLField(blank=True, null=True)
    imagen3 = models.URLField(blank=True, null=True)
    imagen4 = models.URLField(blank=True, null=True)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='No adoptado')

    def __str__(self):
        return self.nombre

class Decision(models.Model):
    TIPO_DECISION_CHOICES = [
        ('SOLICITAR', 'Solicitar'),
        ('IGNORAR', 'Ignorar'),
    ]

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='decisiones')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='decisiones')
    tipo_decision = models.CharField(max_length=10, choices=TIPO_DECISION_CHOICES)
    fecha_decision = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'animal')  # Un usuario solo puede decidir una vez sobre un animal

    def __str__(self):
        return f"{self.usuario.username} - {self.animal.nombre} - {self.tipo_decision}"
