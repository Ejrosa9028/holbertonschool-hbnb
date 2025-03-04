from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, user_id, place_id, text):
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self.text = text
