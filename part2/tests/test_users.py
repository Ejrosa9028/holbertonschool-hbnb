import unittest
from business_logic.user_service import UserService

class TestUserService(unittest.TestCase):
    def setUp(self):
        """Set up before each test"""
        self.user_service = UserService()

    def test_create_user(self):
        """Test user creation"""
        user = self.user_service.create_user("John Doe", "john@example.com")
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, "John Doe")

    def test_get_user_not_found(self):
        """Test fetching a non-existent user"""
        user = self.user_service.get_user_by_id("invalid_id")
        self.assertIsNone(user)

if __name__ == "__main__":
    unittest.main()
