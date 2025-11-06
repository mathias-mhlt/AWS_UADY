from flask import request, jsonify
from app import app, alumnos, validar_nombre, validar_matricula, validar_promedio, validar_alumno_payload

import json

@app.route("/alumnos", methods=["GET"])
def alumnos_get():
    return jsonify(alumnos), 200

@app.route("/alumnos", methods=["POST"])
def alumnos_create():
    data = request.get_json()

    print("=== DEBUG POST /alumnos ===")
    print(f"Data reçue: {data}")
    print(f"Type: {type(data)}")

    id = data.get("id")
    nombres = data.get("nombres")
    apellidos = data.get("apellidos")
    matricula = data.get("matricula")
    promedio = data.get("promedio")

    errors = validar_alumno_payload(data)

    if errors:
        return jsonify({"errors": errors}), 400

    nuevo_alumno = {
        "id": id,
        "nombres": nombres,
        "apellidos": apellidos,
        "matricula": matricula,
        "promedio": promedio
    }
    alumnos.append(nuevo_alumno)

    return jsonify(nuevo_alumno), 201

@app.route("/alumnos/<int:alumno_id>", methods=["GET"])
def alumno_get(alumno_id):
    for alumno in alumnos:
        if alumno["id"] == alumno_id:
            return jsonify(alumno), 200
    return jsonify({"error": "Alumno no encontrado"}), 404

@app.route("/alumnos/<int:alumno_id>", methods=["DELETE"])
def alumno_delete(alumno_id):
    for i, alumno in enumerate(alumnos):
        if alumno["id"] == alumno_id:
            del alumnos[i]
            return jsonify({"message": "Alumno eliminado"}), 200
    return jsonify({"error": "Alumno no encontrado"}), 404

@app.route("/alumnos/<int:alumno_id>", methods=["PUT"])
def alumno_update(alumno_id):
    data = request.get_json()
    for alumno in alumnos:
        if alumno["id"] == alumno_id:
            alumno.update(data)
            return jsonify(alumno), 200
    return jsonify({"error": "Alumno no encontrado"}), 404