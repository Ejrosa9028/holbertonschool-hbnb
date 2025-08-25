from repositories.sqlalchemy_repository import SQLAlchemyRepository
from business_logic.models.place import Place
from persistence.database import db

class PlaceRepository(SQLAlchemyRepository):
    """Place-specific repository"""
    
    def __init__(self):
        super().__init__(Place)
    
    def get_by_owner(self, owner_id: str):
        """Get places by owner"""
        try:
            return db.session.execute(
                db.select(Place).where(Place.owner_id == owner_id)
            ).scalars().all()
        except Exception as e:
            raise Exception(f"Error getting places by owner: {str(e)}")
