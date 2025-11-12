import mysql.connector.pooling
from flask import g, current_app

db_pool = None

#Initialisierung des DB-Pools beim Start der Anwendung

def init_db_pool(config):

    global db_pool
    try:
        db_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name = "image_resizer_pool",
            pool_size = 10,
            host = config["DB_HOST"],
            user = config["DB_USER"],
            password = config.get("DB_PASSWORD", ""),
            database = config["DB_NAME"]
        )
    except KeyError as e:
        raise RuntimeError(f"Fehler in der Konfiguration: {e} nicht in config.py gefunden.")
    except Exception as e:
        raise RuntimeError(f"Konnte DB-Pool nicht initialisieren: {e}")
    
#Verbindungsherstellung aus dem Pool für aktuelle Anfrage

def get_db():
    if 'db' not in g:
        g.db = db_pool.get_connection() 
    return g.db

#Rückgabe der Verbindung am Ende der Anfrage

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()