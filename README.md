# lab08 - Servicios Web REST con Django y Django REST Framework

API REST desarrollada con Django 6 y Django REST Framework (DRF) correspondiente al Laboratorio 08 del curso Desarrollo de Aplicaciones Web / Empresariales (TECSUP).

## Arquitectura del proyecto

```text
lab08/
├── lab08/
│   ├── settings.py         # Configuracion Django, DRF, media y zona horaria
│   └── urls.py             # Enrutador raiz (series, tienda, admin, media)
├── series/
│   ├── models.py           # Modelo Serie (horror, comedy, action, drama)
│   ├── serializers.py      # SerieSerializer (ModelSerializer)
│   ├── views.py            # IndexView, SeriesView, SerieDetailView (APIView)
│   ├── urls.py             # / , /serie , /serie/<int:serie_id>
│   └── tests.py            # Pruebas de integracion CRUD (APITestCase)
├── tienda/
│   ├── models.py           # Modelos Categoria y Producto (integracion Lab 06)
│   ├── serializers.py      # CategoriaSerializer y ProductoSerializer
│   ├── views.py            # Vistas genericas DRF + endpoints con BasicAuthentication
│   ├── urls.py             # /tienda/categorias/, /tienda/productos/, /tienda/auth/*
│   └── tests.py            # Pruebas de vistas genericas y Basic Auth (401/200)
├── poblar_datos.py         # Carga idempotente de superusuario y datos iniciales
├── manage.py
└── requirements.txt
```

## Requisitos y ejecucion local

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python poblar_datos.py
python manage.py runserver 127.0.0.1:8000
```

## Endpoints expuestos

### Modulo `series` (`APIView`)

| Metodo | Endpoint | Descripcion |
| :--- | :--- | :--- |
| `GET` | `/` | Verificacion de estado del servicio (`{"mensaje": "servidor activo"}`). |
| `GET` | `/serie` | Lista todas las series registradas. |
| `POST` | `/serie` | Crea una nueva serie (`201 Created`). |
| `GET` | `/serie/<int:serie_id>` | Obtiene el detalle de una serie por clave primaria (`404` si no existe). |
| `PUT` | `/serie/<int:serie_id>` | Actualiza integramente una serie existente. |
| `DELETE` | `/serie/<int:serie_id>` | Elimina una serie y retorna los datos del registro removido. |

### Modulo `tienda` (`Generic Views` + `BasicAuthentication`)

| Metodo | Endpoint | Clase DRF | Descripcion |
| :--- | :--- | :--- | :--- |
| `GET`, `POST` | `/tienda/categorias/` | `ListCreateAPIView` | Listado y creacion de categorias. |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/tienda/categorias/<int:pk>/` | `RetrieveUpdateDestroyAPIView` | Operaciones por registro de categoria. |
| `GET`, `POST` | `/tienda/productos/` | `ListCreateAPIView` | Listado (`select_related`) y registro de productos. |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/tienda/productos/<int:pk>/` | `RetrieveUpdateDestroyAPIView` | Operaciones por registro de producto. |
| `GET`, `POST` | `/tienda/auth/productos/` | `ListCreateAPIView` + `BasicAuthentication` | Endpoint protegido (`IsAuthenticated`). |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/tienda/auth/productos/<int:pk>/` | `RetrieveUpdateDestroyAPIView` + `BasicAuthentication` | Detalle/edicion protegidos con Basic Auth. |
| `GET` | `/tienda/auth/status/` | `APIView` + `BasicAuthentication` | Valida credenciales enviadas por HTTP Basic Auth. |

## Pruebas automatizadas

```bash
python manage.py test
```

Valida el ciclo completo `GET/POST/PUT/DELETE` en `series`, la serializacion y creacion sobre vistas genericas en `tienda`, y el rechazo (`401 Unauthorized`) frente a la autorizacion (`200 OK`) en los endpoints protegidos con `BasicAuthentication`.
