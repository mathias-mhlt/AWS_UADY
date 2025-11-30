import boto3
from botocore.exceptions import ClientError
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION, S3_BUCKET_NAME, S3_BASE_URL
import uuid
import os

class S3Service:
    """
    Service pour gérer les uploads vers S3.
    """
    
    def __init__(self):
        """
        Initialise le client S3 avec les credentials AWS.
        
        Logique :
        - boto3.client() crée une connexion authentifiée à S3
        - Les credentials proviennent de config.py
        """
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=AWS_REGION
        )
        self.bucket_name = S3_BUCKET_NAME
    
    def upload_foto_perfil(self, file, alumno_id):
        """
        Upload une photo de profil vers S3.
        
        Arguments :
        - file : Objet fichier Flask (FileStorage)
        - alumno_id : ID de l'alumno (pour nommer le fichier)
        
        Retourne :
        - URL publique du fichier uploadé
        - None en cas d'erreur
        
        Logique :
        1. Générer un nom de fichier unique (éviter les collisions)
        2. Extraire l'extension du fichier original
        3. Uploader vers S3 avec ACL public-read
        4. Retourner l'URL publique
        """
        
        # ===== VALIDATION DU FICHIER =====
        if not file:
            return None
        
        # Récupérer l'extension du fichier (.jpg, .png, etc.)
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        # Valider que c'est bien une image
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        if file_extension not in allowed_extensions:
            raise ValueError(f"Extension non autorisée. Utilisez : {', '.join(allowed_extensions)}")
        
        # ===== GÉNÉRATION DU NOM DE FICHIER =====
        # Format : alumnos/{id}/perfil_{uuid}.jpg
        # Exemple : alumnos/123/perfil_a1b2c3d4.jpg
        unique_id = str(uuid.uuid4())[:8]  # 8 premiers caractères d'un UUID
        file_key = f"alumnos/{alumno_id}/perfil_{unique_id}{file_extension}"
        
        try:
            # ===== UPLOAD VERS S3 =====
            self.s3_client.upload_fileobj(
                file,                    # Objet fichier
                self.bucket_name,        # Nom du bucket
                file_key,                # Chemin dans le bucket
                ExtraArgs={
                    'ACL': 'public-read',          # ✅ Rend le fichier public
                    'ContentType': file.content_type  # Définit le MIME type (image/jpeg, etc.)
                }
            )
            
            # ===== CONSTRUCTION DE L'URL PUBLIQUE =====
            file_url = f"{S3_BASE_URL}/{file_key}"
            # Exemple : https://uady-alumnos-fotos-mathias-2025.s3.us-east-1.amazonaws.com/alumnos/123/perfil_a1b2c3d4.jpg
            
            return file_url
            
        except ClientError as e:
            # Erreur AWS (bucket inexistant, permissions, etc.)
            print(f"Erreur S3 : {e}")
            return None
        except Exception as e:
            # Autre erreur
            print(f"Erreur inattendue : {e}")
            return None