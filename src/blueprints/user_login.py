from flask import Blueprint, jsonify, request
import re

user_login_bp = Blueprint("user_login", __name__)

@user_login_bp.route("/users/login", methods=["POST"])
def login():
    try:
        # VALIDACIONES
        patron_invalido = re.compile(r'[^a-zA-Z0-9-_]+$')
        patron_correo_valido = re.compile(r'^[\w\.-]+@[\w\.-]+(\.\w+)+$')

        if type(request.json["email"]) != str or type(request.json["user_password"]) != str:
            return jsonify({"Error": "Los datos solo pueden ser texto"})

        if request.json["email"] == "" or request.json["user_password"] == "":
            return jsonify({"Error": "Todos los campos son obligatorios"}), 400
        
        if len(request.json["email"]) > 254 or len(request.json["user_password"]) > 50:
            return jsonify({"Error": "Longitud de datos superada"}), 400
        
        if patron_invalido.search(request.json["user_password"]):
            return jsonify({"Error": "No se aceptan caracteres especiales"}), 400
        
        if not patron_correo_valido.search(request.json["email"]):
            return jsonify({"Error": "Formato de correo invalido"}), 400  

        # EJECUCION DEL LOGIN
        from app import mysqlconnection
        cursor = mysqlconnection.connection.cursor()
        query = f"SELECT session_token, username FROM users WHERE email = '{request.json['email']}' AND user_password = '{request.json['user_password']}'"
        cursor.execute(query)
        data = cursor.fetchone()
        cursor.close()

        if data != None:
            user_data = {
                "session_token": data[0],
                "username": data[1]
            }
            return jsonify({"Message": "Login exitoso", "Data": user_data})
        else:
            return jsonify({"Error": "Credenciales incorrectas"}), 500
        
    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500