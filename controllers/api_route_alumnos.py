from flask import request, jsonify
from app import app, db, Alumno, validar_nombre, validar_matricula, validar_promedio, validar_alumno_payload

# ✅ VÉRIFIER CES IMPORTS
try:
    from services.s3_service import S3Service
    s3_service = S3Service()
except Exception as e:
    print(f"⚠️ Erreur import S3Service : {e}")
    s3_service = None

try:
    from services.sns_service import SNSService
    sns_service = SNSService()
except Exception as e:
    print(f"⚠️ Erreur import SNSService : {e}")
    sns_service = None

try:
    from services.dynamodb_service import DynamoDBService
    dynamodb_service = DynamoDBService()
except Exception as e:
    print(f"⚠️ Erreur import DynamoDBService : {e}")
    dynamodb_service = None

# Champs autorisés dans PUT (y compris password)
CAMPOS_PERMITIDOS_EN_PUT = {"id", "nombres", "apellidos", "matricula", "promedio", "password"}

@app.route("/alumnos", methods=["GET"])
def alumnos_get():
    alumnos = Alumno.query.all()
    return jsonify([alumno.to_dict() for alumno in alumnos]), 200


@app.route("/alumnos", methods=["POST"])
def alumnos_create():
    data = request.get_json()

    nombres = data.get("nombres")
    apellidos = data.get("apellidos")
    matricula = data.get("matricula")
    promedio = data.get("promedio")
    password = data.get("password")

    errors = validar_alumno_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    nuevo_alumno = Alumno(
        nombres=nombres,
        apellidos=apellidos,
        matricula=matricula,
        promedio=promedio,
        password=password
    )
    
    db.session.add(nuevo_alumno)
    db.session.commit()

    return jsonify(nuevo_alumno.to_dict()), 201


@app.route("/alumnos/<int:alumno_id>", methods=["GET"])
def alumno_get(alumno_id):

    alumno = Alumno.query.get(alumno_id)
    
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    return jsonify(alumno.to_dict()), 200


@app.route("/alumnos/<int:alumno_id>", methods=["DELETE"])
def alumno_delete(alumno_id):

    alumno = Alumno.query.get(alumno_id)
    
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    db.session.delete(alumno)
    
    db.session.commit()
    
    return jsonify({"message": "Alumno eliminado"}), 200


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
    
    # ✅ AJOUTER : Permettre la mise à jour du password
    if "password" in data_to_update:
        password = data_to_update.get("password")
        # Le password peut être n'importe quelle chaîne (pas de validation stricte)
        if password is not None and isinstance(password, str):
            validated_data["password"] = password
    
    if errors:
        return jsonify({"errors": errors}), 400
    
    alumno = Alumno.query.get(alumno_id)
    
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    # Modification des attributs
    for key, value in validated_data.items():
        setattr(alumno, key, value)
    
    # Sauvegarde dans la BD
    db.session.commit()
    
    return jsonify(alumno.to_dict()), 200


@app.route("/alumnos/<int:alumno_id>/fotoPerfil", methods=["POST"])
def upload_foto_perfil(alumno_id):
    """Upload une photo de profil pour un alumno."""
    
    # ✅ VÉRIFIER QUE LE SERVICE EXISTE
    if s3_service is None:
        return jsonify({
            "error": "Servicio S3 no disponible"
        }), 500
    
    alumno = Alumno.query.get(alumno_id)
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    if 'foto' not in request.files:
        return jsonify({"error": "No se proporcionó ninguna foto"}), 400
    
    file = request.files['foto']
    
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400
    
    try:
        foto_url = s3_service.upload_foto_perfil(file, alumno_id)
        
        if foto_url is None:
            return jsonify({"error": "Error al subir la foto a S3"}), 500
        
        alumno.fotoPerfilUrl = foto_url
        db.session.commit()
        
        return jsonify(alumno.to_dict()), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Erreur lors de l'upload : {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route("/alumnos/<int:alumno_id>/email", methods=["POST"])
