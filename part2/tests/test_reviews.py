import unittest
from business_logic.review_service import ReviewService

class TestReviewService(unittest.TestCase):
    def setUp(self):
        self.review_service = ReviewService()

    def test_create_review(self):
        """Test review creation"""
        review = self.review_service.create_review("user123", "place456", "Amazing place!")
        self.assertIsNotNone(review)
        self.assertEqual(review.text, "Amazing place!")

    def test_get_review_not_found(self):
        """Test fetching a non-existent review"""
        with self.assertRaises(ValueError):  # Verifica que se lanza la excepción
            self.review_service.get_review_by_id("invalid_id")

if __name__ == "__main__":
    unittest.main()
