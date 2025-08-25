from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from business_logic.user_facade import user_facade

# Create namespace
user_ns = Namespace('users', description='User operations')

# Define input model for user creation by admin
admin_user_model = user_ns.model('AdminUserCreate', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password'),
    'is_admin': fields.Boolean(required=False, default=False, description='Admin status')
})

# Define input model for user updates (restricted fields)
user_update_model = user_ns.model('UserUpdate', {
    'first_name': fields.String(required=False, description='User first name'),
    'last_name': fields.String(required=False, description='User last name')
})

# Define input model for admin user updates (includes all fields)
admin_user_update_model = user_ns.model('AdminUserUpdate', {
    'first_name': fields.String(required=False, description='User first name'),
    'last_name': fields.String(required=False, description='User last name'),
    'email': fields.String(required=False, description='User email address'),
    'password': fields.String(required=False, description='User password'),
    'is_admin': fields.Boolean(required=False, description='Admin status')
})

# Add security definitions
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    },
}

user_ns.authorizations = authorizations

@user_ns.route('/')
class UserList(Resource):
    @user_ns.doc('list_users')
    def get(self):
        """Retrieve all users (public endpoint)"""
        try:
            users = user_facade.get_all_users()
            return [user.to_dict() for user in users], 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    @user_ns.expect(admin_user_model)
    @user_ns.doc('create_user_admin', security='Bearer Auth')
    def post(self):
        """Create a new user (admin only)"""
        try:
            # Get current user claims from JWT
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Check if user is admin
            if not is_admin:
                return {'error': 'Only administrators can create users through this endpoint'}, 403
            
            user_data = request.json
            user = user_facade.create_user(user_data)
            return {
                'message': 'User created successfully by administrator',
                'user': user.to_dict()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

@user_ns.route('/<string:user_id>')
@user_ns.param('user_id', 'The user identifier')
class User(Resource):
    @user_ns.doc('get_user')
    def get(self, user_id):
        """Retrieve a user by ID (public endpoint)"""
        try:
            user = user_facade.get_user(user_id)
            if user:
                return user.to_dict(), 200
            return {'error': 'User not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    @user_ns.doc('update_user', security='Bearer Auth')
    def put(self, user_id):
        """Update a user (own profile or admin can update any)"""
        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Validate user exists
            user = user_facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            
            user_data = request.json
            
            if is_admin:
                # Admin can update any user with full privileges
                # Use admin model that allows all fields
                updated_user = user_facade.update_user(user_id, user_data)
                return {
                    'message': 'User updated by administrator',
                    'user': updated_user.to_dict()
                }, 200
            else:
                # Regular user can only update their own profile with restricted fields
                if current_user_id != user_id:
                    return {'error': 'You can only update your own profile'}, 403
                
                # Remove restricted fields for non-admin users
                restricted_fields = ['email', 'password', 'is_admin']
                for field in restricted_fields:
                    if field in user_data:
                        user_data.pop(field)
                
                if not user_data:
                    return {'error': 'No valid fields to update'}, 400
                
                updated_user = user_facade.update_user(user_id, user_data)
                return updated_user.to_dict(), 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500
