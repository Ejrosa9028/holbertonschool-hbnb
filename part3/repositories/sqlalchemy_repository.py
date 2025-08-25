from sqlalchemy.exc import SQLAlchemyError
from persistence.database import db
from typing import Optional, List, Any

class SQLAlchemyRepository:
    """SQLAlchemy-based repository for database persistence"""
    
    def __init__(self, model_class):
        self.model = model_class
    
    def add(self, obj) -> Any:
        """Add an object to the database"""
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error adding {self.model.__name__}: {str(e)}")
    
    def get(self, obj_id: str) -> Optional[Any]:
        """Get an object by ID"""
        try:
            return db.session.get(self.model, obj_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error getting {self.model.__name__}: {str(e)}")
    
    def get_all(self) -> List[Any]:
        """Get all objects of this type"""
        try:
            return db.session.execute(
                db.select(self.model)
            ).scalars().all()
        except SQLAlchemyError as e:
            raise Exception(f"Error getting all {self.model.__name__}: {str(e)}")
    
    def update(self, obj) -> Optional[Any]:
        """Update an object in the database"""
        try:
            db.session.commit()
            return obj
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error updating {self.model.__name__}: {str(e)}")
    
    def delete(self, obj_id: str) -> bool:
        """Delete an object from the database"""
        try:
            obj = self.get(obj_id)
            if obj:
                db.session.delete(obj)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error deleting {self.model.__name__}: {str(e)}")
    
    def get_by_attribute(self, attribute: str, value: Any) -> List[Any]:
        """Get objects by a specific attribute value"""
        try:
            return db.session.execute(
                db.select(self.model).where(getattr(self.model, attribute) == value)
            ).scalars().all()
        except SQLAlchemyError as e:
            raise Exception(f"Error getting {self.model.__name__} by {attribute}: {str(e)}")
