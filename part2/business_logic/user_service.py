import uuid
from persistence.in_memory_repository import in_memory_repo
from business_logic.models.user import User
from persistence.in_memory_repository import in_memory_repo  # Singleton

class UserService:
    def __init__(self):
        self.user_repo = in_memory_repo  # Usar el repositorio compartido

    def create_user(self, email, password, first_name="", last_name=""):
        """Crea un nuevo usuario y lo almacena en el repositorio."""
        user = User(email=email, password=password, first_name=first_name, last_name=last_name)
        self.user_repo.save("users", user.id, user)  # Guarda el objeto User, no un dict
        return user  # Devolver el objeto User en lugar de un dict

    def get_user_by_id(self, user_id):
        """Obtiene un usuario por su ID."""
        user = self.user_repo.get("users", user_id)
        if not user:
            return None  # Si no existe, retornar None en lugar de lanzar error
        return user  # Asegurar que se devuelve un objeto User, no un dict

    def delete_user(self, user_id):
        """Elimina un usuario del repositorio."""
        return self.user_repo.delete("users", user_id)
