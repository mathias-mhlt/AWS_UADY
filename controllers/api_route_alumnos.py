from flask import request, jsonify
from app import app, db, Alumno, validar_nombre, validar_matricula, validar_promedio, validar_alumno_payload
from services.s3_service import S3Service
from services.sns_service import SNSService  # ✅ Nouveau import

# Initialiser les services
s3_service = S3Service()
sns_service = SNSService()  # ✅ Nouveau service

# Champs autorisés dans PUT (id sera ignoré mais accepté)
CAMPOS_PERMITIDOS_EN_PUT = {"id", "nombres", "apellidos", "matricula", "promedio"}

@app.route("/alumnos", methods=["GET"])
def alumnos_get():
    """
    Liste tous les alumnos depuis la base de données.
    
    Logique :
    1. Alumno.query.all() récupère TOUS les enregistrements de la table 'alumno'
    2. to_dict() convertit chaque objet Alumno en dictionnaire JSON
    3. List comprehension [alumno.to_dict() for ...] crée une liste de dictionnaires
    """
    alumnos = Alumno.query.all()  # SELECT * FROM alumno
    return jsonify([alumno.to_dict() for alumno in alumnos]), 200


@app.route("/alumnos", methods=["POST"])
def alumnos_create():
    """
    Crée un nouvel alumno dans la base de données.
    Accepte maintenant le champ 'password'.
    """
    data = request.get_json()

    nombres = data.get("nombres")
    apellidos = data.get("apellidos")
    matricula = data.get("matricula")
    promedio = data.get("promedio")
    password = data.get("password")  # ✅ Nouveau champ

    # Validation (sans ID)
    errors = validar_alumno_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # Création d'un objet Alumno
    nuevo_alumno = Alumno(
        nombres=nombres,
        apellidos=apellidos,
        matricula=matricula,
        promedio=promedio,
        password=password  # ✅ Inclure le password
    )
    
    db.session.add(nuevo_alumno)
    db.session.commit()

    return jsonify(nuevo_alumno.to_dict()), 201


@app.route("/alumnos/<int:alumno_id>", methods=["GET"])
def alumno_get(alumno_id):
    """
    Récupère un alumno par son ID.
    
    Logique :
    - Alumno.query.get(id) : Recherche par clé primaire
    - Équivalent SQL : SELECT * FROM alumno WHERE id = ?
    """
    alumno = Alumno.query.get(alumno_id)
    
    # Si aucun résultat, retourner 404
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    return jsonify(alumno.to_dict()), 200


@app.route("/alumnos/<int:alumno_id>", methods=["DELETE"])
def alumno_delete(alumno_id):
    """
    Supprime un alumno de la base de données.
    
    Logique :
    1. Récupérer l'objet depuis la BD
    2. Le marquer pour suppression (db.session.delete)
    3. Confirmer la transaction (db.session.commit)
    """
    alumno = Alumno.query.get(alumno_id)
    
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    # Marquer pour suppression
    db.session.delete(alumno)
    
    # Exécuter le DELETE
    # Équivalent SQL : DELETE FROM alumno WHERE id = ?
    db.session.commit()
    
    return jsonify({"message": "Alumno eliminado"}), 200


@app.route("/alumnos/<int:alumno_id>", methods=["PUT"])
def alumno_update(alumno_id):
    """
    Met à jour un alumno existant.
    
    Changements majeurs :
    - Récupération depuis la BD (pas depuis une liste)
    - Modification des attributs de l'objet
    - db.session.commit() pour sauvegarder
    """
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
    
    # ===== RÉCUPÉRATION DE L'ALUMNO DEPUIS LA BD =====
    alumno = Alumno.query.get(alumno_id)
    
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    # ===== MODIFICATION DES ATTRIBUTS =====
    # Avant : alumno.update(validated_data) sur un dictionnaire
    # Maintenant : Modification directe des attributs de l'objet
    for key, value in validated_data.items():
        setattr(alumno, key, value)  # Équivalent à alumno.nombres = value
    
    # ===== SAUVEGARDE DANS LA BD =====
    # db.session.commit() : Exécute l'UPDATE
    # Équivalent SQL : UPDATE alumno SET nombres=?, apellidos=? WHERE id=?
    db.session.commit()
    
    return jsonify(alumno.to_dict()), 200


@app.route("/alumnos/<int:alumno_id>/fotoPerfil", methods=["POST"])
def upload_foto_perfil(alumno_id):
    """
    Upload une photo de profil pour un alumno.
    
    Endpoint : POST /alumnos/{id}/fotoPerfil
    Content-Type : multipart/form-data
    Body : { "foto": <fichier image> }
    
    Logique :
    1. Vérifier que l'alumno existe
    2. Récupérer le fichier depuis la requête
    3. Uploader vers S3
    4. Sauvegarder l'URL dans la base de données
    5. Retourner les données de l'alumno avec la nouvelle URL
    """
    
    # ===== VÉRIFICATION DE L'EXISTENCE DE L'ALUMNO =====
    alumno = Alumno.query.get(alumno_id)
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    # ===== RÉCUPÉRATION DU FICHIER =====
    # request.files est un dictionnaire contenant les fichiers uploadés
    # La clé doit correspondre au nom du champ dans le formulaire
    if 'foto' not in request.files:
        return jsonify({"error": "No se proporcionó ninguna foto"}), 400
    
    file = request.files['foto']
    
    # Vérifier que le fichier n'est pas vide
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400
    
    try:
        # ===== UPLOAD VERS S3 =====
        foto_url = s3_service.upload_foto_perfil(file, alumno_id)
        
        if foto_url is None:
            return jsonify({"error": "Error al subir la foto a S3"}), 500
        
        # ===== SAUVEGARDE DE L'URL DANS LA BASE DE DONNÉES =====
        alumno.fotoPerfilUrl = foto_url
        db.session.commit()
        
        # ===== RETOUR DES DONNÉES COMPLÈTES =====
        return jsonify(alumno.to_dict()), 200
        
    except ValueError as e:
        # Extension de fichier non autorisée
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Erreur inattendue
        print(f"Erreur lors de l'upload : {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route("/alumnos/<int:alumno_id>/email", methods=["POST"])
def enviar_email_alumno(alumno_id):
    """
    Envoie une notification par email avec les informations d'un alumno.
    
    Endpoint : POST /alumnos/{id}/email
    Content-Type : application/json
    Body : {} (vide, optionnel)
    
    Logique :
    1. Vérifier que l'alumno existe dans la base de données
    2. Récupérer les informations complètes de l'alumno
    3. Envoyer une notification SNS
    4. SNS dispatche automatiquement l'email à tous les abonnés
    5. Retourner un message de confirmation
    
    Codes de retour :
    - 200 : Email envoyé avec succès
    - 404 : Alumno non trouvé
    - 500 : Erreur lors de l'envoi
    """
    
    # ===== VÉRIFICATION DE L'EXISTENCE DE L'ALUMNO =====
    alumno = Alumno.query.get(alumno_id)
    
    if alumno is None:
        return jsonify({
            "error": "Alumno no encontrado"
        }), 404
    
    # ===== ENVOI DE LA NOTIFICATION SNS =====
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



