from repositories.sqlalchemy_repository import SQLAlchemyRepository
from business_logic.models.review import Review
from persistence.database import db

class ReviewRepository(SQLAlchemyRepository):
    """Review-specific repository"""
    
    def __init__(self):
        super().__init__(Review)
    
    def get_by_place(self, place_id: str):
        """Get reviews by place"""
        try:
            return db.session.execute(
                db.select(Review).where(Review.place_id == place_id)
            ).scalars().all()
        except Exception as e:
            raise Exception(f"Error getting reviews by place: {str(e)}")
    
    def get_by_user(self, user_id: str):
        """Get reviews by user"""
        try:
            return db.session.execute(
                db.select(Review).where(Review.user_id == user_id)
            ).scalars().all()
        except Exception as e:
            raise Exception(f"Error getting reviews by user: {str(e)}")
    
    def get_by_user_and_place(self, user_id: str, place_id: str):
        """Check if user has already reviewed a place"""
        try:
            return db.session.execute(
                db.select(Review).where(
                    Review.user_id == user_id,
                    Review.place_id == place_id
                )
            ).scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error checking user place review: {str(e)}")