def enviar_email_alumno(alumno_id):
    """Envoie une notification par email avec les informations d'un alumno."""
    
    # ✅ VÉRIFIER QUE LE SERVICE EXISTE
    if sns_service is None:
        return jsonify({
            "error": "Servicio SNS no disponible"
        }), 500
    
    alumno = Alumno.query.get(alumno_id)
    
    if alumno is None:
        return jsonify({
            "error": "Alumno no encontrado"
        }), 404
    
    success = sns_service.enviar_notificacion_alumno(alumno)
    
    if success:
        return jsonify({
            "message": "Notificación enviada correctamente",
            "alumno": {
                "id": alumno.id,
                "nombres": alumno.nombres,
                "apellidos": alumno.apellidos,
                "matricula": alumno.matricula,
                "promedio": alumno.promedio
            }
        }), 200
    else:
        return jsonify({
            "error": "Error al enviar la notificación",
            "details": "Verifique los logs del servidor para más información"
        }), 500


@app.route("/alumnos/<int:alumno_id>/session/login", methods=["POST"])
def alumno_session_login(alumno_id):
    """Crée une session pour un alumno (login)."""
    
    # ✅ VÉRIFIER QUE LE SERVICE EXISTE
    if dynamodb_service is None:
        return jsonify({
            "error": "Servicio DynamoDB no disponible"
        }), 500
    
    data = request.get_json()
    
    if not data or 'password' not in data:
        return jsonify({
            "error": "Password requerido"
        }), 400
    
    password = data.get('password')
    
    alumno = Alumno.query.get(alumno_id)
    
    if alumno is None:
        return jsonify({
            "error": "Alumno no encontrado"
        }), 404
    
    if alumno.password != password:
        return jsonify({
            "error": "Contraseña incorrecta"
        }), 400
    
    session_data = dynamodb_service.crear_sesion(alumno_id)
    
    if session_data is None:
        return jsonify({
            "error": "Error al crear la sesión"
        }), 500
    
    return jsonify({
        "message": "Login exitoso",
        "sessionString": session_data['sessionString'],
        "sessionId": session_data['id'],
        "alumnoId": session_data['alumnoId'],
        "fecha": session_data['fecha']
    }), 200


@app.route("/alumnos/<int:alumno_id>/session/verify", methods=["POST"])
def alumno_session_verify(alumno_id):
    """Vérifie si une session est valide."""
    
    # ✅ VÉRIFIER QUE LE SERVICE EXISTE
    if dynamodb_service is None:
        return jsonify({
            "error": "Servicio DynamoDB no disponible"
        }), 500
    
    data = request.get_json()
    
    if not data or 'sessionString' not in data:
        return jsonify({
            "error": "sessionString requerido"
        }), 400
    
    session_string = data.get('sessionString')
    
    alumno = Alumno.query.get(alumno_id)
    
    if alumno is None:
        return jsonify({
            "error": "Alumno no encontrado"
        }), 404
    
    is_valid = dynamodb_service.verificar_sesion(session_string)
    
    if is_valid:
        session = dynamodb_service.obtener_sesion_por_string(session_string)
        
        if session and session.get('alumnoId') == alumno_id:
            return jsonify({
                "message": "Sesión válida",
                "valid": True,
                "sessionId": session['id'],
                "alumnoId": session['alumnoId'],
                "fecha": session['fecha']
            }), 200
        else:
            return jsonify({
                "error": "Sesión no pertenece a este alumno",
                "valid": False
            }), 400
    else:
        return jsonify({
            "error": "Sesión inválida o inactiva",
            "valid": False
        }), 400


@app.route("/alumnos/<int:alumno_id>/session/logout", methods=["POST"])
def alumno_session_logout(alumno_id):
    """Ferme une session (logout)."""
    
    # ✅ VÉRIFIER QUE LE SERVICE EXISTE
    if dynamodb_service is None:
        return jsonify({
            "error": "Servicio DynamoDB no disponible"
        }), 500
    
    data = request.get_json()
    
    if not data or 'sessionString' not in data:
        return jsonify({
            "error": "sessionString requerido"
        }), 400
    
    session_string = data.get('sessionString')
    
    alumno = Alumno.query.get(alumno_id)
    
    if alumno is None:
        return jsonify({
            "error": "Alumno no encontrado"
        }), 404
    
    session = dynamodb_service.obtener_sesion_por_string(session_string)
    
    if session is None:
        return jsonify({
            "error": "Sesión no encontrada"
        }), 400
    
    if session.get('alumnoId') != alumno_id:
        return jsonify({
            "error": "Sesión no pertenece a este alumno"
        }), 400
    
    success = dynamodb_service.cerrar_sesion(session_string)
    
    if success:
        return jsonify({
            "message": "Logout exitoso",
            "sessionId": session['id']
        }), 200
    else:
        return jsonify({
            "error": "Error al cerrar la sesión"
        }), 500



