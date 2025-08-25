from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Float, ForeignKey, Table, Column
from business_logic.models.base_model import BaseModel

# Association table for many-to-many relationship between places and amenities
# Fixed for SQLAlchemy 2.0 - use Column instead of mapped_column for association tables
place_amenities = Table(
    'place_amenities',
    BaseModel.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Place model class with SQLAlchemy mapping"""
    
    __tablename__ = 'places'
    
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    owner_id: Mapped[str] = mapped_column(String(60), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="places")
    amenities = relationship("Amenity", secondary=place_amenities, back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = self._validate_title(title)
        self.description = self._validate_description(description)
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner = owner
        self.owner_id = owner.id
    
    def _validate_title(self, title):
        """Validate place title"""
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        if len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        return title.strip()
    
    def _validate_description(self, description):
        """Validate place description"""
        if description is not None and not isinstance(description, str):
            raise ValueError("Description must be a string")
        if description and len(description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")
        return description.strip() if description else ""
    
    def _validate_price(self, price):
        """Validate place price"""
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        return float(price)
    
    def _validate_latitude(self, latitude):
        """Validate latitude"""
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")
        return float(latitude)
    
    def _validate_longitude(self, longitude):
        """Validate longitude"""
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be between -180 and 180")
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return float(longitude)
    
    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
    
    def remove_amenity(self, amenity):
        """Remove an amenity from the place"""
        if amenity in self.amenities:
            self.amenities.remove(amenity)
    
    def add_review(self, review):
        """Add a review to the place"""
        if review not in self.reviews:
            self.reviews.append(review)
    
    def remove_review(self, review):
        """Remove a review from the place"""
        if review in self.reviews:
            self.reviews.remove(review)
    
    def to_dict(self):
        """Convert place to dictionary"""
        place_dict = super().to_dict()
        place_dict['owner'] = {
            'id': self.owner.id,
            'first_name': self.owner.first_name,
            'last_name': self.owner.last_name,
            'email': self.owner.email
        } if self.owner else None
        place_dict['amenities'] = [
            {'id': amenity.id, 'name': amenity.name} 
            for amenity in self.amenities
        ] if self.amenities else []
        place_dict['reviews'] = [review.id for review in self.reviews] if self.reviews else []
        return place_dict
    
    def update(self, **kwargs):
        """Update place attributes with validation"""
        if 'title' in kwargs:
            kwargs['title'] = self._validate_title(kwargs['title'])
        if 'description' in kwargs:
            kwargs['description'] = self._validate_description(kwargs['description'])
        if 'price' in kwargs:
            kwargs['price'] = self._validate_price(kwargs['price'])
        if 'latitude' in kwargs:
            kwargs['latitude'] = self._validate_latitude(kwargs['latitude'])
        if 'longitude' in kwargs:
            kwargs['longitude'] = self._validate_longitude(kwargs['longitude'])
        
        # Remove fields that shouldn't be updated directly
        kwargs.pop('id', None)
        kwargs.pop('created_at', None)
        kwargs.pop('owner', None)
        kwargs.pop('owner_id', None)
        kwargs.pop('amenities', None)
        kwargs.pop('reviews', None)
        
        super().update(**kwargs)
