import os
from flask import Flask, jsonify
from config import Config
from app import db
from app.extensions import cache



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True) #stellt sicher, dass Upload ordner existiert

    import flask_caching
    print("Flask-Caching Modul:", flask_caching.__file__)
    #Initialisierung von Erweiterungen
    cache.init_app(app) 
    db.init_db_pool(app.config)

    app.do_teardown_appcontext(db.close_db) #Teardownfunktion um DB-Verbindung zu schließen


    # Blueprints registrieren
    from .api_v1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix = '/api/v1')

    from .media import bp as media_bp
    app.register_blueprint(media_bp)

    
    #Globales JSON Fehlerhandling
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not Found"}), 404 
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error"}), 500 
    
    return app


