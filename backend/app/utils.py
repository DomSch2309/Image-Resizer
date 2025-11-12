import requests
import uuid
import os
from PIL import Image


#Bild herunterladen, ändern und speichern
def process_image(url: str, width: int, height: int, upload_folder: str) -> str:
    
    headers={
        'User_Agent': 'Mozilla/5.0 (Windows NT 10.0); Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    } 

    try:
        response = requests.get(url, stream = True, timeout = 10, headers = headers) # HTTP get Anfrage
        response.raise_for_status()                                                  # löst Fehlermeldung bei 4xx/5xx aus

        #Bild mit Pillow öffnen, verändern, speichern
        with Image.open(response.raw) as im:
            im.thumbnail((width, height), Image.Resampling.LANCZOS)                  # mit thumbnail() werden Proportionen beibehalten
            ext = im.format.lower() if im.format else 'jpeg'
            new_filename = f"{uuid.uuid4()}.{ext}"                                   # erstellt zufälligen, neuen namen
            save_path = os.path.join(upload_folder, new_filename)
            im.save(save_path)

        return new_filename
    
    # Error-Handling (Download, Bearbeitung)
    except requests.RequestException as e:
        raise IOError(f"Bild-Download fehlgeschlagen: {e}")
    except IOError as e:
        raise IOError(f"Bildverarbeitung fehlgeschlagen: {e}")