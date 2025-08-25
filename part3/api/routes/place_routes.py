from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from business_logic.place_facade import place_facade

# Create namespace
place_ns = Namespace('places', description='Place operations')

# Define input model for place creation
place_model = place_ns.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(required=False, description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'amenities': fields.List(fields.String, required=False, description='List of amenity IDs')
})

# Define input model for place updates
place_update_model = place_ns.model('PlaceUpdate', {
    'title': fields.String(required=False, description='Place title'),
    'description': fields.String(required=False, description='Place description'),
    'price': fields.Float(required=False, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude coordinate'),
    'longitude': fields.Float(required=False, description='Longitude coordinate'),
    'amenities': fields.List(fields.String, required=False, description='List of amenity IDs')
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

place_ns.authorizations = authorizations


@place_ns.route('/')
class PlaceList(Resource):
    @place_ns.doc('list_places')
    def get(self):
        """Retrieve all places (public endpoint)"""
        try:
            places = place_facade.get_all_places()
            return [place.to_dict() for place in places], 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    @place_ns.expect(place_model)
    @place_ns.doc('create_place', security='Bearer Auth')
    def post(self):
        """Create a new place (authenticated users only)"""
        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            
            place_data = request.json
            # Set the owner_id to the current authenticated user
            place_data['owner_id'] = current_user_id
            
            place = place_facade.create_place(place_data)
            return place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500


@place_ns.route('/<string:place_id>')
@place_ns.param('place_id', 'The place identifier')
class Place(Resource):
    @place_ns.doc('get_place')
    def get(self, place_id):
        """Retrieve a place by ID (public endpoint)"""
        try:
            place = place_facade.get_place(place_id)
            if place:
                return place.to_dict(), 200
            return {'error': 'Place not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    @place_ns.expect(place_update_model)
    @place_ns.doc('update_place', security='Bearer Auth')
    def put(self, place_id):
        """Update a place (only by owner or admin)"""
        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Get the place to check ownership
            place = place_facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            # Check if user is the owner or an admin
            if place.owner.id != current_user_id and not is_admin:
                return {'error': 'You can only update places you own'}, 403
            
            place_data = request.json
            updated_place = place_facade.update_place(place_id, place_data)
            if updated_place:
                return updated_place.to_dict(), 200
            return {'error': 'Place not found'}, 404
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500
