import boto3
from botocore.exceptions import ClientError
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION, SNS_TOPIC_ARN

class SNSService:
    
    def __init__(self):

        self.sns_client = boto3.client(
            'sns',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=AWS_REGION
        )
        self.topic_arn = SNS_TOPIC_ARN
    
    def enviar_notificacion_alumno(self, alumno):

        
        try:
            subject = f"Notificación de Alumno: {alumno.nombres} {alumno.apellidos}"
            
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
            
            response = self.sns_client.publish(
                TopicArn=self.topic_arn,
                Subject=subject,
                Message=message,
                MessageAttributes={
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
            
            message_id = response.get('MessageId')
            
            if message_id:
                print(f"Notificacion enviada. MessageId: {message_id}")
                return True
            else:
                print("Error : No MessageId retornado")
                return False
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"Error SNS [{error_code}]: {error_message}")
            return False
            
        except Exception as e:
            print(f"Error durante el envio del SNS : {e}")
            return False