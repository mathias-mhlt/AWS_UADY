from flask import Flask, request, jsonify


app = Flask(__name__)

#in-memory storage
alumnos = []
profesores = []
labeles_alumnos = ["id", "nombres", "apellidos", "matricula", "promedio"]
labeles_profesores = ["id", "nombres", "apellidos", "numeroEmpleado", "horasClase"]

#VALIDACIONES
def validar_id(id):
    try:
        id = int(id)
        return id
    except ValueError:
        return None
    
def validar_nombre(nombre):
    if not isinstance(nombre, str):
        return None
    for ch in nombre:
        if not (ch.isalpha() or ch in " -'"):
            return None
    return nombre

# def not_empty(data):
#     if not data:
#         return False
#     return True

def validar_horas(horas):
    try:
        horas = float(horas)
        if horas < 0:
            return None
        return horas
    except ValueError:
        return None
    
def validar_matricula(matricula):
    if not isinstance(matricula, str):
        return None
    if matricula[0].isalpha() and matricula[1:].isdigit():
        return matricula
    return None

def validar_promedio(promedio):
    if not isinstance(promedio, (int, float)):
        return None
    if promedio < 0 or promedio > 100:
        return None
    return promedio

def validar_labels(payload, labeles):
    for label in payload.keys():
        if label not in labeles:
            return False
    return True

def validar_alumno_payload(payload):
    errors = {}

    if not validar_labels(payload, labeles_alumnos):
        errors["labels"] = "Etiquetas invalidas en el payload."
        return errors

    id = validar_id(payload.get("id"))
    if id is None: 
        errors["id"] = "ID invalido."

    nombres = validar_nombre(payload.get("nombres"))
    if nombres is None: 
        errors["nombres"] = "Nombre invalido."

    apellidos = validar_nombre(payload.get("apellidos"))
    if apellidos is None: 
        errors["apellidos"] = "Apellido invalido."

    matricula = validar_matricula(payload.get("matricula"))
    if matricula is None:   
        errors["matricula"] = "Matricula invalida."
    
    promedio = validar_promedio(payload.get("promedio"))
    if promedio is None:   
        errors["promedio"] = "Promedio invalido."

    return errors

def validar_profesor_payload(payload):
    errors = {}

    if not validar_labels(payload, labeles_profesores):
        errors["labels"] = "Etiquetas invalidas en el payload."
        return errors

    id = validar_id(payload.get("id"))
    if id is None: 
        errors["id"] = "ID invalido."

    numeroEmpleado = validar_id(payload.get("numeroEmpleado"))
    if numeroEmpleado is None: 
        errors["numeroEmpleado"] = "Numero de empleado invalido."

    nombres = validar_nombre(payload.get("nombres"))
    if nombres is None: 
        errors["nombres"] = "Nombre invalido."

    apellidos = validar_nombre(payload.get("apellidos"))
    if apellidos is None: 
        errors["apellidos"] = "Apellido invalido."

    horasClase = validar_horas(payload.get("horasClase"))
    if horasClase is None:   
        errors["horasClase"] = "Horas invalidas."

    return errors

#ERROR HANDLER
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, KeyError):
        return jsonify({"error": "Clave no encontrada en el payload."}), 400
    return jsonify({"error": "Error interno del servidor."}), 500

