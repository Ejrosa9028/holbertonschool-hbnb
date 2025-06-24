from flask import request
from flask_restx import Namespace, Resource
from business_logic.user_service import UserService

user_ns = Namespace("users", description="User operations")

@user_ns.route("/")
class UserList(Resource):
    def get(self):
        """Retrieve all users"""
        return [user.to_dict() for user in UserService.get_all_users()]

    def post(self):
        """Create a new user"""
        data = request.json
        user = UserService.create_user(data["first_name"], data["last_name"], data["email"])
        return user.to_dict(), 201

@user_ns.route("/<string:user_id>")
class UserResource(Resource):
    def get(self, user_id):
        """Retrieve a user by ID (excluding password)"""
        user = UserService.get_user_by_id(user_id)
        if user:
            return user, 200
        return {"message": "User not found"}, 404

    def put(self, user_id):
        """Update a user's details"""
        data = request.json
        updated_user = UserService.update_user(user_id, data)
        if updated_user:
            return updated_user, 200
        return {"message": "User not found"}, 404
    
class UserService:
    def get_user_by_id(self, user_id):
        # Código para obtener el usuario
        pass
