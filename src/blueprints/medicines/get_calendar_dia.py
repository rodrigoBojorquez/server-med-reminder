from flask import Blueprint, jsonify

calendar_medicines_bp = Blueprint("calendar_medicines", __name__)

@calendar_medicines_bp.route("/medicines/<session_token>/calendar/<dia>", methods=["GET"])
def get_medicines_for_day(session_token, dia):
    try:
        from app import mysqlconnection
        # Obtén el user_id asociado al session_token
        cursor = mysqlconnection.connection.cursor()
        query = f"SELECT id_user FROM users WHERE session_token = {session_token}"
        cursor.execute(query)
        data = cursor.fetchone()
        user_id = data[0]

        if user_id is None:
            cursor.close()
            return jsonify({"Error": "El token no es válido"}), 400

        # Consultar medicinas por dia                   MODIFICAR PARA DAR MAS DATOS
        query = f"""
            SELECT 
                medicines.id_medicine,
                  medicines.name_medicine, 
                  type_medicine.name_type_medicine, 
                  TIME_FORMAT(medicines.dose_hour, '%H:%i:%s'), 
                  DATE_FORMAT(medicines.dose_day, '%Y-%m-%d'),
                  medicines.dose_quantity,
                  medicines.comments,
                  status.name_status,
                  medicines.medicine_group
            FROM medicines
            INNER JOIN type_medicine ON type_medicine_id = id_type_medicine
            INNER JOIN status ON status_id = id_status
            WHERE user_id = {user_id} AND dose_day = "{dia}"
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        medicines_day = []

        for row in data:
            medicine = {
                "id_medicine": row[0],
                "name_medicine": row[1],
                "type_medicine": row[2],
                "dose_hour": row[3],
                "dose_day": row[4],
                "dose_quantity": row[5],
                "comments": row[6],
                "status": row[7],
                "medicine_group": row[8] 
            }
            medicines_day.append(medicine)

        return jsonify({"Message": f"Medicamentos programados para el día {dia}", "Data": medicines_day})

    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500
