from flask import request, jsonify
from app import app, alumnos, validar_nombre, validar_matricula, validar_promedio, validar_alumno_payload

# Champs autorisés dans PUT (id sera ignoré mais accepté)
CAMPOS_PERMITIDOS_EN_PUT = {"id", "nombres", "apellidos", "matricula", "promedio"}

@app.route("/alumnos", methods=["GET"])
def alumnos_get():
    """Liste tous les alumnos"""
    return jsonify(alumnos), 200

@app.route("/alumnos", methods=["POST"])
def alumnos_create():
    """Crée un nouvel alumno"""
    data = request.get_json()

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
    """Récupère un alumno par son ID"""
    for alumno in alumnos:
        if alumno["id"] == alumno_id:
            return jsonify(alumno), 200
    return jsonify({"error": "Alumno no encontrado"}), 404

@app.route("/alumnos/<int:alumno_id>", methods=["DELETE"])
def alumno_delete(alumno_id):
    """Supprime un alumno par son ID"""
    for i, alumno in enumerate(alumnos):
        if alumno["id"] == alumno_id:
            del alumnos[i]
            return jsonify({"message": "Alumno eliminado"}), 200
    return jsonify({"error": "Alumno no encontrado"}), 404

@app.route("/alumnos/<int:alumno_id>", methods=["PUT"])
def alumno_update(alumno_id):
    """Met à jour un alumno existant"""
    data = request.get_json()
    
    # Vérifier les clés invalides
    claves_invalidas = set(data.keys()) - CAMPOS_PERMITIDOS_EN_PUT
    if claves_invalidas:
        return jsonify({
            "error": f"Campos no permitidos: {', '.join(claves_invalidas)}"
        }), 400
    
    # Retirer l'ID du body (on utilise celui de l'URL)
    data_to_update = {k: v for k, v in data.items() if k != "id"}
    
    # Valider les champs à mettre à jour
    errors = {}
    validated_data = {}
    
    if "nombres" in data_to_update:
        nombres = validar_nombre(data_to_update.get("nombres"))
        if nombres is None:
            errors["nombres"] = "Nombre inválido."
        else:
            validated_data["nombres"] = nombres
    
    if "apellidos" in data_to_update:
        apellidos = validar_nombre(data_to_update.get("apellidos"))
        if apellidos is None:
            errors["apellidos"] = "Apellido inválido."
        else:
            validated_data["apellidos"] = apellidos
    
    if "matricula" in data_to_update:
        matricula = validar_matricula(data_to_update.get("matricula"))
        if matricula is None:
            errors["matricula"] = "Matrícula inválida."
        else:
            validated_data["matricula"] = matricula
    
    if "promedio" in data_to_update:
        promedio = validar_promedio(data_to_update.get("promedio"))
        if promedio is None:
            errors["promedio"] = "Promedio inválido."
        else:
            validated_data["promedio"] = promedio
    
    if errors:
        return jsonify({"errors": errors}), 400
    
    for alumno in alumnos:
        if alumno["id"] == alumno_id:
            alumno.update(validated_data)
            return jsonify(alumno), 200
    
    return jsonify({"error": "Alumno no encontrado"}), 404



