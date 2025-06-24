from .base_model import BaseModel

class User(BaseModel):
    """Represents a user in the HBnB application."""
    
    def __init__(self, email="", password="", first_name="", last_name="", **kwargs):
        """Initializes a User object."""
        super().__init__(**kwargs)  # BaseModel maneja el ID y timestamps
        self.email = kwargs.get("email", email)
        self.password = kwargs.get("password", password)  # Agregar hashing más adelante
        self.first_name = kwargs.get("first_name", first_name)
        self.last_name = kwargs.get("last_name", last_name)

    def __str__(self):
        """String representation of a User."""
        return f"User({self.id}, {self.email}, {self.first_name} {self.last_name})"
