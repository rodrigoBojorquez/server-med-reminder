from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta

update_group_medicines_bp = Blueprint("update_group_medicines", __name__)

@update_group_medicines_bp.route("/medicines/<session_token>/<group>", methods=["PUT"])
def update_group_medicines(session_token, group):
    try:
        from app import mysqlconnection
        # Obtén el user_id asociado al session_token
        cursor = mysqlconnection.connection.cursor()
        query = f"SELECT users.id_user, medicines.medicine_group FROM medicines INNER JOIN users ON user_id = id_user WHERE session_token = '{session_token}' AND medicine_group = '{group}'"
        cursor.execute(query)
        data = cursor.fetchone()

        if data is None:
            cursor.close()
            return jsonify({"Error": "El token o el grupo de medicinas no es válido"}), 400
        
        id_user = data[0]
        group_medicine = data[1]

        # validar modificaciones
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
        
        #Borrar todos los registros anteriores
        query = f"DELETE FROM medicines WHERE medicine_group = '{group_medicine}'"
        cursor.execute(query)
        mysqlconnection.connection.commit()

        # calculando tipo de medicina
        query = f"SELECT id_type_medicine FROM type_medicine WHERE name_type_medicine = '{request.json['type_medicine']}'"
        cursor.execute(query)
        data = cursor.fetchone()
        type_medicine_id = data[0]

        if type_medicine_id == None:
            cursor.close()
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
            id_user,
            group_medicine
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


        return jsonify({"Message": "Medicina editada con exito"})

    except Exception as ex:
        return jsonify({"Error": f"Ha ocurrido un error inesperado, {ex}"})
    

def medicines_generator(name_medicine, type_medicine_id, start_day, start_hour, dose_quantity, comments, doses_num, doses_interval, user_id, medicine_group):
    medicines = []
    # definiendo grupo
    group = medicine_group

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