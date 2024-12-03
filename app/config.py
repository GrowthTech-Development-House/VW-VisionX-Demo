import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'OJLj+eEsD5prn1Nd+SmEt6ogx1+A5HJdL37tqP1vMdswjmVWqpHbHu0th0Ki5NN+M2JoA1axP5Boks54TzzDbA==')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{os.getenv('DEV_DB_USER', 'root')}:"
        f"{os.getenv('DEV_DB_PASS', 'gtech')}@"
        f"{os.getenv('DEV_DB_HOST', 'localhost')}/"
        f"{os.getenv('DEV_DB_NAME', 'label_app')}?auth_plugin=mysql_native_password"
    )


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{os.getenv('PROD_DB_USER', 'prod_user')}:"
        f"{os.getenv('PROD_DB_PASS', 'prod_password')}@"
        f"{os.getenv('PROD_DB_HOST', 'prod_host')}/"
        f"{os.getenv('PROD_DB_NAME', 'label_app')}?auth_plugin=mysql_native_password"
    )