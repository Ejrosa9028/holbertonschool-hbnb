from business_logic.user_service import UserService


class UserFacade:
    """Facade for user-related operations"""
    
    def __init__(self):
        self.user_service = UserService
    
    def create_user(self, user_data):
        """Create a new user"""
        return self.user_service.create_user(user_data)
    
    def get_user(self, user_id):
        """Get a user by ID"""
        return self.user_service.get_user_by_id(user_id)
    
    def get_user_by_email(self, email):
        """Get a user by email"""
        return self.user_service.get_user_by_email(email)
    
    def get_all_users(self):
        """Get all users"""
        return self.user_service.get_all_users()
    
    def update_user(self, user_id, user_data):
        """Update a user"""
        return self.user_service.update_user(user_id, user_data)
    
    def authenticate_user(self, email, password):
        """Authenticate a user"""
        return self.user_service.authenticate_user(email, password)


# Global facade instance
user_facade = UserFacade()
