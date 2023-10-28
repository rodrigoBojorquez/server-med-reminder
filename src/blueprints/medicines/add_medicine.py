from flask import Blueprint, jsonify, request

add_medicine_bp = Blueprint("add_medicine", __name__)

@add_medicine_bp.route("/medicines/<session_token>", methods=["POST"])
def add_medicine(session_token):
    try:
        datos_obligatorios = {
            "name_medicine": request.json["name_medicine"],
            "type_medicine_id": request.json["type_medicine_id"],
            "dose_hour": request.json["dose_hour"],
            "dose_day": request.json["dose_day"],
            "status_id": request.json["status_id"]
        }

        if is_empty(datos_obligatorios):
            return jsonify({"Error":"Todos los datos son obligatorios"}), 500
        
        if not (
            isinstance(request.json.get("type_medicine_id"), int) and
            isinstance(request.json.get("dose_quantity"), int) and
            isinstance(request.json.get("user_id"), int) and
            isinstance(request.json.get("status_id"), int)
        ):
            return jsonify({"Error": "Tipo de valores incorrectos"}), 500
        
        from app import mysqlconnection             #conexion a la db
        cursor = mysqlconnection.connection.cursor()
        query = f'''INSERT INTO medicines(
            name_medicine, type_medicine_id, dose_hour, dose_day, dose_quantity, comments, medicine_group, status_id
            ) 
            VALUES(
                "{request.json["name_medicine"]}",
                "{request.json["type_medicine_id"]}",
                "{request.json["dose_hour"]}",
                "{request.json["dose_day"]}",
                "{request.json["dose_quantity"]}",
                "{request.json["comments"]}",
                "{request.json["medicine_group"]}",
                "{request.json["status_id"]}"
            )
            '''
        cursor.execute(query)
        mysqlconnection.connection.commit()
        cursor.close()

        return jsonify({"Message": "Medicina agregada con exito"})

    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500
    

def is_empty(obj):
    for valor in obj.values():
        if valor is None:
            return True