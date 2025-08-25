from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from business_logic.review_facade import review_facade

# Create namespace
review_ns = Namespace('reviews', description='Review operations')

# Define input model for review creation
review_model = review_ns.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID')
})

# Define input model for review updates
review_update_model = review_ns.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Review text'),
    'rating': fields.Integer(required=False, description='Rating (1-5)')
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

review_ns.authorizations = authorizations


@review_ns.route('/')
class ReviewList(Resource):
    @review_ns.doc('list_reviews')
    def get(self):
        """Retrieve all reviews (public endpoint)"""
        try:
            reviews = review_facade.get_all_reviews()
            return [review.to_dict() for review in reviews], 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    @review_ns.expect(review_model)
    @review_ns.doc('create_review', security='Bearer Auth')
    def post(self):
        """Create a new review (authenticated users only)"""
        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            
            review_data = request.json
            # Set the user_id to the current authenticated user
            review_data['user_id'] = current_user_id
            
            review = review_facade.create_review(review_data)
            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500


@review_ns.route('/<string:review_id>')
@review_ns.param('review_id', 'The review identifier')
class Review(Resource):
    @review_ns.doc('get_review')
    def get(self, review_id):
        """Retrieve a review by ID (public endpoint)"""
        try:
            review = review_facade.get_review(review_id)
            if review:
                return review.to_dict(), 200
            return {'error': 'Review not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    @review_ns.expect(review_update_model)
    @review_ns.doc('update_review', security='Bearer Auth')
    def put(self, review_id):
        """Update a review (only by author or admin)"""
        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Get the review to check ownership
            review = review_facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            
            # Check if user is the author or an admin
            if review.user.id != current_user_id and not is_admin:
                return {'error': 'You can only update reviews you created'}, 403
            
            review_data = request.json
            updated_review = review_facade.update_review(review_id, review_data)
            if updated_review:
                return updated_review.to_dict(), 200
            return {'error': 'Review not found'}, 404
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500
    
    @jwt_required()
    @review_ns.doc('delete_review', security='Bearer Auth')
    def delete(self, review_id):
        """Delete a review (only by author or admin)"""
        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Get the review to check ownership
            review = review_facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            
            # Check if user is the author or an admin
            if review.user.id != current_user_id and not is_admin:
                return {'error': 'You can only delete reviews you created'}, 403
            
            deleted_review = review_facade.delete_review(review_id)
            if deleted_review:
                return {'message': 'Review deleted successfully'}, 200
            return {'error': 'Review not found'}, 404
            
        except Exception as e:
            return {'error': str(e)}, 500


@review_ns.route('/places/<string:place_id>')
@review_ns.param('place_id', 'The place identifier')
class PlaceReviews(Resource):
    @review_ns.doc('get_place_reviews')
    def get(self, place_id):
        """Retrieve all reviews for a specific place (public endpoint)"""
        try:
            reviews = review_facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200
        except Exception as e:
            return {'error': str(e)}, 500
