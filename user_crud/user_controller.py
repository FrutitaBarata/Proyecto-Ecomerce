from flask_restful import Api, Resource  # Importamos Api y Resource para crear recursos RESTful
from user_repository import UserRepository  # Importamos el repositorio de usuarios para manejar las operaciones con la base de datos
from user_service import UserService  # Importamos el servicio de usuario para aplicar lógica de negocio
from flask import Flask, app, request, jsonify, render_template  # Importamos Flask y herramientas para manejar solicitudes y respuestas en formato JSON
from user import User

def create_api(app):
    api = Api(app)  # Inicializamos la API con la aplicación Flask

    # Recurso para manejar la autenticación de usuarios
    class LoginResource(Resource):
        def post(self):
            data = app.request.get_json()  # Obtenemos los datos JSON de la solicitud
            username = data.get('username')
            password = data.get('password')
        
            user = UserService.authenticate_user(username, password)  # Llamamos al servicio de autenticación
        
            if user:
                return {
                "message": "Usuario válido",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "email": user.email,
                    "updated_at": user.updated_at,
                    "image": user.image,
                    "rol": user.rol
                }
            }, 200  # Retornamos el usuario en caso de éxito
            else:
                return {"message": "Credenciales inválidas, null"}, 401  # Retornamos un error de autenticación

    # Recurso para manejar la creación y obtención de usuarios
    class UserResource(Resource):
        def get(self):
            users = UserRepository.get_all_users()  # Obtenemos todos los usuarios
            return [user.to_dict() for user in users]  # Serializar cada usuario

        def post(self):
            data = app.request.get_json()  # Obtenemos los datos JSON de la solicitud
            new_user = UserRepository.create_user(data['name'], data['username'],data['email'], data['password'], data['updated_at'],
            data['image'], data['rol'])  # Creamos un nuevo usuario
            return {"id": new_user.id,"name":new_user.name, "username": new_user.username,"email":new_user.email,
            "updated_at":new_user.updated_at, "image":new_user.image, "rol":new_user.rol}  # Retornamos el nuevo usuario

    # Recurso para manejar operaciones sobre un único usuario identificado por su ID
    class SingleUserResource(Resource):
        def get(self, user_id):
            user = UserRepository.get_user_by_id(user_id)  # Obtenemos un usuario por su ID
            if user is None:
                return {"message": "User not found"}, 404  # Retornamos error si no se encuentra
            return {"id": user.id, "username": user.username}  # Retornamos los detalles del usuario
        
        def put(self, user_id):
            data = app.request.get_json()  # Obtenemos los datos JSON de la solicitud
            user = UserRepository.update_user(user_id, data.get('username'), data.get('password'))  # Actualizamos el usuario
            if user is None:
                return {"message": "User not found"}, 404  # Retornamos error si no se encuentra
            return {"id": user.id,"name":user.name, "username": user.username,"email":user.email,
            "updated_at":user.updated_at, "image":user.image, "rol":user.rol}  # Retornamos los detalles del usuario actualizado

        def delete(self, user_id):
            user = UserRepository.delete_user(user_id)  # Eliminamos el usuario
            if user is None:
                return {"message": "User not found"}, 404  # Retornamos error si no se encuentra
            return {"message": "User deleted successfully"}  # Confirmamos la eliminación
        
    # Recurso para buscar usuarios por un campo específico (como nombre, username, etc.)
    class UserByFieldResource(Resource):
        def get(self, field_name, value):
            # Verificamos que el campo sea válido antes de realizar la búsqueda
            if field_name not in ['name', 'username', 'email', 'rol']:
                return {"message": "Campo inválido"}, 400  # Retornamos error si el campo no es válido
            
            users = UserService.get_user_by_field(field_name, value)  # Obtenemos los usuarios por campo
            if users:
                return [{
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "email": user.email,
                    "updated_at": user.updated_at,
                    "image": user.image,
                    "rol": user.rol
                } for user in users], 200  # Retornamos la lista de usuarios
            else:
                return {"message": "No se encontraron usuarios"}, 404  # Retornamos error si no se encuentran usuarios

    # Definimos las rutas para cada recurso
    api.add_resource(UserByFieldResource, '/users/search/<string:field_name>/<string:value>')    
    api.add_resource(UserResource, '/api/users')
    api.add_resource(SingleUserResource, '/users/<int:user_id>')
    api.add_resource(LoginResource, '/login')

    @app.route('/users', methods=['GET'])
    def users():
        return render_template('index.html')  # Renderiza la plantilla HTML
   

    return api  # Retornamos la API con las rutas configuradas
