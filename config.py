import os

# ===== CONFIGURACION AWS S3 =====

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'ASIAQKM3NNZIDXBOYKSY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'A215do1vnk/xcWUUFiAv1LDEKzT9Sp/7I8KkmYC7')
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN', 'IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCIE0Z1tbg/4UJ1J0yY3F2EjuqX1JU3BLlNU6LJFQjmqsHAiAoXztXLKMMB26A+wMgLiZ+dDC+yhG/57fnvxr6HJof7irEAgji//////////8BEAIaDDAyMjMzNzY0NjE2MCIMSMyqT5vjdWwnlbbRKpgCuBKEsDvmphwHwS0aGagc7DUONKUiaV1t0PmOwZ5s74AWoSZiHtegZjGim0sGxkFaKdKENbt9j8eGKNuYWTBeFLso0h2vDSKdWQdQ4o3EoQ6oLHR1bRjhd6UzfbKHkeImsJxc719zyRYpYTbX0XotGNuzHoO4fXYnU1Iv2sAnG9hqfOfM//njYpBg98EC4iDf9CcZe2KvhG4j3+uoXuKAcFJMhtrlmRWcJZ9Ib7J1Gln+flychImbDeD+e8S/cmtP4DDoVg/yP8belWXjvWET6KHgmrQ3GWAp17yWBZbGx5DZ8VrK5z9UravtWBU45HePdX/rwOklI3d+Rsx8u7msLCu9pQnFjfM1HehPSnpNh4ytzFG74DkY4DDns+jJBjqeAZ4jArhz+TTXTMRC0xQaOtN3Qnqp7HibhQjJt1+6LxEwsVzmkTIzIa192OnXf7iUDX06pRenjsYklxxcfmsXtajeaC8oriTH2qm5QjMit1z4ixZz1x5jzZVO5cn/Uj4XfVH+uEZMGJWsyx+luvS6NylLxh+ftrmfD6ZUaq1aQmfhwL25pps0bssUcH4939AWudAhNenkleYvMlmKB/On')

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