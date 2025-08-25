from business_logic.models.amenity import Amenity
from repositories.in_memory_repository import in_memory_repo

class AmenityRepository:
    """Repository for Amenity objects"""
    
    def __init__(self):
        self.repo = in_memory_repo
    
    def add(self, amenity: Amenity) -> Amenity:
        """Add a new amenity"""
        return self.repo.add(amenity)
    
    def get(self, amenity_id: str) -> Amenity:
        """Get amenity by ID"""
        return self.repo.get('Amenity', amenity_id)
    
    def get_all(self) -> list:
        """Get all amenities"""
        return self.repo.get_all('Amenity')
    
    def update(self, amenity: Amenity) -> Amenity:
        """Update an amenity"""
        return self.repo.update(amenity)
    
    def delete(self, amenity_id: str) -> bool:
        """Delete an amenity"""
        return self.repo.delete('Amenity', amenity_id) is not None
    
    def get_by_name(self, name: str) -> Amenity:
        """Get amenity by name"""
        amenities = self.repo.get_by_attribute('Amenity', 'name', name)
        return amenities[0] if amenities else None
