import business_logic.place_service  # Importación diferida
from persistence.in_memory_repository import InMemoryRepository

class PlaceFacade:
    def __init__(self):
        from business_logic.place_service import PlaceService
        self.place_service = PlaceService()

    def get_all_places(self):
        return self.service.get_all_places()

    def get_place_by_id(self, place_id):
        return self.service.get_place_by_id(place_id)

    def create_place(self, data):
        return self.service.create_place(data)

    def update_place(self, place_id, data):
        return self.service.update_place(place_id, data)
