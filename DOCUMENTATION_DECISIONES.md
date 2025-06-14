# Documentación: Sistema de Decisiones y Peticiones

## Visión General

El sistema utiliza dos modelos complementarios para manejar la interacción de usuarios con animales:

1. **Decision**: Registra las interacciones iniciales de los usuarios con los animales
2. **Peticion**: Maneja el proceso formal de solicitud de adopción

## Modelo Decision

### Propósito
- Registra si un usuario ha visto/interactuado con un animal
- Se utiliza para filtrar el feed de animales, evitando mostrar animales que el usuario ya ha visto
- Cada usuario solo puede tomar una decisión sobre cada animal

### Tipos de Decisión
- `SOLICITAR`: El usuario está interesado en el animal
- `IGNORAR`: El usuario no está interesado en el animal

### Endpoint: `/api/decisiones/`

#### Crear una Decisión
```http
POST /api/decisiones/
Authorization: Token <token_usuario>
Content-Type: application/json

{
    "animal": <id_animal>,
    "tipo_decision": "SOLICITAR"  // o "IGNORAR"
}
```

#### Ver Decisiones
```http
GET /api/decisiones/
Authorization: Token <token_usuario>
```

- Usuarios normales: ven solo sus propias decisiones
- Empresas: ven todas las decisiones sobre sus animales

#### Resetear Animales Ignorados
```http
DELETE /api/decisiones/reset_ignorados/
Authorization: Token <token_usuario>
```

- Solo disponible para usuarios normales
- Elimina todas las decisiones de tipo "IGNORAR" del usuario
- Permite volver a ver todos los animales que fueron ignorados anteriormente
- No afecta a las decisiones de tipo "SOLICITAR"

## Modelo Peticion

### Propósito
- Maneja el proceso formal de solicitud de adopción
- Permite a las empresas gestionar las solicitudes (aceptar/rechazar)
- Cuando una petición es aceptada, el estado del animal cambia a "En proceso"

### Estados de Petición
- `Pendiente`: La solicitud está esperando respuesta
- `Aceptada`: La empresa ha aceptado la solicitud
- `Rechazada`: La empresa ha rechazado la solicitud

### Endpoint: `/api/peticiones/`

#### Crear una Petición
```http
POST /api/peticiones/
Authorization: Token <token_usuario>
Content-Type: application/json

{
    "animal": <id_animal>
}
```

#### Ver Peticiones
```http
GET /api/peticiones/
Authorization: Token <token_usuario>
```

- Usuarios normales: ven solo sus propias peticiones
- Empresas: ven todas las peticiones para sus animales

## Flujo de Trabajo Recomendado

1. **Para Usuarios Normales**:
   - Al ver un animal en el feed, el usuario debe:
     1. Primero crear una `Decision` (SOLICITAR/IGNORAR)
     2. Si la decisión es "SOLICITAR", crear una `Peticion`
   - El feed solo mostrará animales que:
     - No están adoptados
     - El usuario no ha tomado una decisión sobre ellos

2. **Para Empresas**:
   - Pueden ver todos sus animales sin importar el estado
   - Pueden ver todas las decisiones y peticiones sobre sus animales
   - Pueden gestionar las peticiones (aceptar/rechazar)

## Ejemplo de Uso en el Frontend

```javascript
// 1. Usuario ve un animal y decide solicitarlo
async function solicitarAnimal(animalId) {
    // Primero crear la decisión
    await axios.post('/api/decisiones/', {
        animal: animalId,
        tipo_decision: 'SOLICITAR'
    });

    // Luego crear la petición
    await axios.post('/api/peticiones/', {
        animal: animalId
    });
}

// 2. Usuario decide ignorar un animal
async function ignorarAnimal(animalId) {
    await axios.post('/api/decisiones/', {
        animal: animalId,
        tipo_decision: 'IGNORAR'
    });
}

// 3. Obtener el feed de animales
async function obtenerFeed() {
    const response = await axios.get('/api/animales/');
    return response.data;
}

// 4. Resetear todos los animales ignorados
async function resetearIgnorados() {
    await axios.delete('/api/decisiones/reset_ignorados/');
}
```

## Notas Importantes

1. Una vez que un usuario toma una decisión sobre un animal, este desaparecerá de su feed
2. Las empresas siempre verán todos sus animales, independientemente de las decisiones de los usuarios
3. El estado de un animal puede ser:
   - "No adoptado"
   - "En proceso" (cuando una petición es aceptada)
   - "Adoptado"
4. Los usuarios no autenticados solo verán animales no adoptados 