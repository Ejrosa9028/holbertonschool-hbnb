import os
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

# Import database
from persistence.database import db

# Import route namespaces
from api.routes.user_routes import user_ns
from api.routes.amenity_routes import amenity_ns
from api.routes.place_routes import place_ns
from api.routes.review_routes import review_ns
from api.routes.auth_routes import auth_ns

# Import config
from api.config import config

# Import services
from business_logic.user_service import UserService

# Global extensions
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_name=None):
    """Application factory function"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Set bcrypt instance for UserService
    UserService.set_bcrypt(bcrypt)
    
    # Create tables and initial data
    with app.app_context():
        try:
            print("🔧 Creating database tables...")
            
            # CRITICAL: Import all models BEFORE creating tables
            # This ensures SQLAlchemy knows about all tables to create
            from business_logic.models.user import User
            from business_logic.models.place import Place
            from business_logic.models.review import Review
            from business_logic.models.amenity import Amenity
            
            # Now create all tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Debug: Check what tables were actually created
            import sqlalchemy
            inspector = sqlalchemy.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Created tables: {tables}")
            
            # Insert initial data if needed
            print("🔧 Creating initial data...")
            try:
                from scripts.init_db import create_initial_data
                create_initial_data()
            except ImportError:
                print("⏳ Initial data script not found, skipping...")
            except Exception as e:
                print(f"⚠️ Error creating initial data: {e}")
                print("⏳ Tables don't exist yet, skipping initial data creation")
            
        except Exception as e:
            print(f"❌ Error during database initialization: {e}")
            # Continue anyway for development
    
    # Create API instance
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='A simple Airbnb-like API with JWT Authentication and SQLAlchemy',
        doc='/api/v1/doc/',
        prefix='/api/v1'
    )
    
    # Register namespaces
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(user_ns, path='/users')
    api.add_namespace(amenity_ns, path='/amenities')
    api.add_namespace(place_ns, path='/places')
    api.add_namespace(review_ns, path='/reviews')
    
    @app.route('/')
    def index():
        return {'message': 'Welcome to HBnB API with SQLAlchemy', 'version': '1.0'}, 200
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    # JWT configuration
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        """Add additional claims to JWT"""
        from business_logic.user_service import UserService
        user = UserService.get_user_by_id(identity)
        if user:
            return {
                'is_admin': user.is_admin,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        return {}
    
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        """Define what goes into the JWT token as identity"""
        return user.id
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """Load user from JWT"""
        identity = jwt_data["sub"]
        return UserService.get_user_by_id(identity)
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'error': 'Invalid token'}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'error': 'Authorization token is required'}, 401
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
