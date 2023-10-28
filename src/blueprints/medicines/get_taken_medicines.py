from flask import Blueprint, jsonify

medicines_taken_bp = Blueprint("medicines_taken", __name__)

@medicines_taken_bp.route("/medicines/taken/<session_token>", methods=["GET"])
def get_taken_medicines(session_token):
    try:
        from app import mysqlconnection  # Importa la conexión a la base de datos desde tu aplicación Flask

        # Primero, obtén el user_id asociado al session_token
        cursor = mysqlconnection.connection.cursor()
        query_user_id = "SELECT id_user FROM users WHERE session_token = %s"
        cursor.execute(query_user_id, (session_token,))
        user_id = cursor.fetchone()
        cursor.close()

        if user_id is None:
            return jsonify({"Error": "El session_token no es válido"}), 400

        # Ahora, utiliza el user_id para obtener los medicamentos tomados por el usuario
        cursor = mysqlconnection.connection.cursor()
        query_taken_medicines = """
            SELECT m.id_medicine, m.name_medicine
            FROM medicines m
            WHERE m.user_id = %s
        """
        cursor.execute(query_taken_medicines, (user_id['id_user'],))
        taken_medicines = cursor.fetchall()
        cursor.close()

        # Formatea los resultados en una lista de diccionarios
        taken_medicines_list = [{"id_medicine": med['id_medicine'], "name_medicine": med['name_medicine']} for med in taken_medicines]

        return jsonify({"Message": "Medicamentos tomados por el usuario", "Data": taken_medicines_list})

    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500
