from flask import request, jsonify
from app import app, profesores, validar_nombre, validar_horas, validar_id, validar_profesor_payload

import json

@app.route("/profesores", methods=["GET"])
def profesores_get():
    return jsonify(profesores), 200

@app.route("/profesores", methods=["POST"])
def profesores_create():
    data = request.get_json()


    id = data.get("id")
    nombres = data.get("nombres")
    apellidos = data.get("apellidos")
    numeroEmpleado = data.get("numeroEmpleado")
    horasClase = data.get("horasClase")


    errors = validar_profesor_payload(data)

    if errors:
        return jsonify({"errors": errors}), 400

    nuevo_profesor = {
        "id": id,
        "nombres": nombres,
        "apellidos": apellidos,
        "numeroEmpleado": numeroEmpleado,
        "horasClase": horasClase
    }
    profesores.append(nuevo_profesor)

    return jsonify(nuevo_profesor), 201

@app.route("/profesores/<int:profesor_id>", methods=["GET"])
def profesor_get(profesor_id):
    for profesor in profesores:
        if profesor["id"] == profesor_id:
            return jsonify(profesor), 200
    return jsonify({"error": "Profesor no encontrado"}), 404

@app.route("/profesores/<int:profesor_id>", methods=["DELETE"])
def profesor_delete(profesor_id):
    for i, profesor in enumerate(profesores):
        if profesor["id"] == profesor_id:
            del profesores[i]
            return jsonify({"message": "Profesor eliminado"}), 200
    return jsonify({"error": "Profesor no encontrado"}), 404

@app.route("/profesores/<int:profesor_id>", methods=["PUT"])
def profesor_update(profesor_id):
    data = request.get_json()
    for profesor in profesores:
        if profesor["id"] == profesor_id:
            profesor.update(data)
            return jsonify(profesor), 200
    return jsonify({"error": "Profesor no encontrado"}), 404