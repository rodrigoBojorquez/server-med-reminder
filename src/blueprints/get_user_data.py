from flask import Blueprint, jsonify

get_user_data_bp = Blueprint("get_user_data", __name__)

@get_user_data_bp.route("/users/get-user-data/<session_token>", methods=["GET"])
def get_user_data(session_token):
    try:
        from app import mysqlconnection
        cursor = mysqlconnection.connection.cursor()
        query = f"SELECT username, email, user_password FROM users WHERE session_token = '{session_token}'"
        cursor.execute(query)
        data = cursor.fetchone()
        cursor.close()

        user_info = {
            "username": data[0],
            "email": data[1],
            "user_password": data[2]
        }

        return jsonify({"Message": "Datos enviados con exito", "Data": user_info})
    
    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500