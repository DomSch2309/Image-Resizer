import os

class Config:
    SECRET_KEY =  os.environ.get("secret_key")

#Datenbank Konfiguration
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWORD = ""
    DB_NAME = 'image_resizer_db'

#Upload Verzeichnis
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')

#Flask-Caching Konfiguration
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 86400