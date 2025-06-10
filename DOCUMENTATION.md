# AdoptaAPI - Documentación de Peticiones

Esta documentación detalla el funcionamiento del módulo de `Peticiones` de la AdoptaAPI, diseñado para que los usuarios puedan solicitar la adopción de animales y para que las empresas (protectoras) puedan gestionar dichas solicitudes.

## Modelo de Datos: `Peticion`

Una `Peticion` representa la solicitud de un `Usuario` para adoptar un `Animal`.

-   `animal`: El animal que se desea adoptar.
-   `usuario`: El usuario que realiza la petición.
-   `estado`: El estado actual de la petición. Puede ser:
    -   `'Pendiente'`: La solicitud ha sido creada y está esperando revisión por parte de la empresa.
    -   `'Aceptada'`: La empresa ha aceptado la solicitud. El animal pasa a estado `'En proceso'`.
    -   `'Rechazada'`: La empresa ha rechazado la solicitud.
-   `leida`: Un booleano que indica si la empresa ha visto la petición.
-   `fecha_peticion`: La fecha en que se creó la solicitud.

---

## API Endpoints (`/api/peticiones/`)

La gestión de peticiones se realiza a través de un `ViewSet` que ofrece las siguientes operaciones.

### 1. Crear una Petición de Adopción

Un `Usuario` puede solicitar adoptar un animal.

-   **Endpoint:** `POST /api/peticiones/`
-   **Permisos:** Solo para usuarios autenticados de tipo `USUARIO`.
-   **Request Body (JSON):**
    ```json
    {
      "animal": <ID_DEL_ANIMAL>
    }
    ```
-   **Lógica Importante:**
    -   El `usuario` se asigna automáticamente basándose en el usuario autenticado.
    -   El `estado` inicial siempre es `'Pendiente'`.
    -   El `leida` inicial es `false`.
    -   **Validación:** No se puede crear una petición para un animal que no tenga el estado `'No adoptado'`.
-   **Response (201 Created):**
    ```json
    {
      "id": 1,
      "animal": <ID_DEL_ANIMAL>,
      "usuario": <ID_DEL_USUARIO>,
      "estado": "Pendiente",
      "leida": false,
      "fecha_peticion": "2023-10-27T10:00:00Z"
    }
    ```

### 2. Listar Peticiones

Tanto `Usuarios` como `Empresas` pueden listar peticiones, pero con diferentes alcances.

-   **Endpoint:** `GET /api/peticiones/`
-   **Permisos:** Requiere autenticación.
-   **Lógica de Acceso:**
    -   Si el usuario es de tipo `USUARIO`, verá **solo sus propias peticiones**.
    -   Si el usuario es de tipo `EMPRESA`, verá **todas las peticiones hechas para sus animales**.
-   **Response (200 OK):**
    Un array de objetos Petición. El objeto `usuario` viene anidado con detalles.
    ```json
    [
      {
        "id": 1,
        "animal": <ID_DEL_ANIMAL>,
        "usuario": {
            "id": <ID_USUARIO>,
            "username": "nombredeusuario",
            "email": "usuario@email.com"
        },
        "estado": "Pendiente",
        "leida": false,
        "fecha_peticion": "2023-10-27T10:00:00Z"
      }
    ]
    ```

### 3. Ver el Detalle de una Petición

-   **Endpoint:** `GET /api/peticiones/<ID_PETICION>/`
-   **Permisos:** Requiere autenticación. El usuario (`USUARIO` o `EMPRESA`) solo puede verla si está dentro de su `queryset` (sus peticiones o las de sus animales).

### 4. Gestionar una Petición (Empresa)

Una `Empresa` puede aceptar o rechazar una petición para uno de sus animales.

-   **Endpoint:** `PATCH /api/peticiones/<ID_PETICION>/`
-   **Permisos:** Solo para usuarios autenticados de tipo `EMPRESA`.
-   **Lógica de Acceso:** La empresa solo puede modificar peticiones asociadas a sus propios animales.
-   **Request Body (JSON):**
    Se pueden actualizar `estado` y/o `leida`.
    ```json
    {
      "estado": "Aceptada", // o "Rechazada"
      "leida": true
    }
    ```
-   **Lógica Importante:**
    -   Si el `estado` se cambia a `'Aceptada'`, el estado del `Animal` asociado se actualizará automáticamente a `'En proceso'`.
-   **Response (200 OK):**
    Devuelve la petición actualizada con el detalle del usuario.
    ```json
    {
      "id": 1,
      "animal": <ID_DEL_ANIMAL>,
      "usuario": { ... },
      "estado": "Aceptada",
      "leida": true,
      "fecha_peticion": "..."
    }
    ```

### 5. Cancelar una Petición (Usuario)

Un `Usuario` puede cancelar una petición que haya realizado.

-   **Endpoint:** `DELETE /api/peticiones/<ID_PETICION>/`
-   **Permisos:** Solo para el `USUARIO` que creó la petición.
-   **Lógica Importante:**
    -   Solo se puede cancelar una petición si su `estado` es `'Pendiente'`. Si ya ha sido `Aceptada` o `Rechazada`, no se puede eliminar.
-   **Response (204 No Content):**
    Respuesta vacía si la eliminación es exitosa.

---

## Flujo de Interacción para la Aplicación Frontend

### Para el Usuario (Adoptante)

1.  **Ver Animales:** El usuario navega por la lista de animales (`GET /api/animales/`).
2.  **Iniciar Adopción:** En la página de detalle de un animal, si el animal está "No adoptado", se muestra un botón "Adoptar".
3.  **Crear Petición:** Al hacer clic en "Adoptar", la app envía una `POST /api/peticiones/` con el `id` del animal.
    -   El `token` de autenticación del usuario debe ir en la cabecera `Authorization`.
4.  **Ver Mis Peticiones:** El usuario tiene una sección "Mis Peticiones" que hace una `GET /api/peticiones/` para listar el estado de todas sus solicitudes.
5.  **Cancelar Petición:** En su lista, puede cancelar cualquier petición que siga `'Pendiente'` haciendo `DELETE /api/peticiones/<ID_PETICION>/`.

### Para la Empresa (Protectora)

1.  **Dashboard de Peticiones:** La empresa tiene un panel donde ve todas las peticiones para los animales que ha registrado. Esto se logra con una `GET /api/peticiones/`.
    -   Se pueden destacar las peticiones con `leida: false` como "Nuevas".
2.  **Revisar Petición:** Al hacer clic en una petición, la empresa ve los detalles del animal y del solicitante. Marcarla como leída se puede hacer con una `PATCH` para cambiar `leida` a `true`.
3.  **Aceptar/Rechazar:** La empresa dispone de botones para "Aceptar" o "Rechazar".
    -   **Aceptar:** Envía un `PATCH /api/peticiones/<ID_PETICION>/` con `{"estado": "Aceptada"}`. La API se encarga de cambiar el estado del animal.
    -   **Rechazar:** Envía un `PATCH /api/peticiones/<ID_PETICION>/` con `{"estado": "Rechazada"}`.
4.  **Ver Peticiones por Animal:** En la página de gestión de un animal específico, la empresa podría ver una pestaña con todas las peticiones recibidas para ese animal. 