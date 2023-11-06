import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')
PORT = os.getenv('PORT')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
WTF_CSRF_ENABLED = os.getenv('WTF_CSRF_ENABLED')
