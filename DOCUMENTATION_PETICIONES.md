# Documentación de Endpoints de Peticiones

## Endpoints para Empresa/Backoffice

Los siguientes endpoints están diseñados específicamente para usuarios de tipo EMPRESA y permiten gestionar las peticiones de adopción de sus animales.

### Base URL
Todos los endpoints están disponibles bajo la ruta base: `/api/peticiones/`

### Autenticación
Todos los endpoints requieren autenticación y el usuario debe ser de tipo EMPRESA.

### Endpoints Disponibles

#### 1. Peticiones Default
```
GET /api/peticiones/default/
```
Muestra las peticiones con estado 'Aceptada' o 'Pendiente'.

#### 2. Peticiones Rechazadas
```
GET /api/peticiones/rechazadas/
```
Muestra solo las peticiones con estado 'Rechazada'.

#### 3. Peticiones Aceptadas
```
GET /api/peticiones/aceptadas/
```
Muestra solo las peticiones con estado 'Aceptada'.

#### 4. Peticiones Pendientes
```
GET /api/peticiones/pendientes/
```
Muestra solo las peticiones con estado 'Pendiente'.

### Ordenamiento

Todos los endpoints soportan ordenamiento dinámico a través de parámetros de consulta (query parameters).

#### Parámetros de Ordenamiento

1. `order_by`: Campo por el cual ordenar
   - Valores permitidos:
     - `fecha_peticion`: Fecha de la petición
     - `animal__nombre`: Nombre del animal
     - `animal__fecha_nacimiento`: Edad del animal
   - Por defecto: `fecha_peticion`

2. `order_direction`: Dirección del ordenamiento
   - Valores permitidos:
     - `asc`: Orden ascendente
     - `desc`: Orden descendente
   - Por defecto:
     - `desc` para `fecha_peticion`
     - `asc` para otros campos

#### Ejemplos de Uso

1. Ordenar por nombre del animal (A-Z):
```
GET /api/peticiones/default/?order_by=animal__nombre&order_direction=asc
```

2. Ordenar por nombre del animal (Z-A):
```
GET /api/peticiones/default/?order_by=animal__nombre&order_direction=desc
```

3. Ordenar por edad del animal (más joven primero):
```
GET /api/peticiones/default/?order_by=animal__fecha_nacimiento&order_direction=desc
```

4. Ordenar por fecha de petición (más antigua primero):
```
GET /api/peticiones/default/?order_by=fecha_peticion&order_direction=asc
```

### Respuesta

La respuesta de cada endpoint incluye una lista de peticiones con la siguiente estructura:

```json
[
  {
    "id": 1,
    "animal": {
      "id": 1,
      "nombre": "Nombre del Animal",
      "fecha_nacimiento": "2020-01-01",
      // ... otros campos del animal
    },
    "usuario": {
      "id": 1,
      "username": "nombre_usuario",
      // ... otros campos del usuario
    },
    "estado": "Pendiente",
    "leida": false,
    "fecha_peticion": "2024-03-20T10:00:00Z"
  },
  // ... más peticiones
]
```

### Notas Importantes

1. **Seguridad**:
   - Solo los usuarios de tipo EMPRESA pueden acceder a estos endpoints
   - Las empresas solo pueden ver peticiones relacionadas con sus propios animales

2. **Ordenamiento por Defecto**:
   - Si no se especifican parámetros de ordenamiento, se usa `fecha_peticion` en orden descendente
   - Si se especifica un campo de ordenamiento inválido, se usa el valor por defecto

3. **Rendimiento**:
   - Los endpoints utilizan `select_related` para optimizar las consultas a la base de datos
   - Se recomienda implementar paginación en el frontend para grandes conjuntos de datos

### Ejemplo de Uso en Frontend

```javascript
// Ejemplo usando fetch
async function getPeticiones(estado = 'default', orderBy = 'fecha_peticion', orderDirection = 'desc') {
  const response = await fetch(
    `/api/peticiones/${estado}/?order_by=${orderBy}&order_direction=${orderDirection}`,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    }
  );
  return await response.json();
}

// Ejemplo de uso
const peticiones = await getPeticiones('default', 'animal__nombre', 'asc');
```

### Manejo de Errores

Los endpoints pueden devolver los siguientes códigos de estado:

- `200 OK`: La solicitud fue exitosa
- `401 Unauthorized`: Usuario no autenticado
- `403 Forbidden`: Usuario no es de tipo EMPRESA
- `400 Bad Request`: Parámetros de ordenamiento inválidos 