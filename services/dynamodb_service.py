import boto3
from botocore.exceptions import ClientError
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION, DYNAMODB_TABLE_NAME
import uuid
import time
import secrets

class DynamoDBService:

    
    def __init__(self):

        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=AWS_REGION
        )
        self.table = self.dynamodb.Table(DYNAMODB_TABLE_NAME)
    
    def generar_session_string(self, length=128):

        return secrets.token_hex(length // 2)
    
    def crear_sesion(self, alumno_id):
        
        try:
            session_id = str(uuid.uuid4())
            session_string = self.generar_session_string(128)
            timestamp = int(time.time())
            
            session_data = {
                'id': session_id,
                'fecha': timestamp,
                'alumnoId': alumno_id,
                'active': True,
                'sessionString': session_string
            }
            
            self.table.put_item(Item=session_data)
            
            print(f"Sesion creada : ID={session_id}, AlumnoID={alumno_id}")
            
            return session_data
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"Error DynamoDB [{error_code}]: {error_message}")
            return None
            
        except Exception as e:
            print(f"Error durante la creacion de la sesion : {e}")
            return None
    
    def verificar_sesion(self, session_string):
        
        try:

            response = self.table.scan(
                FilterExpression='sessionString = :ss',
                ExpressionAttributeValues={
                    ':ss': session_string
                }
            )
            
            items = response.get('Items', [])
            
            if not items:
                print(f"Ninguna sesion encontrada con esta sessionString")
                return False
            
            session = items[0]
            
            is_active = session.get('active', False)
            
            if is_active:
                print(f"Sesion valida : ID={session['id']}, AlumnoID={session['alumnoId']}")
                return True
            else:
                print(f"Sesion inactiva : ID={session['id']}")
                return False
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"Error DynamoDB [{error_code}]: {error_message}")
            return False
            
        except Exception as e:
            print(f"Error durante la verificacion : {e}")
            return False
    
    def cerrar_sesion(self, session_string):
        
        try:
            response = self.table.scan(
                FilterExpression='sessionString = :ss',
                ExpressionAttributeValues={
                    ':ss': session_string
                }
            )
            
            items = response.get('Items', [])
            
            if not items:
                print(f"Ninguna sesion encontrada con esta sessionString")
                return False
            
            session = items[0]
            session_id = session['id']
            
            self.table.update_item(
                Key={'id': session_id},
                UpdateExpression='SET active = :val',
                ExpressionAttributeValues={
                    ':val': False
                }
            )
            
            print(f"Sesion cerrada : ID={session_id}")
            return True
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"Error DynamoDB [{error_code}]: {error_message}")
            return False
            
        except Exception as e:
            print(f"Error durante la cerrada : {e}")
            return False
    
    def obtener_sesion_por_string(self, session_string):
        
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
            print(f"Error durante la recuperacion : {e}")
            return None