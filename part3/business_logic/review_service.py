from business_logic.models.review import Review
from business_logic.place_service import PlaceService
from repositories.review_repository import ReviewRepository
from repositories.user_repository import UserRepository

class ReviewService:
    """Service class for review-related business logic"""
    
    @staticmethod
    def create_review(review_data):
        """Create a new review with validations"""
        review_repo = ReviewRepository()
        user_repo = UserRepository()
        
        place_id = review_data.get('place_id')
        user_id = review_data.get('user_id')
        
        # Validate that place exists
        place = PlaceService.get_place_by_id(place_id)
        if not place:
            raise ValueError("Place not found")
        
        # Get user
        user = user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Validate that user is not the place owner
        if place.owner.id == user_id:
            raise ValueError("You cannot review your own place")
        
        # Check if user has already reviewed this place
        existing_review = review_repo.get_by_user_and_place(user_id, place_id)
        if existing_review:
            raise ValueError("You have already reviewed this place")
        
        # Create new review
        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place_id=place_id,
            user_id=user_id
        )
        
        return review_repo.add(review)
    
    @staticmethod
    def get_review_by_id(review_id):
        """Get a review by ID"""
        repository = ReviewRepository()
        return repository.get(review_id)
    
    @staticmethod
    def get_all_reviews():
        """Get all reviews"""
        repository = ReviewRepository()
        return repository.get_all()
    
    @staticmethod
    def get_reviews_by_place(place_id):
        """Get all reviews for a place"""
        repository = ReviewRepository()
        return repository.get_by_place(place_id)
    
    @staticmethod
    def update_review(review_id, review_data):
        """Update a review"""
        repository = ReviewRepository()
        review = repository.get(review_id)
        if not review:
            return None
        
        review.update(**review_data)
        return repository.update(review)
    
    @staticmethod
    def delete_review(review_id):
        """Delete a review"""
        repository = ReviewRepository()
        return repository.delete(review_id)
