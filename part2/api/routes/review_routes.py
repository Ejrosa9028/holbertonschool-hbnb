from flask import request
from flask_restx import Namespace, Resource
from business_logic.review_facade import ReviewFacade

review_ns = Namespace("reviews", description="Review operations")

@review_ns.route("/")
class ReviewList(Resource):
    def post(self):
        """Create a new review"""
        data = request.json
        user_id = data.get("user_id")
        place_id = data.get("place_id")
        text = data.get("text")

        if not user_id or not place_id or not text:
            return {"error": "Missing user_id, place_id, or text"}, 400

        try:
            review = ReviewFacade.create_review(user_id, place_id, text)
            return {"message": "Review created successfully", "review": review.id}, 201
        except ValueError as e:
            return {"error": str(e)}, 400


@review_ns.route("/<string:review_id>")
class ReviewResource(Resource):
    def get(self, review_id):
        """Get a review by ID"""
        review = ReviewFacade.get_review_by_id(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return {
            "id": review.id,
            "user_id": review.user_id,
            "place_id": review.place_id,
            "text": review.text
        }, 200

    def put(self, review_id):
        """Update a review"""
        data = request.json
        new_text = data.get("text")

        if not new_text:
            return {"error": "Text cannot be empty"}, 400

        updated_review = ReviewFacade.update_review(review_id, new_text)
        if not updated_review:
            return {"error": "Review not found"}, 404

        return {"message": "Review updated successfully", "review": updated_review.id}, 200

    def delete(self, review_id):
        """Delete a review"""
        success = ReviewFacade.delete_review(review_id)
        if not success:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200


@review_ns.route("/places/<string:place_id>")
class ReviewsByPlace(Resource):
    def get(self, place_id):
        """Get all reviews for a place"""
        reviews = ReviewFacade.get_reviews_by_place(place_id)
        if not reviews:
            return {"message": "No reviews found for this place"}, 404

        return [
            {"id": review.id, "user_id": review.user_id, "text": review.text}
            for review in reviews
        ], 200