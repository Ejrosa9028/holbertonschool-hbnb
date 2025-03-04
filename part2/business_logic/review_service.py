import datetime
from persistence.in_memory_repository import in_memory_repo  # Usar singleton
from business_logic.models.review import Review

class ReviewService:
    def __init__(self):
        self.review_repo = in_memory_repo  # Usar el repositorio compartido

    def create_review(self, user_id, place_id, text):
        """Crea un nuevo review y lo almacena en el repositorio"""
        if not text.strip():
            raise ValueError("El texto del review no puede estar vacío")

        review = Review(user_id, place_id, text)
        self.review_repo.save("reviews", review.id, review)  # Guardar en la colección "reviews"
        return review

    def get_review_by_id(self, review_id):
        """Obtiene un review por su ID"""
        review = self.review_repo.get("reviews", review_id)
        if not review:
            raise ValueError("Review no encontrado")
        return review

    def get_reviews_by_place(self, place_id):
        """Obtiene todos los reviews asociados a un lugar"""
        reviews = self.review_repo.get_all("reviews")  # Obtener todos los reviews
        return [review for review in reviews if review.place_id == place_id]

    def update_review(self, review_id, new_text):
        """Actualiza el texto de un review existente"""
        review = self.get_review(review_id)
        if not new_text.strip():
            raise ValueError("El texto del review no puede estar vacío")

        review.text = new_text
        review.updated_at = datetime.datetime.utcnow()
        self.review_repo.save("reviews", review.id, review)  # Guardar cambios
        return review

    def delete_review(self, review_id):
        """Elimina un review del repositorio y retorna si se eliminó o no"""
        return self.review_repo.delete("reviews", review_id)  # Retornar resultado de eliminación
