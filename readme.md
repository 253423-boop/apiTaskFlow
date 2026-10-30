# 📘 Documentación de la API REST — TaskFlow

Esta guía describe todos los endpoints disponibles en el backend de **TaskFlow**, detallando qué pantalla de la app Android los consume, cuándo debes enviar un `Body` en formato JSON y qué respuesta devuelve el servidor.

---

## 🌐 URLs Base de Conexión

Dependiendo de dónde ejecutes las pruebas, utiliza la siguiente URL base:

* **Desde tu navegador / Postman / Insomnia (PC):** `http://localhost:8000/api/v1`
* **Desde el Emulador de Android Studio:** `http://10.0.2.2:8000/api/v1`
* **Desde un teléfono Android físico (misma red Wi-Fi):** `http://TU_IP_LOCAL:8000/api/v1`
* **Documentación interactiva (Swagger UI):** `http://localhost:8000/docs`

> **Encabezado requerido en peticiones con Body (`POST` y `PUT`):**
> `Content-Type: application/json`

---

## 📋 Resumen Rápido de Endpoints

| Método | Endpoint | ¿Lleva Body? | Funcionalidad / Pantalla en Android |
| :--- | :--- | :---: | :--- |
| `POST` | `/api/v1/tasks/` | **Sí** | Registrar nueva tarea (Pantalla 3: Agregar tarea) |
| `GET` | `/api/v1/tasks/` | No | Consultar todas las tareas o filtrarlas (Pantalla 2: Mis tareas) |
| `GET` | `/api/v1/tasks/proxima-entrega` | No | Obtener la tarea pendiente más próxima (Pantalla 1: Inicio) |
| `GET` | `/api/v1/tasks/{task_id}` | No | Ver información completa de una tarea (Pantalla 4: Detalle) |
| `PUT` | `/api/v1/tasks/{task_id}` | **Sí** | Editar datos de una tarea o su estado (Pantalla 3: Editar tarea) |
| `PUT` | `/api/v1/tasks/{task_id}/completar` | No | Marcar tarea como completada directamente (Pantalla 4: Detalle) |
| `DELETE` | `/api/v1/tasks/{task_id}` | No | Eliminar tarea tras confirmación (Pantalla 4: Detalle) |

---

## 1. Registrar una nueva tarea (`CREATE`)

Se utiliza en la **Pantalla 3 (Agregar/Editar tarea)** cuando el usuario llena el formulario y presiona guardar.

* **Método:** `POST`
* **Ruta:** `/api/v1/tasks/`
* **¿Requiere Body?:** **Sí (JSON)**

### Reglas de los campos del Body:
| Campo | Tipo | Obligatorio | Descripción |
| :--- | :--- | :---: | :--- |
| `titulo` | `string` | **Sí** | Título de la actividad (1 a 150 caracteres). |
| `materia` | `string` | **Sí** | Nombre libre de la materia (1 a 100 caracteres). |
| `descripcion` | `string` o `null` | No | Detalles adicionales de la tarea. Se puede omitir o enviar `null`. |
| `fecha_entrega` | `string (ISO 8601)` | **Sí** | Fecha y hora límite en formato `YYYY-MM-DDTHH:MM:SS`. |
| `estado` | `string` | No | Por defecto es `"pendiente"`. Valores permitidos: `"pendiente"`, `"completada"`. |

### Ejemplo de Body a enviar (Caso completo):
```json
{
  "titulo": "Exposición de Arquitectura Limpia",
  "materia": "Ingeniería de Software",
  "descripcion": "Preparar diapositivas sobre los principios SOLID aplicados en FastAPI.",
  "fecha_entrega": "2026-11-05T14:30:00",
  "estado": "pendiente"
}
```

### Ejemplo de Body mínimo (Omitiendo campos opcionales o con valor por defecto):
```json
{
  "titulo": "Resolver ejercicios de integrales",
  "materia": "Cálculo Integral",
  "fecha_entrega": "2026-11-02T23:59:00"
}
```

