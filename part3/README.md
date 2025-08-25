# HBnB Part 3 - RESTful API with JWT Authentication and SQLAlchemy

## 📋 Descripción

Esta es la **Parte 3** del proyecto HBnB (Holberton Airbnb Clone), donde implementamos una API REST completa con autenticación JWT y persistencia de datos usando SQLAlchemy. El proyecto evoluciona de un sistema de almacenamiento en memoria a una base de datos robusta con autenticación de usuarios.

## 🏗️ Arquitectura

El proyecto sigue una arquitectura de capas bien definida:

```
├── api/                    # Capa de Presentación (API REST)
│   ├── app.py             # Configuración principal de Flask
│   ├── config.py          # Configuraciones del entorno
│   └── routes/            # Endpoints de la API
├── business_logic/        # Lógica de Negocio
│   ├── facades/           # Patrón Facade para servicios
│   ├── services/          # Servicios de negocio
│   └── models/            # Modelos de datos
├── persistence/           # Capa de Persistencia
│   └── database.py        # Configuración de SQLAlchemy
├── repositories/          # Patrón Repository
└── tests/                # Pruebas automatizadas
```

## 🚀 Características Principales

### ✅ Implementadas en Part 3

- **🔐 Autenticación JWT**: Login/registro de usuarios con tokens seguros
- **🗄️ Base de Datos SQLAlchemy**: Persistencia con SQLite/PostgreSQL
- **👤 Gestión de Usuarios**: CRUD completo con validaciones
- **🏠 Lugares**: Creación y gestión de propiedades
- **⭐ Reseñas**: Sistema de calificaciones y comentarios
- **🎯 Amenidades**: Gestión de características de lugares
- **🔒 Autorización**: Control de acceso basado en roles
- **📚 Documentación Swagger**: API autodocumentada
- **🧪 Testing**: Suite completa de pruebas automatizadas

## 🛠️ Tecnologías Utilizadas

- **Flask**: Framework web minimalista
- **Flask-RESTX**: Extensión para APIs REST + Swagger
- **Flask-JWT-Extended**: Manejo de tokens JWT
- **SQLAlchemy**: ORM para base de datos
- **Flask-SQLAlchemy**: Integración Flask + SQLAlchemy
- **Flask-Bcrypt**: Hashing seguro de contraseñas
- **SQLite/PostgreSQL**: Base de datos
- **pytest**: Framework de testing

## 📦 Instalación y Configuración

### Prerrequisitos

- Python 3.11+
- pip
- virtualenv (recomendado)

### Pasos de Instalación

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd holbertonschool-hbnb/part3
```

2. **Crear entorno virtual**:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno** (opcional):
```bash
# Crear archivo .env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///hbnb.db
FLASK_ENV=development
```

5. **Inicializar la base de datos**:
```bash
python scripts/init_db.py
```

6. **Ejecutar la aplicación**:
```bash
python run.py
```

La API estará disponible en: `http://localhost:5000`

## 🔧 Configuración de Entornos

### Development
```python
FLASK_ENV=development
DEBUG=True
SQLALCHEMY_DATABASE_URI=sqlite:///hbnb.db
```

### Testing
```python
FLASK_ENV=testing
TESTING=True
SQLALCHEMY_DATABASE_URI=sqlite:///:memory:
```

### Production
```python
FLASK_ENV=production
DEBUG=False
SQLALCHEMY_DATABASE_URI=postgresql://user:pass@localhost/hbnb
```

## 🌐 Endpoints de la API

### 🔐 Autenticación (`/api/v1/auth/`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/register` | Registrar nuevo usuario |
| POST | `/login` | Iniciar sesión |
| GET | `/protected` | Endpoint protegido (requiere token) |

### 👤 Usuarios (`/api/v1/users/`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/` | Listar todos los usuarios | No |
| GET | `/{id}` | Obtener usuario específico | No |
| PUT | `/{id}` | Actualizar usuario | Sí (propio perfil) |

### 🏠 Lugares (`/api/v1/places/`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/` | Listar lugares | No |
| POST | `/` | Crear lugar | Sí |
| GET | `/{id}` | Obtener lugar específico | No |
| PUT | `/{id}` | Actualizar lugar | Sí (propietario) |

### ⭐ Reseñas (`/api/v1/reviews/`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/` | Listar reseñas | No |
| POST | `/` | Crear reseña | Sí |
| GET | `/{id}` | Obtener reseña específica | No |
| PUT | `/{id}` | Actualizar reseña | Sí (autor) |
| DELETE | `/{id}` | Eliminar reseña | Sí (autor) |

### 🎯 Amenidades (`/api/v1/amenities/`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/` | Listar amenidades | No |
| POST | `/` | Crear amenidad | Sí (admin) |
| GET | `/{id}` | Obtener amenidad específica | No |
| PUT | `/{id}` | Actualizar amenidad | Sí (admin) |

