from persistence.in_memory_repository import InMemoryRepository
from business_logic.models.place import Place
import uuid  # Para generar un ID único si no viene en data

class PlaceService:
    def __init__(self):
        self.repository = InMemoryRepository()

    def create_place(self, name, city, owner_id, price=0, latitude=None, longitude=None):
        """Crea un lugar con los parámetros correctos"""

        # Validaciones
        if price < 0:
            raise ValueError("Price cannot be negative")
        if latitude is not None and not (-90 <= latitude <= 90):
            raise ValueError("Invalid latitude value")
        if longitude is not None and not (-180 <= longitude <= 180):
            raise ValueError("Invalid longitude value")

        # Creación del objeto Place
        place_data = {
            "id": str(uuid.uuid4()),  # Genera un ID único
            "name": name,
            "city": city,
            "owner_id": owner_id,
            "price": price,
            "latitude": latitude,
            "longitude": longitude,
        }
        place = Place(**place_data)

        # Guardar en el repositorio
        self.repository.save("places", place.id, place)
        return place

    def get_all_places(self):
        """Obtiene todos los lugares"""
        return self.repository.get_all("places")

    def get_place_by_id(self, place_id):
        """Obtiene un lugar por su ID"""
        return self.repository.get("places", place_id)

    def update_place(self, place_id, data):
        """Actualiza un lugar"""
        return self.repository.update("places", place_id, data)
