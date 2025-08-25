from business_logic.amenity_service import AmenityService


class AmenityFacade:
    """Facade for amenity-related operations"""
    
    def __init__(self):
        self.amenity_service = AmenityService
    
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        return self.amenity_service.create_amenity(amenity_data)
    
    def get_amenity(self, amenity_id):
        """Get an amenity by ID"""
        return self.amenity_service.get_amenity_by_id(amenity_id)
    
    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_service.get_all_amenities()
    
    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        return self.amenity_service.update_amenity(amenity_id, amenity_data)


# Global facade instance
amenity_facade = AmenityFacade()
