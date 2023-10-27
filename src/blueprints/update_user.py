from flask import Blueprint, jsonify, request
import re

update_user_bp = Blueprint("update_user", __name__)

@update_user_bp.route("/users/<session_token>", methods=["PUT"])
def update_user(session_token):
    try:
        patron_invalido = re.compile(r'[^a-zA-Z0-9-_]+$')
        patron_correo_valido = re.compile(r'^[\w\.-]+@[\w\.-]+(\.\w+)+$')

        if request.json["username"] == "" or request.json["email"] == "" or request.json["user_password"] == "":
            return jsonify({"Error": "Todos los campos son necesarios"}), 500

        if type(request.json["username"]) != str or type(request.json["email"]) != str or type(request.json["user_password"]) != str:
            return jsonify({"Error": "Los datos solo pueden ser texto"}), 500
        
        if len(request.json["username"]) > 50 or len(request.json["email"]) > 254 or len(request.json["user_password"]) > 50:
            return jsonify({"Error": "Longitud de datos superada"}), 500
        
        if patron_invalido.search(request.json["username"]) or patron_invalido.search(request.json["user_password"]):
            return jsonify({"Error": "No se aceptan caracteres especiales"}), 500
        
        if not patron_correo_valido.search(request.json["email"]):
            return jsonify({"Error": "Formato de correo invalido"}), 500
        
        if not secure_password(request.json["user_password"]):
            return jsonify({"Error": "La contraseña debe contener una minuscula, una mayuscula y 6 caracteres"}), 500
        

        from app import mysqlconnection
        cursor = mysqlconnection.connection.cursor()

        # BUSCAR EL ID DEL USUARIO
        query = f"SELECT id_user FROM users WHERE session_token = {session_token}"
        cursor.execute(query)
        data = cursor.fetchone()
        user_id = data[0]

        # EJECUTAR ACTUALIZACION
        query = f"UPDATE users SET username = '{request.json['username']}', email = '{request.json['email']}', user_password = '{request.json['user_password']}' WHERE id_user = {user_id}"
        cursor.execute(query)
        mysqlconnection.connection.commit()
        return jsonify({"Message": "Datos actualizados con exito"})
    
    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500
    
def secure_password(user_password):
    if len(user_password) < 6:
        return False
    tiene_mayuscula = False
    tiene_minuscula = False
    for caracter in user_password:
        if caracter.isupper():
            tiene_mayuscula = True
        elif caracter.islower():
            tiene_minuscula = True
    return (tiene_mayuscula and tiene_minuscula)