from django.db import models
from django.conf import settings
from animales.models import Animal

class Peticion(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='peticiones')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='peticiones')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')
    leida = models.BooleanField(default=False)
    fecha_peticion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('animal', 'usuario')

    def __str__(self):
        return f"Petición de {self.usuario.username} para {self.animal.nombre}"
