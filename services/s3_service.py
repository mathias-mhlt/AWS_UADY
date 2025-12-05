import boto3
from botocore.exceptions import ClientError
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION, S3_BUCKET_NAME, S3_BASE_URL
import uuid
import os

class S3Service:
    
    def __init__(self):

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=AWS_REGION
        )
        self.bucket_name = S3_BUCKET_NAME
    
    def upload_foto_perfil(self, file, alumno_id):

        if not file:
            return None
        
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        if file_extension not in allowed_extensions:
            raise ValueError(f"Extension prohibida. Utiliza : {', '.join(allowed_extensions)}")
        
        unique_id = str(uuid.uuid4())[:8]
        file_key = f"alumnos/{alumno_id}/perfil_{unique_id}{file_extension}"
        
        try:
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                file_key,
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': file.content_type
                }
            )
            
            file_url = f"{S3_BASE_URL}/{file_key}"
            
            return file_url
            
        except ClientError as e:
            print(f"Error S3 : {e}")
            return None
        except Exception as e:
            print(f"Error : {e}")
            return None