import os
from datetime import datetime, timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_sevret_key' # This key is not in use .
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///data.db' #you can change the name of the .db file
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt_secret_key' #You can change the secret key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    
