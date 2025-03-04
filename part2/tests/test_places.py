import unittest
from business_logic.place_service import PlaceService

class TestPlaceService(unittest.TestCase):
    def setUp(self):
        self.place_service = PlaceService()

    def test_create_place(self):
        """Test place creation"""
        place = self.place_service.create_place("Beach House", "Miami", "user123", price=100, latitude=25.7617, longitude=-80.1918)
        self.assertIsNotNone(place)
        self.assertEqual(place.name, "Beach House")

    def test_get_place_not_found(self):
        """Test fetching a non-existent place"""
        place = self.place_service.get_place_by_id("invalid_id")
        self.assertIsNone(place)

if __name__ == "__main__":
    unittest.main()
