# 🌐 HBnB - Parte 2: API RESTful

Este repositorio contiene la segunda parte del proyecto HBnB, centrada en la creación de una API RESTful modular utilizando Flask. La API permite gestionar entidades como `users`, `places` y `reviews` mediante operaciones CRUD.

---

## 📌 Tecnologías Utilizadas

- **Python 3**
- **Flask** (`Blueprint`, `Flask-RESTx`)
- **Estructura modular por rutas**
- **Patrón Fachada (Facade Pattern)**
- **Repositorio en memoria (simulación de base de datos)**

---

## 📁 Estructura de Carpetas

part2/
<br>
│
<br>
├── api/
<br>
│ ├── app.py # Punto de entrada principal
<br>
│ ├── config.py # Configuración de la aplicación
<br>
│ └── routes/ # Rutas REST (users, places, reviews)
<br>
│
<br>
├── business_logic/
<br>
│ ├── models/ # Entidades: User, Place, Review, Amenity
<br>
│ ├── *_service.py # Lógica de servicios por entidad
<br>
│ └── *_facade.py # Fachadas para simplificar acceso a servicios
<br>
│
<br>
├── persistence/
<br>
│ └── in_memory_repository.py # Repositorio simulado
<br>
│
<br>
└── tests/ # Tests unitarios
<br>

---

## 📬 Endpoints Disponibles

| Método | Ruta                         | Descripción                |
|--------|------------------------------|----------------------------|
| GET    | `/users`                     | Listar todos los usuarios  |
| GET    | `/users/<user_id>`           | Obtener un usuario         |
| POST   | `/users`                     | Crear usuario              |
| PUT    | `/users/<user_id>`           | Actualizar usuario         |
| GET    | `/places`                    | Listar todos los lugares   |
| POST   | `/places`                    | Crear nuevo lugar          |
| PUT    | `/places/<place_id>`         | Actualizar lugar           |
| GET    | `/reviews/places/<place_id>` | Ver reseñas por lugar      |
| POST   | `/reviews`                   | Crear reseña               |
| GET    | `/reviews/<review_id>`       | Obtener una reseña         |
| PUT    | `/reviews/<review_id>`       | Actualizar reseña          |

---

## 🧪 Cómo Probar la API

1. Activa el entorno virtual:
```bash
source venv/bin/activate
```

2. Ejecuta el servidor:
```bash
python3 -m api.app
```

3. Usa herramientas como curl para consumir la API:
```bash

# Obtener todos los usuarios
curl -X GET http://127.0.0.1:5000/users

# Crear un nuevo lugar
curl -X POST http://127.0.0.1:5000/places \
     -H "Content-Type: application/json" \
     -d '{"title": "Casa bonita", "price": 100}'
```

---

## 👤 Autor
- **Emanuel Rosa Alamo** - Estudiante de Holberton School