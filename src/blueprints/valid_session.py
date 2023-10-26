from flask import Blueprint, jsonify

valid_session_bp = Blueprint("valid_session", __name__)

@valid_session_bp.route("/users/<session_token>", methods=["GET"])
def valid_session(session_token):
    try:
        from app import mysqlconnection
        cursor = mysqlconnection.connection.cursor()
        query = f"SELECT email FROM users WHERE session_token = '{session_token}'"
        cursor.execute(query)
        data = cursor.fetchone()
        cursor.close()

        if data != None:
            return jsonify({"Message": "Cuenta autenticada", "Status": True})
        else:
            return jsonify({"Error": "Token no valido"}), 500
        
    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500