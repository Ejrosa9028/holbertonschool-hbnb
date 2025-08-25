import uuid
from datetime import datetime
from persistence.database import db
from business_logic.models.user import User
from business_logic.models.amenity import Amenity
from flask import current_app
from sqlalchemy import inspect

def create_initial_data():
    """Create initial data for the database"""
    
    try:
        # Check if tables exist first
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'users' not in tables or 'amenities' not in tables:
            print("⏳ Tables don't exist yet, skipping initial data creation")
            return
        
        # Check if admin user already exists
        admin_email = "admin@hbnb.com"
        existing_admin = db.session.execute(
            db.select(User).where(User.email == admin_email)
        ).scalar_one_or_none()
        
        if not existing_admin:
            # Create admin user
            admin_user = User(
                first_name="Admin",
                last_name="HBnB", 
                email=admin_email,
                password="admin123",  # This will be hashed below
                is_admin=True
            )
            
            # Hash password
            from flask_bcrypt import Bcrypt
            bcrypt = Bcrypt(current_app)
            admin_user.hash_password("admin123", bcrypt)
            
            db.session.add(admin_user)
            print("✅ Admin user created")
        else:
            print("ℹ️  Admin user already exists")
        
        # Create basic amenities if they don't exist
        basic_amenities = [
            "WiFi",
            "Air Conditioning", 
            "Swimming Pool",
            "Gym",
            "Parking",
            "Pet Friendly",
            "Kitchen",
            "Washing Machine",
            "TV",
            "Balcony"
        ]
        
        amenities_created = 0
        for amenity_name in basic_amenities:
            existing_amenity = db.session.execute(
                db.select(Amenity).where(Amenity.name == amenity_name)
            ).scalar_one_or_none()
            
            if not existing_amenity:
                amenity = Amenity(name=amenity_name)
                db.session.add(amenity)
                amenities_created += 1
        
        if amenities_created > 0:
            print(f"✅ {amenities_created} amenities created")
        else:
            print("ℹ️  All amenities already exist")
        
        db.session.commit()
        print("✅ Initial data creation completed successfully")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating initial data: {e}")
        # Don't re-raise the exception to prevent app startup failure
        return
