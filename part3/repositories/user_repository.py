from repositories.sqlalchemy_repository import SQLAlchemyRepository
from business_logic.models.user import User
from persistence.database import db

class UserRepository(SQLAlchemyRepository):
    """User-specific repository with custom methods"""
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email: str):
        """Get a user by email"""
        try:
            return db.session.execute(
                db.select(User).where(User.email == email.lower())
            ).scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Error getting user by email: {str(e)}")
    
    def get_all_users(self):
        """Get all users"""
        return self.get_all()
