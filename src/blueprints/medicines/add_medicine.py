from flask import Blueprint, jsonify, request

add_medicine_bp = Blueprint("add_medicine", __name__)

@add_medicine_bp.route("/medicines/<session_token>")
def add_medicine(session_token):
    try:
        datos_enviados = {
            "name_medicine": request.json["name_medicine"],
            "type_medicine_id": request.json["type_medicine_id"],
            "dose_hour": request.json["dose_hour"],
            "dose_day": request.json["dose_day"],
            "user_id": request.json["user_id"],
            "status_id": request.json["status_id"]
        }

        if is_empty(datos_enviados):
            return jsonify({"Error":"Todos los datos son obligatorios"}), 500
        
        return jsonify("Recibidos")

    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500
    

def is_empty(obj):
    for valor in obj.values():
        if valor is None:
            return True