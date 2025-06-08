from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Campos que se muestran en la lista de usuarios
    list_display = ('username', 'nombre', 'tipo', 'telefono', 'provincia', 'is_staff', 'date_joined')
    list_filter = ('tipo', 'provincia', 'is_staff', 'is_active', 'es_aprobada')
    search_fields = ('username', 'nombre', 'telefono', 'nombre_empresa')
    
    # Organización de campos en el formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('nombre', 'tipo', 'telefono', 'provincia')
        }),
        ('Perfil de Adoptante', {
            'fields': (
                'tiene_ninos', 'tiene_otros_animales', 'tipo_vivienda',
                'prefiere_pequenos', 'disponible_para_paseos', 'acepta_enfermos',
                'acepta_viejos', 'busca_tranquilo', 'tiene_trabajo', 'animal_estara_solo'
            ),
            'classes': ('collapse',)  # Hace que esta sección sea colapsable
        }),
        ('Información de Empresa', {
            'fields': ('nombre_empresa', 'es_aprobada'),
            'classes': ('collapse',)
        }),
    )
    
    # Campos para mostrar al crear un nuevo usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('nombre', 'tipo', 'telefono', 'provincia')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
