from user import db, User  # Importamos la base de datos y el modelo de usuario

class UserRepository:

    @staticmethod
    def get_all_users():
        return User.query.all()  # Obtenemos todos los usuarios desde la base de datos

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)  # Obtenemos un usuario por su ID
    
    @staticmethod
    def get_user_by_field(field_name, value):
        # Usa `filter` en lugar de `filter_by` para poder especificar el campo dinámicamente
        user = User.query.filter(getattr(User, field_name) == value).all()  # Filtramos usuarios por un campo específico
        return user
    
    @staticmethod
    def create_user(name, username, email, password, updated_at, image, rol):
        new_user = User(name=name, username=username,email=email, password=password, updated_at=updated_at, image=image, rol=rol)
        db.session.add(new_user)  # Agregamos el nuevo usuario a la sesión de la base de datos
        db.session.commit()  # Guardamos los cambios en la base de datos
        return new_user

    @staticmethod
    def update_user(user_id,name=None, username=None, password=None):
        user = User.query.get(user_id)  # Obtenemos el usuario por su ID
        if user:
            if name:
                user.name = name  # Actualizamos el nombre si se proporciona
            if username:
                user.username = username  # Actualizamos el username si se proporciona
            if password:
                user.password = password  # Actualizamos la contraseña si se proporciona
            db.session.commit()  # Guardamos los cambios en la base de datos
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)  # Obtenemos el usuario por su ID
        if user:
            db.session.delete(user)  # Eliminamos el usuario
            db.session.commit()  # Guardamos los cambios en la base de datos
        return user
    
    @staticmethod
    def authenticate_user(username, password):
        # Realiza la consulta para encontrar al usuario con el username y password proporcionados
        return User.query.filter_by(username=username, password=password).first()  # Autenticamos al usuario
