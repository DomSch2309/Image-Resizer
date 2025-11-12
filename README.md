Anwendung:
- Webanwendung über die der User eine HTTP URL, welche auf ein Bild verweist, einreichen  und gewünschte maximale Höhe und Breite (in Pixeln) eingeben kann. Die Anwendung gibt dann eine zufällig generierte URL zurück, welche wiederum auf das neu erstellte Bild verweist.

Anforderungen:
- Einreichen einer URL mit Bildverweis
- Eingabe von gewünschter Höhe und Breite in Pixeln
- zufällig generierte URL für das neue Bild
- Originale Proportionen sollen beibehalten werden
- Bild soll Serverseitig gecached werden
- ist das gecachte Bild älter als 24 Stunden, und eine Aktualisierung der URL schlägt fehl, sollte das alte gecachte Bild weiter verwendet werden
- API
	- API-Calls
		- Ändern der Größe eines Bildes, mittels URL, Höhe und Breite
		- Löschen eines Bilds mit gegebener URL
		- Auflistung der bearbeiteten Bilder
- Frontend:
	- Einfügen der Ziel-URL, Zielgröße und Zielbreite
	- Liste der bearbeiteten Bilder (Liste der URLs?)
	- Möglichkeit die Bilder anzuschauen
	- Möglichkeit die Bilder zu löschen

Verwendete Technologien:
- Programmiersprache: Python
- Bibliotheken/Frameworks:
	- Flask: 
		- JSON-API, Webzugriff, API-Calls, hochladen des veränderten Bildes
	- request:
		- herunterladen des Bildes
	- Pillow:
		- Bearbeitung des Bildes
	- Nice-GUI:
		- Frontend
	- MySQL-Connector
		- Datenbankanbindung zum MySQL Community Server
  - Datenbank:
    - MySQL
   

Anwendung starten:
  - Vorraussetzungen:
    - Python(3.8 oder neuer)
    - Git
    - MySQL Server
   
1. Repository klonen
2. Bibliotheken/Frameworks aus "requirements.txt" installieren
3. Datenbank Setup:
   - Quelltext aus SQL_Datenbank.txt auf MySQL aufspielen
4. In /app/config.py Datenbankdaten ergänzen (Host, User, Password, DB-Name)
5. run.py ausführen
6. http://127.0.0.1:5000 aufrufen

Bis hierher sollte die Anwendung funktionieren, das Frontend habe ich nicht zum Laufen bekommen. 
