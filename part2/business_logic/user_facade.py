from business_logic.user_service import UserService

class UserFacade:
    def __init__(self):
        self.user_service = UserService()

    def create_user(self, email, password, first_name="", last_name=""):
        """Crea un nuevo usuario y lo retorna."""
        return self.user_service.create_user(email, password, first_name, last_name)

    def get_user_by_id(self, user_id):
        """Obtiene un usuario por su ID."""
        return self.user_service.get_user_by_id(user_id)

    def get_all_users(self):
        """Obtiene todos los usuarios registrados."""
        return self.user_service.get_all_users()

    def update_user(self, user_id, **kwargs):
        """Actualiza los datos de un usuario."""
        return self.user_service.update_user(user_id, **kwargs)

    def delete_user(self, user_id):
        """Elimina un usuario por su ID."""
        return self.user_service.delete_user(user_id)
