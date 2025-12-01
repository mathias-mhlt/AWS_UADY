import boto3
from botocore.exceptions import ClientError
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION, SNS_TOPIC_ARN

class SNSService:
    """
    Service pour envoyer des notifications par email via SNS.
    """
    
    def __init__(self):
        """
        Initialise le client SNS avec les credentials AWS.
        
        Logique :
        - boto3.client('sns') crée une connexion authentifiée à SNS
        - Les credentials proviennent de config.py
        """
        self.sns_client = boto3.client(
            'sns',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=AWS_REGION
        )
        self.topic_arn = SNS_TOPIC_ARN
    
    def enviar_notificacion_alumno(self, alumno):
        """
        Envoie une notification avec les informations d'un alumno.
        
        Arguments :
        - alumno : Objet Alumno (model SQLAlchemy)
        
        Retourne :
        - True si envoyé avec succès
        - False en cas d'erreur
        
        Logique :
        1. Construire le sujet du message
        2. Construire le corps du message (informations de l'alumno)
        3. Publier sur le topic SNS
        4. SNS envoie automatiquement à tous les abonnés
        """
        
        try:
            # ===== CONSTRUCTION DU SUJET =====
            subject = f"Notificación de Alumno: {alumno.nombres} {alumno.apellidos}"
            
            # ===== CONSTRUCTION DU CORPS DU MESSAGE =====
            message = f"""
Hola,

Se ha solicitado el envío de información del siguiente alumno:

INFORMACIÓN DEL ALUMNO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Nombre completo: {alumno.nombres} {alumno.apellidos}
 Matrícula: {alumno.matricula or 'No especificada'}
 Promedio: {alumno.promedio if alumno.promedio is not None else 'No especificado'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Este mensaje fue generado automáticamente por el sistema UADY-AWS.

Saludos cordiales,
Sistema de Gestión de Alumnos
            """.strip()
            
            # ===== PUBLICATION SUR SNS =====
            response = self.sns_client.publish(
                TopicArn=self.topic_arn,     # Topic cible
                Subject=subject,              # Sujet de l'email (optionnel)
                Message=message,              # Corps du message
                MessageAttributes={           # Métadonnées optionnelles
                    'AlumnoID': {
                        'DataType': 'Number',
                        'StringValue': str(alumno.id)
                    },
                    'Matricula': {
                        'DataType': 'String',
                        'StringValue': alumno.matricula or 'N/A'
                    }
                }
            )
            
            # ===== VÉRIFICATION DU SUCCÈS =====
            # SNS retourne un MessageId si succès
            message_id = response.get('MessageId')
            
            if message_id:
                print(f"Notification envoyée avec succès. MessageId: {message_id}")
                return True
            else:
                print("Erreur : Pas de MessageId retourné")
                return False
            
        except ClientError as e:
            # Erreur AWS (permissions, ARN invalide, etc.)
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"Erreur SNS [{error_code}]: {error_message}")
            return False
            
        except Exception as e:
            # Autre erreur
            print(f"Erreur inattendue lors de l'envoi SNS : {e}")
            return False