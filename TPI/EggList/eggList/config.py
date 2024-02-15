import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = os.getenv("SECRET_KEY")
SECURITY_PASSWORD_SALT = SECRET_KEY
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

