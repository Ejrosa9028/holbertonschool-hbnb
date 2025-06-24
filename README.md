# 🏡 HBnB Evolution

HBnB Evolution es una aplicación web inspirada en AirBnB, diseñada para permitir a los usuarios registrar, buscar y gestionar propiedades, así como publicar reseñas y administrar amenidades.

---

## 🚀 Características Principales

- 📊 Visualización de entidades con **Mermaid.js**.
- 📡 **API RESTful** documentada y estructurada.

---

## 🧠 Arquitectura

- **Flask**
- **Mermaid.js**

---

## 📊 Diagrama Entidad-Relación

```mermaid
classDiagram
class User {
    +UUID id
    +String first_name
    +String last_name
    +String email
    +String password
    +Boolean is_admin
    +DateTime created_at
    +DateTime updated_at
    +register()
    +updateProfile()
    +delete()
}

class Place {
    +UUID id
    +String title
    +String description
    +Float price
    +Float latitude
    +Float longitude
    +UUID owner_id
    +List~UUID~ amenity_ids
    +DateTime created_at
    +DateTime updated_at
    +create()
    +update()
    +delete()
    +list()
}

class Review {
    +UUID id
    +UUID place_id
    +UUID user_id
    +Integer rating
    +String comment
    +DateTime created_at
    +DateTime updated_at
    +create()
    +update()
    +delete()
    +listByPlace()
}

class Amenity {
    +UUID id
    +String name
    +String description
    +DateTime created_at
    +DateTime updated_at
    +create()
    +update()
    +delete()
    +list()
}

User "1" --> "0..*" Place : owns
Place "1" --> "0..*" Review : has
User "1" --> "0..*" Review : writes
Place "0..*" --> "0..*" Amenity : has
```

---

## 👤 Autor
- **Emanuel Rosa Alamo** - Estudiante de Holberton School