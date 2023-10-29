from flask import Blueprint, jsonify

update_group_medicines_bp = Blueprint("update_group_medicines", __name__)

@update_group_medicines_bp.route("/medicines/<session_token>/<group>", methods=["PUT"])
def update_group_medicines(session_token, group):
    try:
        from app import mysqlconnection
        # Obtén el user_id asociado al session_token
        cursor = mysqlconnection.connection.cursor()
        query = f"SELECT users.id_user, medicines.medicine_group FROM medicines INNER JOIN users ON user_id = id_user WHERE session_token = '{session_token}' AND medicine_group = '{group}'"
        cursor.execute(query)
        data = cursor.fetchone()

        if data is None:
            cursor.close()
            return jsonify({"Error": "El token o el grupo de medicinas no es válido"}), 400
        
        id_user = data[0]
        group_medicine = data[1]

        

        return "validaciones exitosas"

    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"})