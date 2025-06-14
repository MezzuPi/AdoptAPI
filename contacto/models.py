from django.db import models
from usuarios.models import PROVINCIAS_CHOICES

# Create your models here.

class ContactForm(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    provincia = models.CharField(max_length=50, choices=PROVINCIAS_CHOICES, null=True, blank=True)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f"Contacto de {self.nombre_empresa} - {self.fecha_envio}"
