import os
import hashlib
import json
from flask import Blueprint, request, jsonify, current_app, url_for
from ..extensions import cache
from ..db import get_db
from ..utils import process_image

bp = Blueprint('api_v1', __name__)

# Cache Schlüssel erstellen
def make_resize_cache_key(*args, **kwargs):

    try:
        json_data = request.get_json()                                                      # get_json zum parsen
        if not json_data:
            return request.path
        
        s = json.dumps(json_data, sort_keys=True)                                           # Sortierung der Schlüssen und erstellen des Hashwerts
        hash_str = hashlib.md5(s.encode()).hexdigest()
        return f"resize_post_{hash_str}"
    except Exception:
        return request.path                                                         

# Endpunkt zum Ändern der Bildgröße    
@bp.route('/resize', methods = ["Post"])
@cache.cached(timeout=86400)
def resize_image():

    data = request.get_json()
    if not data or 'url' not in data or 'width' not in data or 'height' not in data:
        return jsonify({"error": "ungültige Eingeabe"}), 400
    
    try:
        width = int(data['width'])
        height = int(data['height'])

        new_filename = process_image(                                                           # Bildbearbeitung
            data['url'], width, height, current_app.config
        )
        
        db = get_db()                                                                           # speichern in der DB
        cursor = db.cursor()
        query = ("Insert into processed_images "
                 "(original_url, new_filename, target_width, target_height)"
                 "Values (%s, %s, %s, %s)")
        cursor.execute(query, (data['url'],new_filename, width, height))
        db.commit()
        new_id = cursor.lastrowid
        cursor.close()

        new_media_url = url_for('media.serve_media', filename=new_filename, _external=True)    # Zufällige URL erstellen
        return jsonify({
            "id": new_id,
            "new_url": new_media_url,
            "original_url": data['url'],
            "target_width": width,
            "target_height": height,
            "cached": False

        })
    
    except Exception as e:
        return jsonify({"error": str(e)}),

# Auflistung der bearbeiteten Bilder
@bp.route('/images', methods = ["Get"])
def list_images():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("Select * From processed_images order by created_at DESC")
    images = cursor.fetchall()
    cursor.close()

    for img in images:
        img['new_url'] = url_for('media.serve_media', filename = img['new_filename'], _external = True)     # dynamische Generierung für Einträge

    return jsonify({"images": images})

# Löschen von Bildern aus DB und Dateisystem
@bp.route('/image/<int:image_id>', methods = ["Delete"])
def delete_image(image_id):
    db = get_db()
    cursor = db.cursor(dictionary = True)
    cursor.execute("Select * From processed_images where id = %s", (image_id))                              # Bild Infos aus DB abrufen
    image = cursor.fetchone()
    if not image:
        cursor.close()
        return jsonify({"error": "Bild nicht gefunden"}), 404
    
    original_request_data = {
        "url": image['original_url'],
        "width": image['target_width'],
        "height": image['target_height']
    }

    # Cache Invalidierung/Rekonstruktion JSON_Body
    s = json.dumps(original_request_data, sort_keys=True)
    hash_str = hashlib.md5(s.encode()).hexdigest()
    cache_key = f"resize_post_{hash_str}"
    cache.delete(cache_key)

    # Datei vom Dateisystem löschen
    try:
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], image['new_filename'])
        if os.path.exists(file_path):
            os.remove(file_path)
    except OSError as e:
        current_app.logger.error(f"Fehler beim Löschen der Datei: {e}")

    # DB-Eintrag löschen
    cursor.execute("Delete from processed_images Where id = %s", (image_id,))
    db.commit()
    cursor.close()

    return '', 204