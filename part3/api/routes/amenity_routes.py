from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from business_logic.amenity_facade import amenity_facade

# Create namespace
amenity_ns = Namespace('amenities', description='Amenity operations')

# Define input model for amenity creation
amenity_model = amenity_ns.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name')
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

amenity_ns.authorizations = authorizations

@amenity_ns.route('/')
class AmenityList(Resource):
    @amenity_ns.doc('list_amenities')
    def get(self):
        """Retrieve all amenities (public endpoint)"""
        try:
            amenities = amenity_facade.get_all_amenities()
            return [amenity.to_dict() for amenity in amenities], 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    @amenity_ns.expect(amenity_model)
    @amenity_ns.doc('create_amenity', security='Bearer Auth')
    def post(self):
        """Create a new amenity (admin only)"""
        try:
            # Get current user claims from JWT
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Check if user is admin
            if not is_admin:
                return {'error': 'Only administrators can create amenities'}, 403
            
            amenity_data = request.json
            amenity = amenity_facade.create_amenity(amenity_data)
            return amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

@amenity_ns.route('/<string:amenity_id>')
@amenity_ns.param('amenity_id', 'The amenity identifier')
class Amenity(Resource):
    @amenity_ns.doc('get_amenity')
    def get(self, amenity_id):
        """Retrieve an amenity by ID (public endpoint)"""
        try:
            amenity = amenity_facade.get_amenity(amenity_id)
            if amenity:
                return amenity.to_dict(), 200
            return {'error': 'Amenity not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    @amenity_ns.expect(amenity_model)
    @amenity_ns.doc('update_amenity', security='Bearer Auth')
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        try:
            # Get current user claims from JWT
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Check if user is admin
            if not is_admin:
                return {'error': 'Only administrators can update amenities'}, 403
            
            amenity_data = request.json
            amenity = amenity_facade.update_amenity(amenity_id, amenity_data)
            if amenity:
                return amenity.to_dict(), 200
            return {'error': 'Amenity not found'}, 404
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500
