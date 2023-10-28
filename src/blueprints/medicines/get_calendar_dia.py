from flask import Blueprint, jsonify
from app import mysqlconnection  # Importa la conexión a la base de datos desde tu aplicación Flask

calendar_medicines_bp = Blueprint("calendar_medicines", __name__)

@calendar_medicines_bp.route("/medicines/<session_token>/calendar/<dia>", methods=["GET"])
def get_medicines_for_day(session_token, dia):
    try:
        # Obtén el user_id asociado al session_token
        cursor = mysqlconnection.connection.cursor()
        query_user_id = "SELECT id_user FROM users WHERE session_token = %s"
        cursor.execute(query_user_id, (session_token,))
        user = cursor.fetchone()
        cursor.close()

        if user is None:
            return jsonify({"Error": "El session_token no es válido"}), 400

        # Consulta los medicamentos programados para el día especificado
        cursor = mysqlconnection.connection.cursor()
        query_medicines_for_day = """
            SELECT m.id_medicine, m.name_medicine
            FROM medicines m
            WHERE m.user_id = %s AND m.dose_day = %s
        """
        cursor.execute(query_medicines_for_day, (user['id_user'], dia))
        scheduled_medicines = cursor.fetchall()
        cursor.close()

        # Formatea los resultados en una lista de diccionarios
        scheduled_medicines_list = [{"id_medicine": med['id_medicine'], "name_medicine": med['name_medicine']} for med in scheduled_medicines]

        return jsonify({"Message": f"Medicamentos programados para el día {dia}", "Data": scheduled_medicines_list})

    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500
