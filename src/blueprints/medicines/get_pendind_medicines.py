from flask import Blueprint, jsonify

pending_medicines_bp = Blueprint("pending_medicines", __name__)

@pending_medicines_bp.route("/medicines/pending/<session_token>", methods=["GET"])
def get_pending_medicines(session_token):
    try:
        from app import mysqlconnection
        # Obtén el user_id asociado al session_token
        cursor = mysqlconnection.connection.cursor()
        query = f"SELECT id_user FROM users WHERE session_token = '{session_token}'"
        cursor.execute(query)
        data = cursor.fetchone()

        if data is None:
            cursor.close()
            return jsonify({"Error": "El token no es válido"}), 400
        
        id_user = data[0]

        # Consulta los medicamentos tomados por el usuario
        query_taken_medicines = f"""
            SELECT 
                medicines.id_medicine, 
                medicines.name_medicine,
                type_medicine.name_type_medicine,
                TIME_FORMAT(medicines.dose_hour, '%H:%i:%s'), 
                DATE_FORMAT(medicines.dose_day, '%Y-%m-%d'),
                medicines.dose_quantity,
                medicines.comments,
                status.name_status
            FROM medicines
            INNER JOIN type_medicine ON type_medicine_id = id_type_medicine
            INNER JOIN status ON status_id = id_status
            WHERE user_id = {id_user} AND status_id = 3
        """
        cursor.execute(query_taken_medicines)
        data = cursor.fetchall()
        cursor.close()

        medicines = []

        for row in data:
            medicine = {
                "id_medicine": row[0],
                "name_medicine": row[1],
                "type_medicine": row[2],
                "dose_hour": row[3],
                "dose_day": row[4],
                "dose_quantity": row[5],
                "comments": row[6],
                "status": row[7]
            }
            medicines.append(medicine)

        return jsonify({"Message": "Medicamentos pendientes", "Data": medicines})

    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500
