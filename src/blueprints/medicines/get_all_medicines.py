from flask import Blueprint, jsonify

get_all_medicines_bp = Blueprint("get_all_medicines", __name__)

@get_all_medicines_bp.route("/medicines", methods=["GET"])
def get_all_medicines():
    try:
        from app import mysqlconnection
        cursor = mysqlconnection.connection.cursor()
        query = "SELECT id_medicine, name_medicine, name_type_medicine, dose_quantity, user_id, medicine_group FROM medicines INNER JOIN type_medicine ON type_medicine_id = id_type_medicine"   # editar query
        cursor.execute(query)
        data = cursor.fetchall()
        medicines = []
        for row in data:
            medicine = {
                "id_medicine": row[0],
                "name_medicine": row[1],
                "type_medicine": row[2],
                "dose_quantity": row[3],
                "user_id": row[4],
                "medicine_group": row[5]
            }
            medicines.append(medicine)
        return jsonify({"Message": "Todas las medicinas", "Data": medicines})
    
    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500