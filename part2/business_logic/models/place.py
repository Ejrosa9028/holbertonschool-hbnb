from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, id, name, city, owner_id, price=0, latitude=0.0, longitude=0.0, amenities=None):
        super().__init__(id)
        self.id = id
        self.name = name
        self.city = city
        self.owner_id = owner_id
        self.price = max(0, price)  # Evita precios negativos
        self.latitude = latitude if latitude is not None else 0.0  # Evita problemas con None
        self.longitude = longitude if longitude is not None else 0.0
        self.amenities = amenities if amenities is not None else []  # Evita listas compartidas entre instancias

    def __str__(self):
        """Devuelve una representación en string del objeto"""
        return f"Place({self.id}, {self.name}, {self.city}, Owner: {self.owner_id}, ${self.price}, Coordinates: ({self.latitude}, {self.longitude}))"

