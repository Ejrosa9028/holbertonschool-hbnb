from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from business_logic.models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity model class with SQLAlchemy mapping"""
    
    __tablename__ = 'amenities'
    
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    # Many-to-many relationship with places
    places = relationship("Place", secondary="place_amenities", back_populates="amenities")
    
    def __init__(self, name):
        super().__init__()
        self.name = self._validate_name(name)
    
    def _validate_name(self, name):
        """Validate amenity name"""
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string")
        if len(name.strip()) == 0:
            raise ValueError("Amenity name cannot be empty")
        if len(name) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters")
        return name.strip()
    
    def update(self, **kwargs):
        """Update amenity attributes with validation"""
        if 'name' in kwargs:
            kwargs['name'] = self._validate_name(kwargs['name'])
        
        # Remove fields that shouldn't be updated directly
        kwargs.pop('id', None)
        kwargs.pop('created_at', None)
        
        super().update(**kwargs)
