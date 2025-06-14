from django.contrib import admin
from .models import Animal

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'estado', 'empresa', 'genero', 'fecha_nacimiento', 'tamano', 'raza', 'esterilizado', 'problema_salud')
    list_filter = ('especie', 'estado', 'tamano', 'esterilizado', 'problema_salud', 'empresa')
    search_fields = ('nombre', 'raza', 'empresa__username')
