from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from business_logic.user_facade import user_facade

# Create namespace
auth_ns = Namespace('auth', description='Authentication operations')

# Define input models
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

register_model = auth_ns.model('Register', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'is_admin': fields.Boolean(required=False, default=False, description='Admin status')
})


@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.doc('register_user')
    def post(self):
        """Register a new user"""
        try:
            user_data = request.json
            user = user_facade.create_user(user_data)
            
            # Create access token using user ID instead of user object  
            access_token = create_access_token(identity=user.id)
            
            return {
                'message': 'User registered successfully',
                'access_token': access_token,
                'user': user.to_dict()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.doc('login_user')
    def post(self):
        """Login user and return access token"""
        try:
            credentials = request.json
            email = credentials.get('email')
            password = credentials.get('password')
            
            if not email or not password:
                return {'error': 'Email and password are required'}, 400
            
            # Authenticate user
            user = user_facade.authenticate_user(email, password)
            
            if user:
                # Create tokens using user ID
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
                
                return {
                    'message': 'Login successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': user.to_dict()
                }, 200
            else:
                return {'error': 'Invalid email or password'}, 401
        
        except Exception as e:
            return {'error': str(e)}, 500


@auth_ns.route('/protected')
class Protected(Resource):
    @jwt_required()
    @auth_ns.doc('protected_endpoint', security='Bearer Auth')
    def get(self):
        """Test protected endpoint - requires valid JWT token"""
        try:
            current_user_id = get_jwt_identity()
            user = user_facade.get_user(current_user_id)
            
            if user:
                return {
                    'message': f'Hello {user.first_name}! This is a protected endpoint.',
                    'user_id': current_user_id,
                    'user': user.to_dict()
                }, 200
            else:
                return {'error': 'User not found'}, 404
        
        except Exception as e:
            return {'error': str(e)}, 500


# Add security definitions for Swagger documentation
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    },
}
auth_ns.authorizations = authorizations
