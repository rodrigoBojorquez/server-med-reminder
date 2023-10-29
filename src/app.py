from flask import Flask, jsonify
from flask_mysqldb import MySQL
from config import config
from flask_cors import CORS

# IMPORT BLUEPRINTS
from blueprints.get_all_users import get_all_users_bp
from blueprints.user_login import user_login_bp
from blueprints.valid_session import valid_session_bp
from blueprints.delete_user import delete_user_bp
from blueprints.user_sign_up import user_sign_up_bp
from blueprints.get_user_data import get_user_data_bp
from blueprints.update_user import update_user_bp
from blueprints.medicines.get_all_medicines import get_all_medicines_bp
from blueprints.medicines.add_medicine import add_medicine_bp
from blueprints.medicines.get_calendar_dia import calendar_medicines_bp
from blueprints.medicines.get_pendind_medicines import pending_medicines_bp
from blueprints.medicines.get_taken_medicines import medicines_taken_bp
from blueprints.medicines.get_user_medicines import get_user_medicines_bp
from blueprints.medicines.update_group_medicines import update_group_medicines_bp
from blueprints.medicines.get_type_medicines import get_type_medicines_bp


app = Flask(__name__)
mysqlconnection = MySQL(app)
CORS(app)

# REGISTRO DE BLUEPRINTS
app.register_blueprint(get_all_users_bp)
app.register_blueprint(user_login_bp)
app.register_blueprint(valid_session_bp)
app.register_blueprint(delete_user_bp)
app.register_blueprint(user_sign_up_bp)
app.register_blueprint(get_user_data_bp)
app.register_blueprint(update_user_bp)
app.register_blueprint(get_all_medicines_bp)
app.register_blueprint(add_medicine_bp)
app.register_blueprint(calendar_medicines_bp)
app.register_blueprint(pending_medicines_bp)
app.register_blueprint(medicines_taken_bp)
app.register_blueprint(get_user_medicines_bp)
app.register_blueprint(update_group_medicines_bp)
app.register_blueprint(get_type_medicines_bp)

@app.route("/")
def home():
    return "El servidor se esta ejecutando correctamente"

def page_not_found(err):
    return "<h1>La pagina que buscas no existe</h1>", 404

if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.register_error_handler(404, page_not_found)
    app.run()