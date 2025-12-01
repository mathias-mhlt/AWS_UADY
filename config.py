import os

# ===== CONFIGURATION AWS S3 =====
# Ces valeurs proviennent de "AWS Details" dans AWS Academy

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'ASIAQKM3NNZID6JNDOMM')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'q0zAdV0pIREu3dHLFrTiQMHVmRhqCniEoAbGqjUg')
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN', 'IQoJb3JpZ2luX2VjEDgaCXVzLXdlc3QtMiJGMEQCIAV+sAZhTnA/12jbaVo/Mrzu8fRq7FeImbLTqS6f+x8LAiAn3tUuozc1i2jsvmj7kC01cBfomhOJjxQEoXEcUNJUziq7AggBEAIaDDAyMjMzNzY0NjE2MCIMKAWnffR9vOEe7rRHKpgC9fUYdiyDdhH/eEm1lT40pGtxHXGVfYzd6wDlSus8lgqDgwH/7zDav3NDqsweMHGgQk75PEGUnV7Fefhi4J9D9nWw0nZQUdIGA5R3pp2w2preTIgAblrAqKkaOJpRfRo6RkLzHjqiiRC8icNbD+a+R1A3JY7j/xhWBJkRAJEdi0zQCizmdr5frMnV8f1rG1KXIJdnMEo4OAkfzBXMWqH1mG6TFOhd9p+/A6KHVqCkJo7pbDNBThF9co4gk8szokJ5GhlZ89hY/cLBETxGC8oIPvsz+p+/qWWbylK65Y5wS53eNj0zrCP1VPBb6hFLvMGEjqy8WTbLDQQpyNTI3qvBqzawyCCmrScLYye8xtfPzNfTcy1nc+eWLzDS9rbJBjqeAfU1eXt/8OSVWXEX2Vg0eGkc0815cZJuUhL4GlK4rK3/AqbNQllyLWTQ+2c/kmRV1NHk3PtefIGz00HwYsGaRZ2iF6pf/hg9idyLm+DAIGVaxSY4zUy2sjEpJfJU/BlKI41qTq97AUxMJf8jEO2QKJFPDoxwOZG7I1OxJvdpy/1/qXjVZHS9GKMm2Ms/BUhNYrsT5leQL2ROyxie5Xyt')

# Région AWS (doit correspondre à votre bucket)
AWS_REGION = 'us-east-1'

# Nom de votre bucket S3
S3_BUCKET_NAME = 'm25090057-uady-aws-academy-proyecto-final'  # ⚠️ MODIFIER avec votre nom de bucket

# URL de base pour accéder aux fichiers
S3_BASE_URL = f'https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com'

# ===== CONFIGURATION SNS =====
# ARN du topic SNS pour les notifications
SNS_TOPIC_ARN = os.environ.get(
    'SNS_TOPIC_ARN',
    'arn:aws:sns:us-east-1:022337646160:uady-proyecto-final-notificacion'
)