import unittest
from business_logic.review_facade import ReviewFacade

class TestReviewFacade(unittest.TestCase):
    def test_create_review_facade(self):
        """Test creating a review via facade"""
        review = ReviewFacade.create_review("user123", "place456", "Great view!")
        self.assertIsNotNone(review)
        self.assertEqual(review.text, "Great view!")

if __name__ == "__main__":
    unittest.main()
