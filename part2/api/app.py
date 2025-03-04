#!/usr/bin/python3 
from flask import Flask
from flask_restx import Api
from api.routes.user_routes import user_ns
from api.routes.place_routes import place_ns
from api.routes.review_routes import review_ns


app = Flask(__name__)
api = Api(app)

api.add_namespace(user_ns, path="/users")
api.add_namespace(place_ns, path="/places")
api.add_namespace(review_ns, path="/reviews")

if __name__ == "__main__":
    app.run(debug=True)

class InMemoryRepository:
    """Repositorio en memoria para almacenar objetos de forma temporal."""
    
    def __init__(self):
        self.data = {}  # Diccionario para almacenar objetos
        self.next_id = 1  # Simulación de ID incremental

    def create(self, obj):
        """Agrega un nuevo objeto al repositorio."""
        obj_id = self.next_id
        obj["id"] = obj_id  # Asignar un ID único
        self.data[obj_id] = obj
        self.next_id += 1
        return obj

    def get(self, obj_id):
        """Obtiene un objeto por su ID."""
        return self.data.get(obj_id)

    def get_all(self):
        """Retorna todos los objetos almacenados."""
        return list(self.data.values())

    def update(self, obj_id, updates):
        """Actualiza un objeto existente con nuevos valores."""
        if obj_id in self.data:
            self.data[obj_id].update(updates)
            return self.data[obj_id]
        return None

    def delete(self, obj_id):
        """Elimina un objeto por su ID."""
        return self.data.pop(obj_id, None)


# Repositorios específicos para cada entidad
class UserRepository(InMemoryRepository):
    """Repositorio específico para usuarios."""
    pass

class PlaceRepository(InMemoryRepository):
    """Repositorio específico para lugares."""
    pass

class ReviewRepository(InMemoryRepository):
    """Repositorio específico para reseñas."""
    pass


# Instancias globales de los repositorios (se usarán en otros módulos)
user_repository = UserRepository()
place_repository = PlaceRepository()
review_repository = ReviewRepository()

print("Rutas registradas en la API:")
for rule in app.url_map.iter_rules():
    print(rule)
