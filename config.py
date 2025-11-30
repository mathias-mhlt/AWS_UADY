import os

# ===== CONFIGURATION AWS S3 =====
# Ces valeurs proviennent de "AWS Details" dans AWS Academy

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'ASIAQKM3NNZIIDSQQXX4')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '63T2lTNqfAxxAyEA6AD/mMDvgjtwbVFUozCwBcMj')
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN', 'IQoJb3JpZ2luX2VjEBwaCXVzLXdlc3QtMiJHMEUCIQDCcryblYXgmFpc1xAn7oUI4xK9WMsWPMCF6kBjyo/8jQIgd7Hh5Jh9Zsq03tpKYGxlYDhXfR0QkhFMBuhGat7QBmIqxAII5f//////////ARACGgwwMjIzMzc2NDYxNjAiDPh0zLcPbTmA+miFDSqYAiPehktbeL5r0V5W14J6pvci2/Wd5ghfUiT6MD0g6ZzArLynwqWaoyXPuzB6TDGSXy9KN5faZy1yl+B5qbFA2gi99L+9/NzG8xR9w2AxfiO7HderQ/j4RSLdvKmV1WLUfLRskUP40X0aGTt5yEDnWYsEH/5T1gBU3IiwFrmb7B0aOecDbgxQrPJHMK3Nu9363+e6ZOmkz13UZDNmQCzeGBuC0ybcDhg+oLxCTPD5oXZxOEBhwofSw/OJVIXXah3l9R26LYNhwCP1q3pjDd/YS+cPbDfv54K5MHJq+Vd7qxu8mVXHnh+sjckaREdZFCZZEAXSz9OQjEpq/E59FB87fXWVyWPSS7nUGrK0sJtIAGEDQPUk4lVJgtcw6uOwyQY6nQHaOG09XNzoqQ/o6bIeMx8h3jTwY2eG5fS24wiYq2QAPLeK8BIr9v5EmlA6zJnEpSJbOnaFB8wVx3ch3MdQ1DkJXxmuDS/IajzbScG4aW+dDC6Q/huQ/Rgt+YUo1YE/wTh73me6qvcRTdVPuoVuATvL8bM43rdD5bkX23000rSlpjkMPIZNz8LcrZ8nLyKMxt9CFL/7aVurj+6uWUbH')

# Région AWS (doit correspondre à votre bucket)
AWS_REGION = 'us-east-1'

# Nom de votre bucket S3
S3_BUCKET_NAME = 'm25090057-uady-aws-academy-proyecto-final'  # ⚠️ MODIFIER avec votre nom de bucket

# URL de base pour accéder aux fichiers
S3_BASE_URL = f'https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com'