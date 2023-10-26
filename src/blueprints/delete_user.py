from flask import Blueprint, request, jsonify

delete_user_bp = Blueprint("delete_user", __name__)

@delete_user_bp.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        from app import mysqlconnection
        cursor = mysqlconnection.connection.cursor()
        # COMPROBAR SI HAY USUARIO CON ESE ID
        query = f"SELECT * FROM users WHERE id_user = {id}"
        cursor.execute(query)
        data = cursor.fetchone()

        if data == None:
            cursor.close()
            return jsonify({"Error": "Usuario no existente"}), 500
        
        query = f"DELETE FROM users WHERE id_user = {id}"
        cursor.execute(query)
        mysqlconnection.connection.commit()
        return jsonify({"Message": "Usuario eliminado con exito"})
    
    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500