import uuid
from datetime import datetime

class BaseModel:
    """Base class for all models, providing common attributes and methods."""
    
    def __init__(self, id=None, created_at=None, updated_at=None):
        self.id = id if id else str(uuid.uuid4())  # Genera un UUID si no se proporciona
        self.created_at = created_at if created_at else datetime.utcnow()
        self.updated_at = updated_at if updated_at else datetime.utcnow()

    def save(self):
        """Updates the `updated_at` timestamp to the current time."""
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Returns a dictionary representation of the instance."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    def __str__(self):
        """Returns a string representation of the object."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.to_dict()}"

