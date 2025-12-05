import os

# ===== CONFIGURACION AWS S3 =====

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'ASIAQKM3NNZIGSKYKDU5')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'AtCgsIah7w95oow3FqTKpJvuj4orq4VbuUyXHL4f')
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN', 'IQoJb3JpZ2luX2VjEFIaCXVzLXdlc3QtMiJHMEUCIQCCO/VD2E3b+zPsh4BZhioRXNyOEcNy/ohlpM1mVkM2jQIgZG+Aov+67Ixs/Dya8kTatdQxnRlHNv6CY/T1nvPuSAUquwIIGhACGgwwMjIzMzc2NDYxNjAiDFm5k4tK8f3PhNLVuiqYAnnAwUidpAco4HNb/JyjxzS2AgdNQH9jHTS46VhwtdUqcukQ6DJ4WV3kqaMT+F5m4XIf4V03OGn+QUdhaN9CUBFUGLtEtQBEywwvGP0SZhoFCvKv9nAlBegViynTXCaoqAOK0m2uR4m1peQNbtJJRdn5oSHKdDmF5hqD7DMcMxNzWN/fhKQopVvp5/knCyGifwNKSipR2WDo7PvsGp1oDcARaPpwISErnTZAUJYSNhUC6nKofuxm2YbxozC+wNXC+5+Os8eWR9A+tYTDbbx4QbCMTWShb+Y5unCdSgycUvMuO1Ve2KNKXeT33TxLe+MvRUT1oiFguQh45zK+qMuXkXXgUbeI+2Hqx+KPYiTyaxdaZ8CUBxNmuTMwi8C8yQY6nQFHh/lIYyohSzfux1UBUBmS6jc4VvChFeB3wozZpFiWbkdHlAvNgCy3dsffrmqCgik+RIn7c0NUUuzWUaa3zkDh6h3+0q8EmiQG7ELYzWoYuTm6dIdm5fqqRR11OZuXfYAdoxyZesVLtfpD1Osql2r7csYlOR0gvhtLzM2DTVzAdbWnaNg7bf9/PzmIXs6RZsele7y6QVPwXwU+yr2q')

AWS_REGION = 'us-east-1'

S3_BUCKET_NAME = 'm25090057-uady-aws-academy-proyecto-final'

S3_BASE_URL = f'https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com'

# ===== CONFIGURACION SNS =====
SNS_TOPIC_ARN = os.environ.get(
    'SNS_TOPIC_ARN',
    'arn:aws:sns:us-east-1:022337646160:uady-proyecto-final-notificacion'
)

# ===== CONFIGURACION DYNAMODB =====
DYNAMODB_TABLE_NAME = os.environ.get(
    'DYNAMODB_TABLE_NAME',
    'sesiones-alumnos'
)