from business_logic.models.user import User
from repositories.user_repository import UserRepository

class UserService:
    """Service class for user-related business logic"""
    
    def __init__(self, bcrypt=None):
        self.bcrypt = bcrypt
        self.repository = UserRepository()
    
    @staticmethod
    def set_bcrypt(bcrypt):
        """Set the bcrypt instance for the service"""
        UserService.bcrypt = bcrypt
    
    @classmethod
    def create_user(cls, user_data):
        """Create a new user"""
        repository = UserRepository()
        
        # Check if email already exists
        existing_user = repository.get_by_email(user_data.get('email', ''))
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create new user
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            password=user_data.get('password'),
            is_admin=user_data.get('is_admin', False)
        )
        
        # Hash password after creation
        if cls.bcrypt:
            user.hash_password(user_data.get('password'), cls.bcrypt)
        
        return repository.add(user)
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get a user by ID"""
        repository = UserRepository()
        return repository.get(user_id)
    
    @staticmethod
    def get_user_by_email(email):
        """Get a user by email"""
        repository = UserRepository()
        return repository.get_by_email(email)
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        repository = UserRepository()
        return repository.get_all()
    
    @classmethod
    def update_user(cls, user_id, user_data):
        """Update a user"""
        repository = UserRepository()
        user = repository.get(user_id)
        if not user:
            return None
        
        # Check if email is being changed and if new email already exists
        if 'email' in user_data and user_data['email'].lower() != user.email:
            existing_user = repository.get_by_email(user_data['email'])
            if existing_user:
                raise ValueError("User with this email already exists")
        
        # Hash password if provided
        if 'password' in user_data and cls.bcrypt:
            plain_password = user_data['password']
            user.update(**user_data)
            user.hash_password(plain_password, cls.bcrypt)
        else:
            user.update(**user_data)
        
        return repository.update(user)
    
    @classmethod
    def authenticate_user(cls, email, password):
        """Authenticate a user by email and password"""
        user = cls.get_user_by_email(email)
        if user and cls.bcrypt and user.check_password(password, cls.bcrypt):
            return user
        return None
