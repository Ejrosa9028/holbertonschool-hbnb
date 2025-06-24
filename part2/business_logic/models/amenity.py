from .base_model import BaseModel

class Amenity(BaseModel):
    """Represents an amenity available in a place (e.g., Wi-Fi, Pool, Gym)."""
    
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
