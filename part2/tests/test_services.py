import unittest
from business_logic.user_service import UserService
from business_logic.place_service import PlaceService
from business_logic.review_service import ReviewService

class TestServices(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()
        self.place_service = PlaceService()
        self.review_service = ReviewService()

    def test_create_and_get_user(self):
        user = self.user_service.create_user("Alice", "alice@example.com")
        fetched_user = self.user_service.get_user_by_id(user.id)
        self.assertEqual(fetched_user.name, "Alice")

    def test_create_and_get_place(self):
        place = self.place_service.create_place("Mountain Cabin", "Colorado")
        fetched_place = self.place_service.get_place_by_id(place.id)
        self.assertEqual(fetched_place.name, "Mountain Cabin")

    def test_create_and_get_review(self):
        review = self.review_service.create_review("user123", "place456", "Loved it!")
        fetched_review = self.review_service.get_review_by_id(review.id)
        self.assertEqual(fetched_review.text, "Loved it!")

if __name__ == "__main__":
    unittest.main()
