from business_logic.review_service import ReviewService
from business_logic.models.review import Review

class ReviewFacade:
    def __init__(self):
        self.review_service = ReviewService()  # Se instancia ReviewService

    @staticmethod
    def create_review(user_id, place_id, text):
        """Crea un review usando ReviewService"""
        return ReviewService().create_review(user_id, place_id, text)

    def get_review_by_id(self, review_id):
        """Obtiene un review por su ID"""
        return self.review_service.get_review(review_id)

    def get_reviews_by_place(self, place_id):
        """Obtiene todos los reviews de un lugar"""
        return self.review_service.get_reviews_by_place(place_id)

    def update_review(self, review_id, new_text):
        """Actualiza un review"""
        return self.review_service.update_review(review_id, new_text)

    def delete_review(self, review_id):
        """Elimina un review"""
        self.review_service.delete_review(review_id)

