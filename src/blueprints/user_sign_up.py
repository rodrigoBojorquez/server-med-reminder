from flask import Blueprint, jsonify, request
import re, string, random

user_sign_up_bp = Blueprint("user_sign_up", __name__)

@user_sign_up_bp.route("/users/sign-up", methods=["POST"])
def sign_up():
    try:
        # VALIDACIONES DE DATOS
        patron_invalido = re.compile(r'[^a-zA-Z0-9-_]+$')
        patron_correo_valido = re.compile(r'^[\w\.-]+@[\w\.-]+(\.\w+)+$')

        if type(request.json["username"]) != str or type(request.json["email"]) != str or type(request.json["user_password"]) != str:
            return jsonify({"Error": "Los datos solo pueden ser texto"}), 500

        if request.json["username"] == "" or request.json["email"] == "" or request.json["user_password"] == "":
            return jsonify({"Error": "Todos los campos son obligatorios"}), 500
        
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
        query = f"SELECT email FROM users WHERE email = '{request.json['email']}'"
        cursor.execute(query)
        data = cursor.fetchone()

        if data:
            cursor.close()
            return jsonify({"Error": "Correo ya registrado"}), 500
        
        # EJECUCION DE REGISTRO
        query = f'INSERT INTO users (username, email, user_password, session_token) VALUES ("{request.json["username"]}", "{request.json["email"]}", "{request.json["user_password"]}", "{generate_session_token()}")'
        cursor.execute(query)
        mysqlconnection.connection.commit()
        cursor.close()
        return jsonify({"Message": "Se registro al usuario con exito"}), 201

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

def generate_session_token():
    caracteres = string.ascii_letters = string.digits
    token_aleatorio = "".join(random.choice(caracteres) for i in range(15))
    return token_aleatorio