### Respuesta exitosa (`201 Created`):
```json
{
  "titulo": "Exposición de Arquitectura Limpia",
  "materia": "Ingeniería de Software",
  "descripcion": "Preparar diapositivas sobre los principios SOLID aplicados en FastAPI.",
  "fecha_entrega": "2026-11-05T14:30:00",
  "estado": "pendiente",
  "id": 5,
  "created_at": "2026-10-29T22:15:00.123456",
  "vencida": false
}
```

---

## 2. Consultar y filtrar tareas (`READ`)

Se utiliza en la **Pantalla 2 (Mis tareas)** para listar las tarjetas y aplicar los filtros («Todas», «Pendientes» y «Completadas»). Las tareas se devuelven ordenadas por fecha de entrega de la más próxima a la más lejana.

* **Método:** `GET`
* **Ruta:** `/api/v1/tasks/`
* **¿Requiere Body?:** **No**

### Cómo usar los filtros (Query Params):
* **Filtro «Todas»:** `GET /api/v1/tasks/`
* **Filtro «Pendientes»:** `GET /api/v1/tasks/?estado=pendiente`
* **Filtro «Completadas»:** `GET /api/v1/tasks/?estado=completada`

### Respuesta exitosa (`200 OK`):
> 💡 **Nota para Android:** Usa la propiedad booleana `"vencida"` que devuelve cada objeto para mostrar u ocultar la etiqueta visual de **Tarea vencida** en la tarjeta.

```json
[
  {
    "titulo": "Entregar reporte de requerimientos",
    "materia": "Ingeniería de Software",
    "descripcion": "Subir PDF con los apartados 1 al 4 del contexto del proyecto.",
    "fecha_entrega": "2026-10-27T18:00:00",
    "estado": "pendiente",
    "id": 3,
    "created_at": "2026-10-25T10:00:00",
    "vencida": true
  },
  {
    "titulo": "Conectar API REST con Retrofit/Ktor",
    "materia": "Desarrollo Móvil",
    "descripcion": "Implementar las peticiones HTTP asíncronas para el CRUD de TaskFlow.",
    "fecha_entrega": "2026-10-31T14:00:00",
    "estado": "pendiente",
    "id": 1,
    "created_at": "2026-10-29T12:00:00",
    "vencida": false
  }
]
```

---

## 3. Consultar la próxima entrega (`READ`)

Se utiliza en la **Pantalla 1 (Inicio)** para llenar la tarjeta de **«Próxima entrega»**. Devuelve únicamente la tarea con estado `"pendiente"` cuya fecha de entrega sea la más cercana.

* **Método:** `GET`
* **Ruta:** `/api/v1/tasks/proxima-entrega`
* **¿Requiere Body?:** **No**

### Respuesta exitosa (`200 OK`):
* Si existen tareas pendientes, devuelve un objeto JSON con la tarea más cercana:
```json
{
  "titulo": "Conectar API REST con Retrofit/Ktor",
  "materia": "Desarrollo Móvil",
  "descripcion": "Implementar las peticiones HTTP asíncronas para el CRUD de TaskFlow.",
  "fecha_entrega": "2026-10-31T14:00:00",
  "estado": "pendiente",
  "id": 1,
  "created_at": "2026-10-29T12:00:00",
  "vencida": false
}
```
* Si el estudiante no tiene ninguna tarea pendiente, devuelve `null` (con código `200 OK`), para que en la app Android puedas mostrar un mensaje como *"¡Todo al día! No tienes entregas pendientes"*.

---

## 4. Consultar detalle de una tarea (`READ`)

Se utiliza al abrir la **Pantalla 4 (Detalle de tarea)** al tocar una tarjeta de la lista.

* **Método:** `GET`
* **Ruta:** `/api/v1/tasks/{task_id}` *(Ejemplo: `/api/v1/tasks/1`)*
* **¿Requiere Body?:** **No**

### Respuesta exitosa (`200 OK`):
```json
{
  "titulo": "Conectar API REST con Retrofit/Ktor",
  "materia": "Desarrollo Móvil",
  "descripcion": "Implementar las peticiones HTTP asíncronas para el CRUD de TaskFlow.",
  "fecha_entrega": "2026-10-31T14:00:00",
  "estado": "pendiente",
  "id": 1,
  "created_at": "2026-10-29T12:00:00",
  "vencida": false
}
```

