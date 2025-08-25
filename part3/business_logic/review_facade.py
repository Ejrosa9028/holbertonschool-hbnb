from business_logic.review_service import ReviewService


class ReviewFacade:
    """Facade for review-related operations"""
    
    def __init__(self):
        self.review_service = ReviewService
    
    def create_review(self, review_data):
        """Create a new review"""
        return self.review_service.create_review(review_data)
    
    def get_review(self, review_id):
        """Get a review by ID"""
        return self.review_service.get_review_by_id(review_id)
    
    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_service.get_all_reviews()
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a place"""
        return self.review_service.get_reviews_by_place(place_id)
    
    def update_review(self, review_id, review_data):
        """Update a review"""
        return self.review_service.update_review(review_id, review_data)
    
    def delete_review(self, review_id):
        """Delete a review"""
        return self.review_service.delete_review(review_id)


# Global facade instance
review_facade = ReviewFacade()
