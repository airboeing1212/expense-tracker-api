import os
from datetime import datetime, timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_sevret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    
