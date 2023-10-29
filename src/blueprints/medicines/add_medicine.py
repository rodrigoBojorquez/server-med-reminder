from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import random

add_medicine_bp = Blueprint("add_medicine", __name__)

@add_medicine_bp.route("/medicines/<session_token>", methods=["POST"])
def add_medicine(session_token):
    try:
        if (
            request.json["name_medicine"] == "" or
            request.json["type_medicine"] == "" or
            request.json["dose_quantity"] == "" or
            request.json["start_day"] == "" or
            request.json["start_hour"] == "" or
            request.json["doses_num"] == None or
            request.json["doses_interval"] == None      # or      
            # request.json["comments"] == ""
        ):
            return jsonify({"Error":"Todos los datos son obligatorios"}), 500

        if not (
            isinstance(request.json.get("doses_num"), int) and
            isinstance(request.json.get("doses_interval"), int) and
            isinstance(request.json.get("name_medicine"), str) and
            isinstance(request.json.get("type_medicine"), str) and
            isinstance(request.json.get("dose_quantity"), str) and
            isinstance(request.json.get("start_day"), str) and
            isinstance(request.json.get("start_hour"), str)
        ):
            return jsonify({"Error": "Tipo de valores incorrectos"}), 500
        
        from app import mysqlconnection
        cursor = mysqlconnection.connection.cursor()

        query = f"SELECT users.id_user FROM users WHERE session_token = {session_token}"
        cursor.execute(query)
        data = cursor.fetchone()
        user_id = data[0]

        if user_id == None:
            return jsonify({"Error": "Token no valido"}), 401
        
        # CALCULAR VALORES DE LLAVES FORANEAS
        query = f"SELECT id_type_medicine FROM type_medicine WHERE name_type_medicine = '{request.json['type_medicine']}'"
        cursor.execute(query)
        data = cursor.fetchone()
        type_medicine_id = data[0]

        if type_medicine_id == None:
            return jsonify({"Error": "Tipo de medicina invalido"})
        
        # CREAR ARREGLO CON TODAS LAS MEDICINAS
        medicines = medicines_generator(
            request.json["name_medicine"],
            type_medicine_id,
            request.json["start_day"],
            request.json["start_hour"],
            request.json["dose_quantity"],
            request.json["comments"],
            request.json["doses_num"],
            request.json["doses_interval"],
            user_id
        )

        for medicine in medicines:
            query = '''INSERT INTO medicines(
                name_medicine, type_medicine_id, dose_hour, dose_day, dose_quantity, comments, user_id, medicine_group, status_id
                ) 
                VALUES(
                    "{}",
                    {},
                    "{}",
                    "{}",
                    "{}",
                    "{}",
                    {},
                    "{}",
                    {}
                )
                '''.format(medicine["name_medicine"], medicine["type_medicine_id"], medicine["dose_hour"], medicine["dose_day"], medicine["dose_quantity"], medicine["comments"], medicine["user_id"], medicine["medicine_group"], medicine["status_id"])
            cursor.execute(query)

        mysqlconnection.connection.commit() 
        cursor.close()

        return jsonify({"Message": "Medicina agregada con exito"})

    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"}), 500
    

def generate_medicine_group():
    medicine_group = ''.join(str(random.randint(0,9)) for _ in range(15))
    return medicine_group
    
def medicines_generator(name_medicine, type_medicine_id, start_day, start_hour, dose_quantity, comments, doses_num, doses_interval, user_id):
    medicines = []
    # definiendo grupo
    group = generate_medicine_group()

    # Convertir start_day y start_hour a objetos de fecha y hora
    start_day = datetime.strptime(start_day, "%Y-%m-%d")
    start_hour = datetime.strptime(start_hour, "%H:%M:%S").time()
    current_dose_time = datetime.combine(start_day, start_hour)
    
    for i in range(doses_num):
        # Calcular la fecha y hora de la dosis actual
        current_dose_hour = current_dose_time.strftime("%H:%M:%S")
        current_dose_day = current_dose_time.strftime("%Y-%m-%d")

        medicine = {
            "name_medicine": name_medicine,
            "type_medicine_id": type_medicine_id,
            "dose_day": current_dose_day,
            "dose_hour": current_dose_hour,
            "dose_quantity": dose_quantity,
            "comments": comments,
            "user_id": user_id,
            "medicine_group": group,
            "status_id": 3
        }
        medicines.append(medicine)

        current_dose_time += timedelta(hours=doses_interval)        # acutaliza la hora
    
    return medicines