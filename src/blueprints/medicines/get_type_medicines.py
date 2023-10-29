from flask import Blueprint, jsonify

get_type_medicines_bp = Blueprint("get_type_medicines", __name__)

@get_type_medicines_bp.route("/medicines/type-medicines", methods=["GET"])
def get_type_medicines():
    try:
        from app import mysqlconnection

        cursor = mysqlconnection.connection.cursor()
        query = f"SELECT name_type_medicine FROM type_medicine"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        type_medicines = []
        for row in data:
            type_medicines.append(row[0])

        return jsonify({"Message": "Tipos de medicinas", "Data": type_medicines})
    
    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado {ex}"}), 500