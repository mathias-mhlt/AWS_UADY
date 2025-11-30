from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# ===== CONFIGURATION BASE DE DONNÉES =====
# Chemin absolu vers le fichier de base de données
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'alumnos_profesores.db')
# Désactiver le tracking des modifications (améliore les performances)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser SQLAlchemy (ORM) et Migrate (migrations)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ===== SUPPRESSION DE L'IN-MEMORY STORAGE =====
# AVANT : alumnos = []
# AVANT : profesores = []
# MAINTENANT : Les données sont dans la base de données

# Labels pour référence (optionnel, peut être supprimé)
labeles_alumnos = ["id", "nombres", "apellidos", "matricula", "promedio"]
labeles_profesores = ["id", "nombres", "apellidos", "numeroEmpleado", "horasClase"]

#VALIDATIONS
def validar_id(id):
    """Valide que l'ID est un entier positif"""
    try:
        id = int(id)
        if id > 0:
            return id
        return None
    except (ValueError, TypeError):
        return None

def validar_matricula(matricula):
    """Valide que la matricule commence par A suivi de chiffres"""
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
    """Valide que le nom contient uniquement des lettres, espaces, tirets et apostrophes"""
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
    """Valide que le promedio est un nombre entre 0 et 100"""
    try:
        promedio = float(promedio)
        if 0 <= promedio <= 100:
            return promedio
        return None
    except (ValueError, TypeError):
        return None

def validar_horas(horas):
    """Valide que les heures sont un entier positif"""
    try:
        horas = int(horas)
        if horas > 0:
            return horas
        return None
    except (ValueError, TypeError):
        return None

def validar_alumno_payload(payload):
    """Valide le payload pour créer/modifier un alumno"""
    errors = {}
    
    # # ID - obligatoire pour POST
    # if "id" not in payload:
    #     errors["id"] = "ID requerido."
    # else:
    #     id_validado = validar_id(payload.get("id"))
    #     if id_validado is None:
    #         errors["id"] = "ID inválido."
    
    # Nombres - optionnel, mais si présent doit être valide
    if "nombres" in payload:
        nombres = validar_nombre(payload.get("nombres"))
        if nombres is None:
            errors["nombres"] = "Nombre inválido."
    
    # Apellidos - optionnel, mais si présent doit être valide
    if "apellidos" in payload:
        apellidos = validar_nombre(payload.get("apellidos"))
        if apellidos is None:
            errors["apellidos"] = "Apellido inválido."
    
    # Matricula - optionnel, mais si présent doit être valide
    if "matricula" in payload:
        matricula = validar_matricula(payload.get("matricula"))
        if matricula is None:
            errors["matricula"] = "Matrícula inválida."
    
    # Promedio - optionnel, mais si présent doit être valide
    if "promedio" in payload:
        promedio = validar_promedio(payload.get("promedio"))
        if promedio is None:
            errors["promedio"] = "Promedio inválido."
    
    return errors

def validar_profesor_payload(payload):
    """Valide le payload pour créer/modifier un profesor"""
    errors = {}
    
    # # ID - obligatoire pour POST
    # if "id" not in payload:
    #     errors["id"] = "ID requerido."
    # else:
    #     id_validado = validar_id(payload.get("id"))
    #     if id_validado is None:
    #         errors["id"] = "ID inválido."
    
    # Nombres - optionnel
    if "nombres" in payload:
        nombres = validar_nombre(payload.get("nombres"))
        if nombres is None:
            errors["nombres"] = "Nombre inválido."
    
    # Apellidos - optionnel
    if "apellidos" in payload:
        apellidos = validar_nombre(payload.get("apellidos"))
        if apellidos is None:
            errors["apellidos"] = "Apellido inválido."
    
    # NumeroEmpleado - optionnel
    if "numeroEmpleado" in payload:
        numero = validar_id(payload.get("numeroEmpleado"))
        if numero is None:
            errors["numeroEmpleado"] = "Número de empleado inválido."
    
    # HorasClase - optionnel
    if "horasClase" in payload:
        horas = validar_horas(payload.get("horasClase"))
        if horas is None:
            errors["horasClase"] = "Horas de clase inválidas."
    
    return errors

# ===== MODÈLES DE BASE DE DONNÉES =====

class Alumno(db.Model):
    """
    Modèle représentant un étudiant dans la base de données.
    
    Nouveaux champs :
    - fotoPerfilUrl : URL de la photo de profil sur S3
    - password : Mot de passe de l'alumno (stocké en clair pour cet exercice)
    """
    __tablename__ = 'alumno'
    
    # ID auto-incrémenté par la base de données
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Champs existants
    nombres = db.Column(db.String(100), nullable=True)
    apellidos = db.Column(db.String(100), nullable=True)
    matricula = db.Column(db.String(20), nullable=True)
    promedio = db.Column(db.Float, nullable=True)
    
    # ===== NOUVEAUX CHAMPS =====
    fotoPerfilUrl = db.Column(db.String(500), nullable=True)  # URL de S3
    password = db.Column(db.String(255), nullable=True)       # Mot de passe
    
    def to_dict(self):
        """
        Convertit l'objet Alumno en dictionnaire JSON.
        Inclut maintenant fotoPerfilUrl et password.
        """
        return {
            'id': self.id,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'matricula': self.matricula,
            'promedio': self.promedio,
            'fotoPerfilUrl': self.fotoPerfilUrl,  # ✅ Nouveau
            'password': self.password              # ✅ Nouveau
        }


class Profesor(db.Model):
    """
    Modèle représentant un professeur dans la base de données.
    """
    __tablename__ = 'profesor'
    
    # ID auto-incrémenté
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Champs optionnels
    nombres = db.Column(db.String(100), nullable=True)
    apellidos = db.Column(db.String(100), nullable=True)
    numeroEmpleado = db.Column(db.Integer, nullable=True)
    horasClase = db.Column(db.Integer, nullable=True)
    
    def to_dict(self):
        """
        Convertit l'objet Profesor en dictionnaire JSON.
        """
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