---

## 5. Editar una tarea o cambiar su estado (`UPDATE`)

Se utiliza en la **Pantalla 3 (Modo Editar tarea)** cuando el usuario modifica los campos del formulario, o bien para cambiar su estado. Todos los campos en este `PUT` son opcionales: puedes enviar el objeto completo desde el formulario o solo los campos que cambiaron.

* **Método:** `PUT`
* **Ruta:** `/api/v1/tasks/{task_id}` *(Ejemplo: `/api/v1/tasks/1`)*
* **¿Requiere Body?:** **Sí (JSON)**

### Caso A — Body al guardar el formulario de "Editar tarea" (Pantalla 3):
```json
{
  "titulo": "Conectar API REST con Retrofit y Coroutines",
  "materia": "Desarrollo Móvil Android",
  "descripcion": "Implementar las peticiones HTTP asíncronas y manejo de errores.",
  "fecha_entrega": "2026-11-01T18:00:00",
  "estado": "pendiente"
}
```

### Caso B — Body si solo quieres cambiar el estado a completada en esta misma ruta:
```json
{
  "estado": "completada"
}
```

### Respuesta exitosa (`200 OK`):
Devuelve la tarea actualizada (observa que si pasa a `"completada"`, `"vencida"` siempre será `false`):
```json
{
  "titulo": "Conectar API REST con Retrofit y Coroutines",
  "materia": "Desarrollo Móvil Android",
  "descripcion": "Implementar las peticiones HTTP asíncronas y manejo de errores.",
  "fecha_entrega": "2026-11-01T18:00:00",
  "estado": "completada",
  "id": 1,
  "created_at": "2026-10-29T12:00:00",
  "vencida": false
}
```

---

## 6. Marcar como completada con un toque (`UPDATE` directo)

Atajo diseñado específicamente para el botón **«Marcar como completada»** de la **Pantalla 4 (Detalle de tarea)**, evitando que tengas que construir un Body JSON en Android.

* **Método:** `PUT`
* **Ruta:** `/api/v1/tasks/{task_id}/completar` *(Ejemplo: `/api/v1/tasks/1/completar`)*
* **¿Requiere Body?:** **No**

### Respuesta exitosa (`200 OK`):
```json
{
  "titulo": "Conectar API REST con Retrofit/Ktor",
  "materia": "Desarrollo Móvil",
  "descripcion": "Implementar las peticiones HTTP asíncronas para el CRUD de TaskFlow.",
  "fecha_entrega": "2026-10-31T14:00:00",
  "estado": "completada",
  "id": 1,
  "created_at": "2026-10-29T12:00:00",
  "vencida": false
}
```

---

## 7. Eliminar una tarea (`DELETE`)

Se ejecuta en la **Pantalla 4 (Detalle de tarea)** después de que el estudiante acepta el cuadro de diálogo de confirmación de eliminación.

* **Método:** `DELETE`
* **Ruta:** `/api/v1/tasks/{task_id}` *(Ejemplo: `/api/v1/tasks/1`)*
* **¿Requiere Body?:** **No**

### Respuesta exitosa (`204 No Content`):
No devuelve cuerpo de respuesta (indica que la tarea fue borrada correctamente de SQLite).

---

## ⚠️ Códigos de Respuesta y Errores Comunes

| Código HTTP | Significado | Cuándo ocurre |
| :---: | :--- | :--- |
| `200 OK` | Éxito | La consulta (`GET`) o edición (`PUT`) se realizó correctamente. |
| `201 Created` | Creado | La tarea se registró con éxito mediante `POST`. |
| `204 No Content` | Eliminado | La tarea se eliminó con éxito mediante `DELETE`. |
| `404 Not Found` | No encontrado | Se intentó consultar, editar o eliminar un `task_id` que no existe en la base de datos. |
| `422 Unprocessable Entity` | Error de validación | Falta un campo obligatorio en el Body (`titulo`, `materia`, `fecha_entrega`), el formato de fecha no es válido o el `estado` no es `"pendiente"` ni `"completada"`. |