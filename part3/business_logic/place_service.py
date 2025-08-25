from business_logic.models.place import Place
from repositories.place_repository import PlaceRepository
from repositories.user_repository import UserRepository
from repositories.amenity_repository import AmenityRepository

class PlaceService:
    """Service class for place-related business logic"""
    
    @staticmethod
    def create_place(place_data):
        """Create a new place"""
        place_repo = PlaceRepository()
        user_repo = UserRepository()
        amenity_repo = AmenityRepository()
        
        # Get owner
        owner_id = place_data.get('owner_id')
        owner = user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        
        # Create new place
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description', ''),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner
        )
        
        # Add amenities if provided
        amenity_ids = place_data.get('amenities', [])
        for amenity_id in amenity_ids:
            amenity = amenity_repo.get(amenity_id)
            if amenity:
                place.add_amenity(amenity)
        
        return place_repo.add(place)
    
    @staticmethod
    def get_place_by_id(place_id):
        """Get a place by ID"""
        repository = PlaceRepository()
        return repository.get(place_id)
    
    @staticmethod
    def get_all_places():
        """Get all places"""
        repository = PlaceRepository()
        return repository.get_all()
    
    @staticmethod
    def update_place(place_id, place_data):
        """Update a place"""
        place_repo = PlaceRepository()
        amenity_repo = AmenityRepository()
        
        place = place_repo.get(place_id)
        if not place:
            return None
        
        # Handle amenities update
        if 'amenities' in place_data:
            amenity_ids = place_data.pop('amenities')
            # Clear current amenities
            place.amenities.clear()
            # Add new amenities
            for amenity_id in amenity_ids:
                amenity = amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)
        
        # Update place
        place.update(**place_data)
        return place_repo.update(place)
