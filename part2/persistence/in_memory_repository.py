from business_logic.models.user import User
from business_logic.models.place import Place
from business_logic.models.review import Review
from business_logic.models.amenity import Amenity

class InMemoryRepository:
    def __init__(self):
        # Diccionario con todas las entidades
        self.data = {
            "users": {},
            "places": {},
            "reviews": {},
            "amenities": {}
        }

    def save(self, collection, key, value):
        """Guarda o actualiza un elemento en una colección"""
        self.data.setdefault(collection, {})  # Crea la colección si no existe
        self.data[collection][key] = value

    def get(self, collection, key):
        """Recupera un elemento de una colección"""
        return self.data.get(collection, {}).get(key)

    def get_all(self, collection):
        """Recupera todos los elementos de una colección"""
        return list(self.data.get(collection, {}).values())

    def delete(self, collection, key):
        """Elimina un elemento de una colección"""
        if key in self.data.get(collection, {}):
            del self.data[collection][key]
            return True
        return False

# Singleton para usar el repositorio en toda la app
in_memory_repo = InMemoryRepository()


