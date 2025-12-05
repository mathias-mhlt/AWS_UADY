from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# ===== CONFIGURACION DATABASE =====

if os.environ.get('ENV') == 'production':
    # ===== CONFIGURACION RDS MYSQL (PRODUCION) =====
    DB_USER = os.environ.get('DB_USER', 'm25090057')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Eselproyectofinal!')
    DB_HOST = os.environ.get('DB_HOST', 'database-proyecto-final.cslvaacprg0m.us-east-1.rds.amazonaws.com')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'database-proyecto-final')
    
    DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
else:
    # ===== CONFIGURACION SQLITE (LOCAL/DEV) =====
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'alumnos_profesores.db')

# CONFIGURACION Flask
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"Conexion a la base de datos : {DATABASE_URI.split('@')[-1] if '@' in DATABASE_URI else 'SQLite local'}")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

labeles_alumnos = ["id", "nombres", "apellidos", "matricula", "promedio"]
labeles_profesores = ["id", "nombres", "apellidos", "numeroEmpleado", "horasClase"]

#VALIDACIONES
def validar_id(id):
    try:
        id = int(id)
        if id > 0:
            return id
        return None
    except (ValueError, TypeError):
        return None

def validar_matricula(matricula):
    if not isinstance(matricula, str):
        return None
    matricula = matricula.strip()
    if not matricula:
        return None
    if not matricula.startswith('A'):
        return None
    if not matricula[1:].isdigit():
        return None
    return matricula

def validar_nombre(nombre):
    if not isinstance(nombre, str):
        return None
    nombre = nombre.strip()
    if not nombre:
        return None
    for ch in nombre:
        if not (ch.isalpha() or ch in " -'"):
            return None
    return nombre

def validar_promedio(promedio):
    try:
        promedio = float(promedio)
        if 0 <= promedio <= 100:
            return promedio
        return None
    except (ValueError, TypeError):
        return None

def validar_horas(horas):
    try:
        horas = int(horas)
        if horas > 0:
            return horas
        return None
    except (ValueError, TypeError):
        return None

def validar_alumno_payload(payload):
    errors = {}
    
    # if "id" not in payload:
    #     errors["id"] = "ID requerido."
    # else:
    #     id_validado = validar_id(payload.get("id"))
    #     if id_validado is None:
    #         errors["id"] = "ID inválido."
    
    if "nombres" in payload:
        nombres = validar_nombre(payload.get("nombres"))
        if nombres is None:
            errors["nombres"] = "Nombre inválido."
    
    if "apellidos" in payload:
        apellidos = validar_nombre(payload.get("apellidos"))
        if apellidos is None:
            errors["apellidos"] = "Apellido inválido."
    
    if "matricula" in payload:
        matricula = validar_matricula(payload.get("matricula"))
        if matricula is None:
            errors["matricula"] = "Matrícula inválida."
    
    if "promedio" in payload:
        promedio = validar_promedio(payload.get("promedio"))
        if promedio is None:
            errors["promedio"] = "Promedio inválido."
    
    return errors

def validar_profesor_payload(payload):
    errors = {}
    
    if "nombres" in payload:
        nombres = validar_nombre(payload.get("nombres"))
        if nombres is None:
            errors["nombres"] = "Nombre inválido."
    
    if "apellidos" in payload:
        apellidos = validar_nombre(payload.get("apellidos"))
        if apellidos is None:
            errors["apellidos"] = "Apellido inválido."
    
    if "numeroEmpleado" in payload:
        numero = validar_id(payload.get("numeroEmpleado"))
        if numero is None:
            errors["numeroEmpleado"] = "Número de empleado inválido."
    
    if "horasClase" in payload:
        horas = validar_horas(payload.get("horasClase"))
        if horas is None:
            errors["horasClase"] = "Horas de clase inválidas."
    
    return errors

# ===== MODELOS DE BASE DE DATOS =====

class Alumno(db.Model):
    __tablename__ = 'alumnos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(100), nullable=True)
    apellidos = db.Column(db.String(100), nullable=True)
    matricula = db.Column(db.String(20), nullable=True)
    promedio = db.Column(db.Float, nullable=True)
    fotoPerfilUrl = db.Column(db.String(500), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):

        return {
            'id': self.id,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'matricula': self.matricula,
            'promedio': self.promedio,
            'fotoPerfilUrl': self.fotoPerfilUrl,
            'password': self.password
        }


class Profesor(db.Model):
    __tablename__ = 'profesores'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(100), nullable=True)
    apellidos = db.Column(db.String(100), nullable=True)
    numeroEmpleado = db.Column(db.Integer, nullable=True)
    horasClase = db.Column(db.Integer, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'numeroEmpleado': self.numeroEmpleado,
            'horasClase': self.horasClase
        }

#ERROR HANDLERS
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Método no permitido"}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

