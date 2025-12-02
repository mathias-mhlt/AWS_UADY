import boto3
from botocore.exceptions import ClientError
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION, DYNAMODB_TABLE_NAME
import uuid
import time
import secrets

class DynamoDBService:
    """
    Service pour gérer les sessions des alumnos dans DynamoDB.
    """
    
    def __init__(self):
        """
        Initialise le client DynamoDB avec les credentials AWS.
        
        Logique :
        - boto3.resource('dynamodb') crée une interface de haut niveau
        - Plus simple que boto3.client() pour les opérations CRUD
        """
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=AWS_REGION
        )
        self.table = self.dynamodb.Table(DYNAMODB_TABLE_NAME)
    
    def generar_session_string(self, length=128):
        """
        Génère un string aléatoire sécurisé de 128 caractères.
        
        Arguments :
        - length : Longueur du string (défaut: 128)
        
        Retourne :
        - String hexadécimal aléatoire
        
        Logique :
        - secrets.token_hex() génère des bytes aléatoires cryptographiquement sûrs
        - Convertit en hexadécimal (0-9, a-f)
        - 128 caractères hex = 64 bytes
        """
        return secrets.token_hex(length // 2)
    
    def crear_sesion(self, alumno_id):
        """
        Crée une nouvelle session pour un alumno (login).
        
        Arguments :
        - alumno_id : ID de l'alumno (int)
        
        Retourne :
        - Dictionnaire contenant les données de la session
        - None en cas d'erreur
        
        Logique :
        1. Générer un UUID unique pour l'ID de la session
        2. Générer un sessionString aléatoire de 128 caractères
        3. Récupérer le timestamp Unix actuel
        4. Créer l'entrée dans DynamoDB
        """
        
        try:
            # ===== GÉNÉRATION DES DONNÉES DE SESSION =====
            session_id = str(uuid.uuid4())  # UUID v4 (ex: "550e8400-e29b-41d4-a716-446655440000")
            session_string = self.generar_session_string(128)
            timestamp = int(time.time())  # Timestamp Unix (ex: 1701234567)
            
            # ===== CRÉATION DE L'ITEM DYNAMODB =====
            session_data = {
                'id': session_id,
                'fecha': timestamp,
                'alumnoId': alumno_id,
                'active': True,
                'sessionString': session_string
            }
            
            # ===== INSERTION DANS DYNAMODB =====
            self.table.put_item(Item=session_data)
            
            print(f"✅ Session créée : ID={session_id}, AlumnoID={alumno_id}")
            
            return session_data
            
        except ClientError as e:
            # Erreur AWS (permissions, table inexistante, etc.)
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"❌ Erreur DynamoDB [{error_code}]: {error_message}")
            return None
            
        except Exception as e:
            # Autre erreur
            print(f"❌ Erreur inattendue lors de la création de session : {e}")
            return None
    
    def verificar_sesion(self, session_string):
        """
        Vérifie si une session est valide (active).
        
        Arguments :
        - session_string : String de session à vérifier (128 caractères)
        
        Retourne :
        - True si la session existe et est active
        - False sinon
        
        Logique :
        1. Scanner la table pour trouver l'item avec ce sessionString
        2. Vérifier que l'item existe
        3. Vérifier que active = True
        """
        
        try:
            # ===== RECHERCHE PAR SESSIONSTRING =====
            # Scan = parcourt toute la table (pas optimal, mais simple)
            # Alternative : Utiliser un GSI (Global Secondary Index) sur sessionString
            response = self.table.scan(
                FilterExpression='sessionString = :ss',
                ExpressionAttributeValues={
                    ':ss': session_string
                }
            )
            
            items = response.get('Items', [])
            
            # ===== VÉRIFICATION DES RÉSULTATS =====
            if not items:
                print(f"❌ Aucune session trouvée avec ce sessionString")
                return False
            
            # Prendre le premier résultat (devrait être unique)
            session = items[0]
            
            # Vérifier que la session est active
            is_active = session.get('active', False)
            
            if is_active:
                print(f"✅ Session valide : ID={session['id']}, AlumnoID={session['alumnoId']}")
                return True
            else:
                print(f"❌ Session inactive : ID={session['id']}")
                return False
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"❌ Erreur DynamoDB [{error_code}]: {error_message}")
            return False
            
        except Exception as e:
            print(f"❌ Erreur inattendue lors de la vérification : {e}")
            return False
    
    def cerrar_sesion(self, session_string):
        """
        Ferme une session (logout) en mettant active = False.
        
        Arguments :
        - session_string : String de session à fermer
        
        Retourne :
        - True si la session a été fermée avec succès
        - False sinon
        
        Logique :
        1. Trouver la session par sessionString
        2. Mettre à jour l'attribut active à False
        """
        
        try:
            # ===== RECHERCHE DE LA SESSION =====
            response = self.table.scan(
                FilterExpression='sessionString = :ss',
                ExpressionAttributeValues={
                    ':ss': session_string
                }
            )
            
            items = response.get('Items', [])
            
            if not items:
                print(f"❌ Aucune session trouvée avec ce sessionString")
                return False
            
            session = items[0]
            session_id = session['id']
            
            # ===== MISE À JOUR DE L'ATTRIBUT ACTIVE =====
            self.table.update_item(
                Key={'id': session_id},
                UpdateExpression='SET active = :val',
                ExpressionAttributeValues={
                    ':val': False
                }
            )
            
            print(f"✅ Session fermée : ID={session_id}")
            return True
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"❌ Erreur DynamoDB [{error_code}]: {error_message}")
            return False
            
        except Exception as e:
            print(f"❌ Erreur inattendue lors de la fermeture : {e}")
            return False
    
    def obtener_sesion_por_string(self, session_string):
        """
        Récupère les données complètes d'une session par son sessionString.
        
        Arguments :
        - session_string : String de session
        
        Retourne :
        - Dictionnaire avec les données de la session
        - None si non trouvée
        """
        
        try:
            response = self.table.scan(
                FilterExpression='sessionString = :ss',
                ExpressionAttributeValues={
                    ':ss': session_string
                }
            )
            
            items = response.get('Items', [])
            
            if not items:
                return None
            
            return items[0]
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération : {e}")
            return None