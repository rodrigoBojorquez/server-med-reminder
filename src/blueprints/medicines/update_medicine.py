from flask import Blueprint, jsonify, request

update_medicine_bp = Blueprint("update_medicine", __name__)

@update_medicine_bp.route("/medicines/<session_token>/<medicine_id>", methods=["PATCH"])
def update_medicine(session_token, medicine_id):
    try:
        if(request.json["name_status"] == ""):
            return jsonify({"Error": "Parametro requerido"}), 401

        from app import mysqlconnection
        cursor = mysqlconnection.connection.cursor()
        query = f"SELECT users.id_user, medicines.id_medicine FROM medicines INNER JOIN users ON user_id = id_user WHERE session_token = '{session_token}' AND id_medicine = {medicine_id}"
        cursor.execute(query)
        data = cursor.fetchone()

        if data == None:
            cursor.close()
            return jsonify({"Error": "Token o Id de medicina no valido"}), 401
        
        user_id = data[0]
        id_medicine = data[1]

        # obteniendo id forane de status
        query = f"SELECT id_status FROM status WHERE name_status = '{request.json['name_status']}'"
        cursor.execute(query)
        data = cursor.fetchone()

        if data == None:
            cursor.close()
            return jsonify({"Error": "Status invalido"}), 401
        
        status_id = data[0]

        query = f"UPDATE medicines SET status_id = {status_id} WHERE id_medicine = {id_medicine} AND user_id = {user_id}" 
        cursor.execute(query)
        mysqlconnection.connection.commit()       

        return jsonify({"Message": "Se ha tomado la medicina con exito"})

        

    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500 