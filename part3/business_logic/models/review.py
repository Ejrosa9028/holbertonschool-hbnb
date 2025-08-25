from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, ForeignKey
from business_logic.models.base_model import BaseModel

class Review(BaseModel):
    """Review model class with SQLAlchemy mapping"""
    
    __tablename__ = 'reviews'
    
    text: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    place_id: Mapped[str] = mapped_column(String(60), ForeignKey('places.id'), nullable=False)
    user_id: Mapped[str] = mapped_column(String(60), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    place = relationship("Place", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place_id = place_id
        self.user_id = user_id
    
    def _validate_text(self, text):
        """Validate review text"""
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")
        if len(text.strip()) == 0:
            raise ValueError("Review text cannot be empty")
        if len(text) > 1000:
            raise ValueError("Review text cannot exceed 1000 characters")
        return text.strip()
    
    def _validate_rating(self, rating):
        """Validate review rating"""
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    def to_dict(self):
        """Convert review to dictionary"""
        review_dict = super().to_dict()
        review_dict['place'] = {
            'id': self.place.id,
            'title': self.place.title
        } if self.place else None
        review_dict['user'] = {
            'id': self.user.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name
        } if self.user else None
        return review_dict
    
    def update(self, **kwargs):
        """Update review attributes with validation"""
        if 'text' in kwargs:
            kwargs['text'] = self._validate_text(kwargs['text'])
        if 'rating' in kwargs:
            kwargs['rating'] = self._validate_rating(kwargs['rating'])
        
        # Remove fields that shouldn't be updated directly
        kwargs.pop('id', None)
        kwargs.pop('created_at', None)
        kwargs.pop('place_id', None)
        kwargs.pop('user_id', None)
        kwargs.pop('place', None)
        kwargs.pop('user', None)
        
        super().update(**kwargs)
