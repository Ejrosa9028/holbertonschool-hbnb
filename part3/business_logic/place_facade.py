from business_logic.place_service import PlaceService


class PlaceFacade:
    """Facade for place-related operations"""
    
    def __init__(self):
        self.place_service = PlaceService
    
    def create_place(self, place_data):
        """Create a new place"""
        return self.place_service.create_place(place_data)
    
    def get_place(self, place_id):
        """Get a place by ID"""
        return self.place_service.get_place_by_id(place_id)
    
    def get_all_places(self):
        """Get all places"""
        return self.place_service.get_all_places()
    
    def update_place(self, place_id, place_data):
        """Update a place"""
        return self.place_service.update_place(place_id, place_data)


# Global facade instance
place_facade = PlaceFacade()
