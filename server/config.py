from dotenv import load_dotenv
import os
load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    PASSWORD = os.getenv('PASSWORD')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{PASSWORD}@db:3306/dashboard'

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False