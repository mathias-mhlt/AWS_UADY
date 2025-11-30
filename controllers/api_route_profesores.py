from flask import request, jsonify
from app import app, db, Profesor, validar_nombre, validar_horas, validar_id, validar_profesor_payload

# Champs autorisés dans PUT (id sera ignoré mais accepté)
CAMPOS_PERMITIDOS_EN_PUT = {"id", "nombres", "apellidos", "numeroEmpleado", "horasClase"}

@app.route("/profesores", methods=["GET"])
def profesores_get():
    """Liste tous les profesores depuis la base de données"""
    profesores = Profesor.query.all()  # SELECT * FROM profesor
    return jsonify([profesor.to_dict() for profesor in profesores]), 200


@app.route("/profesores", methods=["POST"])
def profesores_create():
    """Crée un nouveau profesor dans la base de données"""
    data = request.get_json()

    # L'ID n'est PLUS extrait (auto-généré)
    nombres = data.get("nombres")
    apellidos = data.get("apellidos")
    numeroEmpleado = data.get("numeroEmpleado")
    horasClase = data.get("horasClase")

    errors = validar_profesor_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # Création d'un objet Profesor
    nuevo_profesor = Profesor(
        nombres=nombres,
        apellidos=apellidos,
        numeroEmpleado=numeroEmpleado,
        horasClase=horasClase
    )
    
    # Insertion dans la BD
    db.session.add(nuevo_profesor)
    db.session.commit()

    return jsonify(nuevo_profesor.to_dict()), 201


@app.route("/profesores/<int:profesor_id>", methods=["GET"])
def profesor_get(profesor_id):
    """Récupère un profesor par son ID"""
    profesor = Profesor.query.get(profesor_id)
    
    if profesor is None:
        return jsonify({"error": "Profesor no encontrado"}), 404
    
    return jsonify(profesor.to_dict()), 200


@app.route("/profesores/<int:profesor_id>", methods=["DELETE"])
def profesor_delete(profesor_id):
    """Supprime un profesor de la base de données"""
    profesor = Profesor.query.get(profesor_id)
    
    if profesor is None:
        return jsonify({"error": "Profesor no encontrado"}), 404
    
    db.session.delete(profesor)
    db.session.commit()
    
    return jsonify({"message": "Profesor eliminado"}), 200


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
    
    # Retirer l'ID du body
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
    
    # Récupération de l'objet depuis la BD
    profesor = Profesor.query.get(profesor_id)
    
    if profesor is None:
        return jsonify({"error": "Profesor no encontrado"}), 404
    
    # Modification des attributs
    for key, value in validated_data.items():
        setattr(profesor, key, value)
    
    # Sauvegarde dans la BD
    db.session.commit()
    
    return jsonify(profesor.to_dict()), 200


