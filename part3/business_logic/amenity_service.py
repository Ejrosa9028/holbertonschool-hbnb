from business_logic.models.amenity import Amenity
from repositories.amenity_repository import AmenityRepository

class AmenityService:
    """Service class for amenity-related business logic"""
    
    @staticmethod
    def create_amenity(amenity_data):
        """Create a new amenity"""
        repository = AmenityRepository()
        
        # Check if amenity with same name already exists
        existing_amenity = repository.get_by_name(amenity_data.get('name', ''))
        if existing_amenity:
            raise ValueError("Amenity with this name already exists")
        
        # Create new amenity
        amenity = Amenity(name=amenity_data.get('name'))
        return repository.add(amenity)
    
    @staticmethod
    def get_amenity_by_id(amenity_id):
        """Get an amenity by ID"""
        repository = AmenityRepository()
        return repository.get(amenity_id)
    
    @staticmethod
    def get_all_amenities():
        """Get all amenities"""
        repository = AmenityRepository()
        return repository.get_all()
    
    @staticmethod
    def update_amenity(amenity_id, amenity_data):
        """Update an amenity"""
        repository = AmenityRepository()
        amenity = repository.get(amenity_id)
        if not amenity:
            return None
        
        # Check if name is being changed and if new name already exists
        if 'name' in amenity_data and amenity_data['name'].strip() != amenity.name:
            existing_amenity = repository.get_by_name(amenity_data['name'])
            if existing_amenity:
                raise ValueError("Amenity with this name already exists")
        
        # Update amenity
        amenity.update(**amenity_data)
        return repository.update(amenity)
