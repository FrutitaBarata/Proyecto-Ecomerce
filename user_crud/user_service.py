from user_repository import UserRepository  # Importamos el repositorio de usuarios

class UserService:

    @staticmethod
    def authenticate_user(username, password):
        # Lógica adicional, como encriptación de contraseñas, puede ir aquí
        # Se delega la autenticación al repositorio de usuarios
        return UserRepository.authenticate_user(username, password)

    @staticmethod
    def get_user_by_field(field_name, value):
        # Se delega la búsqueda de usuarios por un campo específico al repositorio
        return UserRepository.get_user_by_field(field_name, value)
