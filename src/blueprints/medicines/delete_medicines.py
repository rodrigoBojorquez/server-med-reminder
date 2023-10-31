from flask import Blueprint, jsonify

delete_medicine_bp = Blueprint("delete_medicine", __name__)

@delete_medicine_bp.route("/medicines/<session_token>/<group>", methods=["DELETE"])
def delete_medicine(session_token, group):
    try:
        from app import mysqlconnection
        cursor = mysqlconnection.connection.cursor()

        query = f"SELECT users.id_user, medicines.medicine_group FROM medicines INNER JOIN users ON user_id = id_user WHERE session_token = {session_token} AND medicine_group = '{group}'"
        cursor.execute(query)
        data = cursor.fetchone()

        if data == None:
            cursor.close()
            return jsonify({"Error": "Token o grupo invalido"}), 401

        query = f"DELETE FROM medicines WHERE medicine_group = '{group}'"
        cursor.execute(query)
        mysqlconnection.connection.commit()

        return jsonify({"Message": "Medicina eliminada con exito"})
        
    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500