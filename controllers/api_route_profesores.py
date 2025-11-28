from flask import request, jsonify
from app import app, profesores, validar_nombre, validar_horas, validar_id, validar_profesor_payload

# Champs autorisés dans PUT (id sera ignoré mais accepté)
CAMPOS_PERMITIDOS_EN_PUT = {"id", "nombres", "apellidos", "numeroEmpleado", "horasClase"}

@app.route("/profesores", methods=["GET"])
def profesores_get():
    """Liste tous les profesores"""
    return jsonify(profesores), 200

@app.route("/profesores", methods=["POST"])
def profesores_create():
    """Crée un nouveau profesor"""
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
    """Récupère un profesor par son ID"""
    for profesor in profesores:
        if profesor["id"] == profesor_id:
            return jsonify(profesor), 200
    return jsonify({"error": "Profesor no encontrado"}), 404

@app.route("/profesores/<int:profesor_id>", methods=["DELETE"])
def profesor_delete(profesor_id):
    """Supprime un profesor par son ID"""
    for i, profesor in enumerate(profesores):
        if profesor["id"] == profesor_id:
            del profesores[i]
            return jsonify({"message": "Profesor eliminado"}), 200
    return jsonify({"error": "Profesor no encontrado"}), 404

@app.route("/profesores/<int:profesor_id>", methods=["PUT"])
def profesor_update(profesor_id):
    """Met à jour un profesor existant"""
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
    
    if "numeroEmpleado" in data_to_update:
        numeroEmpleado = validar_id(data_to_update.get("numeroEmpleado"))
        if numeroEmpleado is None:
            errors["numeroEmpleado"] = "Número de empleado inválido."
        else:
            validated_data["numeroEmpleado"] = numeroEmpleado
    
    if "horasClase" in data_to_update:
        horasClase = validar_horas(data_to_update.get("horasClase"))
        if horasClase is None:
            errors["horasClase"] = "Horas de clase inválidas."
        else:
            validated_data["horasClase"] = horasClase
    
    if errors:
        return jsonify({"errors": errors}), 400
    
    for profesor in profesores:
        if profesor["id"] == profesor_id:
            profesor.update(validated_data)
            return jsonify(profesor), 200
    
    return jsonify({"error": "Profesor no encontrado"}), 404


