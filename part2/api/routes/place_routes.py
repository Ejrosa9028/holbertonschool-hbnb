from flask import request
from flask_restx import Namespace, Resource, fields
from business_logic.place_facade import PlaceFacade

# Definir el namespace para los endpoints de "places"
place_ns = Namespace('places', description="Operations related to places")

# Instanciar la fachada de lugares
place_facade = PlaceFacade()

# Definir el modelo de datos para validación y documentación en Swagger
place_model = place_ns.model('Place', {
    'id': fields.String(required=True, description='The place ID'),
    'name': fields.String(required=True, description='The name of the place'),
    'description': fields.String(description='Detailed description of the place'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'price': fields.Float(description='Price per night'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
})


@place_ns.route('/')
class PlaceList(Resource):
    @place_ns.marshal_list_with(place_model)
    def get(self):
        """Retrieve all places"""
        return place_facade.get_all_places()

    @place_ns.expect(place_model)
    @place_ns.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        data = place_ns.payload
        return place_facade.create_place(data), 201


@place_ns.route('/<string:place_id>')
class PlaceResource(Resource):
    @place_ns.marshal_with(place_model)
    def get(self, place_id):
        """Retrieve a place by its ID"""
        return place_facade.get_place_by_id(place_id)

    @place_ns.expect(place_model)
    @place_ns.marshal_with(place_model)
    def put(self, place_id):
        """Update an existing place"""
        data = place_ns.payload
        return place_facade.update_place(place_id, data)
