import os

# ===== CONFIGURATION AWS S3 =====
# Ces valeurs proviennent de "AWS Details" dans AWS Academy

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'ASIAQKM3NNZIEKO5RM3U')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'Ib5lmpVNGzGh0N0FCggqw20ljV0F05X4KGpgpAOW')
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN', 'IQoJb3JpZ2luX2VjECgaCXVzLXdlc3QtMiJIMEYCIQDgnZXgXKBwxPdBzQLo4W4OzGSOabdTDOhy0PPt8yE2HgIhAK6/JWxPsC56N8ylVDfbR+oO8dvWoCrm+XKRMUhsWR/MKsQCCPH//////////wEQAhoMMDIyMzM3NjQ2MTYwIgw0b/rAE02JL+jpmsoqmAJY/Ph5gmMiUC+W8W9XH5u17emM6+QgFupWdjVVAZeHZClli2X1CG4aIcUhu5Qqv7Sqn6lmYVSWPSCvFm5Y8o1FNRB2eejG1jhcoXYgS603llRmKyM1ZAoxXGOI1W7lreoJZY6Y8y653ucNmOa7RijDRq38UEuRd0jLVLsudCLYh97Ih6D5EIG9P8AeFOQHXNdeKAt85VH/tgCDDu0G5GZea0h+kI09/udvK5vYispHfVEqyvb0IlwPvVjyVa2A3IWn/gNTp1jDsdCMTYXOaM70qYRY8Z5Zf6YsT1l530DjZv+lLK79JCH7bJY37rhoGK7DI5lVbZxUqhgoZo1n1hh6zL4LB6rUMylHHhgigo8clMfowPW27NmDMOe1s8kGOpwBPNsQydXR/pTGx/xhxAe1GgkTuAsKWW1D4UuFo0TGfik69M2Ma80AsJhUiEThUY+W9e9cImhKXXRrgfxtCqla0LeWC5ceqgO6tpOSpwEDDia8q0s7PYMPS3zs655lzX5IjJbI7OO5RC9mc9n76qQ6hmUZtKoO0l9Mjt/DEzfYvWWn1AqrIpoWnirLwsuQb1FF726/f1wfaRfc/5tO')

# Région AWS (doit correspondre à votre bucket)
AWS_REGION = 'us-east-1'

# Nom de votre bucket S3
S3_BUCKET_NAME = 'm25090057-uady-aws-academy-proyecto-final'  # ⚠️ MODIFIER avec votre nom de bucket

# URL de base pour accéder aux fichiers
S3_BASE_URL = f'https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com'