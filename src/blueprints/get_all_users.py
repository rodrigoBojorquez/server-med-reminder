from flask import Blueprint, jsonify
get_all_users_bp = Blueprint("get_all_users", __name__)

@get_all_users_bp.route("/users", methods=["GET"])
def get_all_users():
    try:
        from app import mysqlconnection
        cursor = mysqlconnection.connection.cursor()
        query = "SELECT * FROM users"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        users = []
        for fila in data:
            user = {
                "id": fila[0],
                "username": fila[1],
                "email": fila[2],
                "user_password": fila[3],
                "session_token": fila[4]
            }
            users.append(user)

        return jsonify({"Message": "Peticion exitosa","Data": users})
    
    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500