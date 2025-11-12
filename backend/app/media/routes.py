from flask import Blueprint, send_from_directory, current_app

bp = Blueprint('media', __name__)

@bp.route('/media/<path:filename>')
#liefert Dateien aus dem UPLOAD_FOLDER
def serve_media(filename):
    return send_from_directory(current_app.config, filename)