## 🔒 Autenticación

### Registro de Usuario
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe", 
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### Usar Token
```bash
curl -X GET http://localhost:5000/api/v1/auth/protected \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## 🗄️ Modelos de Datos

### User
```python
- id: str (UUID)
- first_name: str (max 50)
- last_name: str (max 50)
- email: str (unique, max 120)
- password: str (hashed)
- is_admin: bool
- created_at: datetime
- updated_at: datetime
```

### Place
```python
- id: str (UUID)
- title: str (max 100)
- description: str
- price: float
- latitude: float
- longitude: float
- owner_id: str (FK -> User)
- amenities: List[Amenity]
- created_at: datetime
- updated_at: datetime
```

### Review
```python
- id: str (UUID)
- text: str
- rating: int (1-5)
- user_id: str (FK -> User)
- place_id: str (FK -> Place)
- created_at: datetime
- updated_at: datetime
```

### Amenity
```python
- id: str (UUID)
- name: str (unique, max 50)
- created_at: datetime
- updated_at: datetime
```

## 🧪 Testing

### Ejecutar todas las pruebas
```bash
pytest tests/ -v
```

### Ejecutar pruebas específicas
```bash
pytest tests/test_api.py -v
pytest tests/test_services.py -v
pytest tests/test_facades.py -v
```

### Ejecutar con coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

### Estructura de Tests
```
tests/
├── test_api.py          # Pruebas de endpoints
├── test_facades.py      # Pruebas de facades
├── test_services.py     # Pruebas de servicios
├── test_places.py       # Pruebas específicas de lugares
├── test_reviews.py      # Pruebas específicas de reseñas
├── test_users.py        # Pruebas específicas de usuarios
└── test_repository.py   # Pruebas de repositorios
```

## 📚 Documentación

### Swagger UI
Accede a la documentación interactiva en:
```
http://localhost:5000/api/v1/doc/
```

### Postman Collection
Importa la colección de Postman incluida en `docs/postman_collection.json`

## 🔍 Validaciones Implementadas

### Usuario
- ✅ Email formato válido y único
- ✅ Contraseña mínimo 6 caracteres
- ✅ Nombres no vacíos (max 50 caracteres)

### Lugar
- ✅ Título requerido (max 100 caracteres)
- ✅ Precio debe ser positivo
- ✅ Coordenadas válidas (-90 a 90 lat, -180 a 180 lng)
- ✅ Propietario debe existir

### Reseña
- ✅ Calificación entre 1 y 5
- ✅ Texto no vacío
- ✅ Usuario no puede reseñar su propio lugar
- ✅ Usuario solo puede tener una reseña por lugar

## 🛡️ Seguridad

### Implementaciones de Seguridad
- 🔐 **Hashing de contraseñas**: Bcrypt con salt
- 🎫 **JWT Tokens**: Expiración configurable
- 🚫 **Validación de entrada**: Sanitización de datos
- 🔒 **Autorización**: Control de acceso basado en roles
- 🛡️ **CORS**: Configurado para producción

### Headers de Seguridad
```python
- Content-Security-Policy
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
```

## 🚀 Despliegue

### Docker (Recomendado)
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

### Variables de Entorno para Producción
```bash
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-key
DATABASE_URL=postgresql://user:password@host:port/database
```

## 🐛 Debugging y Logs

### Activar logs detallados
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Logs de desarrollo
```bash
python run.py --debug
```

## 📈 Mejoras Futuras

### Part 4 (Próximas características)
- 🎨 **Frontend Web**: Interface de usuario completa
- 📱 **API Mobile**: Endpoints optimizados para móviles
- 🔍 **Búsqueda Avanzada**: Filtros y geolocalización
- 📊 **Analytics**: Dashboard de métricas
- 💳 **Sistema de Pagos**: Integración con Stripe
- 📧 **Notificaciones**: Email y push notifications
- 🌐 **Internacionalización**: Soporte multi-idioma
- ☁️ **Cloud Storage**: Imágenes en AWS S3
- 📱 **Aplicación Móvil**: React Native/Flutter

## 🤝 Contribución

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver archivo [LICENSE.md](LICENSE.md) para detalles.

## 👤 Autor

- **Emanuel Rosa Alamo** - *Desarrollador Principal* - [@Ejrosa9028](https://github.com/Ejrosa9028)

## 🙏 Agradecimientos

- Holberton School por la estructura del proyecto
- Flask y SQLAlchemy communities
- Todos los contribuidores del proyecto

---

⭐ **¿Te gusta el proyecto? ¡Dale una estrella!**

📧 **Contacto**: ejrosa9028@gmail.com