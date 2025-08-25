import re
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from business_logic.models.base_model import BaseModel

class User(BaseModel):
    """User model class with SQLAlchemy mapping"""
    
    __tablename__ = 'users'
    
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships (will be defined after other models are created)
    places = relationship("Place", back_populates="owner", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.email = self._validate_email(email)
        self.password = self._validate_password(password)
        self.is_admin = is_admin
    
    def _validate_name(self, name, field_name):
        """Validate name fields"""
        if not name or not isinstance(name, str):
            raise ValueError(f"{field_name} is required and must be a string")
        if len(name.strip()) == 0:
            raise ValueError(f"{field_name} cannot be empty")
        if len(name) > 50:
            raise ValueError(f"{field_name} cannot exceed 50 characters")
        return name.strip()
    
    def _validate_email(self, email):
        """Validate email format"""
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
        return email.lower()
    
    def _validate_password(self, password):
        """Validate password requirements"""
        if not password or not isinstance(password, str):
            raise ValueError("Password is required and must be a string")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return password
    
    def hash_password(self, password, bcrypt):
        """Hash the password using bcrypt"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password, bcrypt):
        """Check if provided password matches the hashed password"""
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self):
        """Convert user to dictionary, excluding password"""
        user_dict = super().to_dict()
        user_dict.pop('password', None)
        user_dict['places'] = [place.id for place in self.places] if self.places else []
        user_dict['reviews'] = [review.id for review in self.reviews] if self.reviews else []
        return user_dict
    
    def update(self, **kwargs):
        """Update user attributes with validation"""
        if 'first_name' in kwargs:
            kwargs['first_name'] = self._validate_name(kwargs['first_name'], "First name")
        if 'last_name' in kwargs:
            kwargs['last_name'] = self._validate_name(kwargs['last_name'], "Last name")
        if 'email' in kwargs:
            kwargs['email'] = self._validate_email(kwargs['email'])
        if 'password' in kwargs:
            kwargs['password'] = self._validate_password(kwargs['password'])
        
        # Remove fields that shouldn't be updated directly
        kwargs.pop('id', None)
        kwargs.pop('created_at', None)
        kwargs.pop('places', None)
        kwargs.pop('reviews', None)
        
        super().update(**kwargs)
