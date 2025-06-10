# AdoptaAPI - Documentación de Gestión de Animales

Esta documentación explica cómo las `Empresas` pueden modificar y eliminar los animales que han creado a través de la API.

---

## API Endpoints (`/api/animales/`)

La gestión de los animales creados por una empresa se realiza a través de los siguientes endpoints.

### 1. Modificar un Animal

Una `Empresa` puede modificar los datos de un animal que le pertenece. Se recomienda usar el método `PATCH` para actualizar solo los campos necesarios.

-   **Endpoint:** `PATCH /api/animales/<ID_ANIMAL>/`
-   **Permisos:**
    -   El usuario debe estar autenticado.
    -   El usuario debe ser de tipo `EMPRESA`.
    -   El usuario debe ser el propietario del animal (el `empresa` que lo creó).
    -   Se requiere el `token` de autenticación en la cabecera `Authorization`.
-   **Request Body (JSON):**
    El cuerpo de la solicitud puede contener cualquiera de los campos del modelo `Animal`. No es necesario enviarlos todos.

    **Campos de texto/número/booleanos:**
    `nombre`, `especie`, `raza`, `edad`, `tamaño`, `genero`, `descripcion`, `ubicacion`, `requisitos_adopcion`, `gastos_adopcion`, `estado`, `urgente`.

    **Campos de imagen (para subir nuevas imágenes):**
    `imagen1_file`, `imagen2_file`, `imagen3_file`, `imagen4_file`.

    **Ejemplo de Request Body:**
    ```json
    {
      "descripcion": "Ha aprendido nuevos trucos. ¡Es muy inteligente!",
      "requisitos_adopcion": "Necesita un hogar con jardín y sin otros perros."
    }
    ```
    Si se quiere actualizar una imagen, se debe enviar como `form-data` en lugar de `JSON`, incluyendo el campo de archivo correspondiente (ej: `imagen1_file`).

-   **Response (200 OK):**
    Devuelve el objeto `Animal` completo con los datos actualizados.
    ```json
    {
        "id": <ID_ANIMAL>,
        "nombre": "Firulais",
        "especie": "Perro",
        // ... todos los demás campos ...
        "descripcion": "Ha aprendido nuevos trucos. ¡Es muy inteligente!",
        "requisitos_adopcion": "Necesita un hogar con jardín y sin otros perros."
    }
    ```

### 2. Eliminar un Animal

Una `Empresa` puede eliminar un registro de animal que le pertenece.

-   **Endpoint:** `DELETE /api/animales/<ID_ANIMAL>/`
-   **Permisos:**
    -   El usuario debe estar autenticado.
    -   El usuario debe ser de tipo `EMPRESA`.
    -   El usuario debe ser el propietario del animal.
    -   Se requiere el `token` de autenticación en la cabecera `Authorization`.
-   **Request Body:**
    No se necesita cuerpo para esta solicitud.
-   **Response (204 No Content):**
    La respuesta no tiene contenido, indicando que el recurso fue eliminado exitosamente.

---

## Flujo de Interacción para la Aplicación Frontend

1.  **Panel de Gestión de Animales:** La empresa tiene una sección "Mis Animales" donde se listan los animales que ha creado. Esto se puede lograr con un `GET /api/animales/?empresa_id=<ID_EMPRESA>`.
2.  **Seleccionar un Animal:** La empresa hace clic en un animal de su lista para ir a una página de edición.
3.  **Modificar Datos:** La página de edición muestra un formulario con los datos actuales del animal. La empresa modifica los campos que necesite y guarda los cambios.
    -   Al guardar, la aplicación envía una petición `PATCH /api/animales/<ID_ANIMAL>/` con los campos que han cambiado. Si se modifican imágenes, la petición debe ser de tipo `multipart/form-data`.
4.  **Eliminar Animal:** En la página de edición o en el listado, hay un botón de "Eliminar".
    -   Al hacer clic (y probablemente tras una confirmación), la aplicación envía una petición `DELETE /api/animales/<ID_ANIMAL>/`.
    -   Tras una respuesta `204`, la aplicación debe refrescar la lista de animales para que el animal eliminado ya no aparezca. 