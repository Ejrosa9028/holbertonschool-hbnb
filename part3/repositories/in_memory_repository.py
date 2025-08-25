from business_logic.models.user import User
from business_logic.models.place import Place
from business_logic.models.review import Review
from business_logic.models.amenity import Amenity


class InMemoryRepository:
    """In-memory storage for all entities"""
    
    def __init__(self):
        self._storage = {
            'User': {},
            'Place': {},
            'Review': {},
            'Amenity': {}
        }
    
    def add(self, obj):
        """Add an object to the repository"""
        obj_type = obj.__class__.__name__
        if obj_type in self._storage:
            self._storage[obj_type][obj.id] = obj
            return obj
        raise ValueError(f"Unknown object type: {obj_type}")
    
    def get(self, obj_type, obj_id):
        """Get an object by type and ID"""
        if obj_type in self._storage:
            return self._storage[obj_type].get(obj_id)
        return None
    
    def get_all(self, obj_type):
        """Get all objects of a specific type"""
        if obj_type in self._storage:
            return list(self._storage[obj_type].values())
        return []
    
    def update(self, obj):
        """Update an object in the repository"""
        obj_type = obj.__class__.__name__
        if obj_type in self._storage and obj.id in self._storage[obj_type]:
            self._storage[obj_type][obj.id] = obj
            return obj
        return None
    
    def delete(self, obj_type, obj_id):
        """Delete an object from the repository"""
        if obj_type in self._storage and obj_id in self._storage[obj_type]:
            deleted_obj = self._storage[obj_type].pop(obj_id)
            
            # Handle relationships when deleting
            if obj_type == 'Review':
                # Remove review from place and user
                review = deleted_obj
                if review.place:
                    review.place.remove_review(review)
                if review.user and review in review.user.reviews:
                    review.user.reviews.remove(review)
            
            return deleted_obj
        return None
    
    def get_by_attribute(self, obj_type, attribute, value):
        """Get objects by a specific attribute value"""
        if obj_type in self._storage:
            return [obj for obj in self._storage[obj_type].values() 
                   if hasattr(obj, attribute) and getattr(obj, attribute) == value]
        return []


# Global repository instance
in_memory_repo = InMemoryRepository()

