import httpx
from nicegui import ui, app

#URl zum Flask-Backend
api_base_url = "http://127.0.0.1:5000/api/v1"

#asynchroner HTTP-Client
api_client = httpx.AsyncClient(base_url = api_base_url)


# 1. UI-Layout definieren

# Eingabefelder Haupt-Layout

with ui.card().classes('w-full max-w-lg mx-auto'):
    ui.label('Neues Bild verarbeiten').classes('text-h6')
    url_input = ui.input(label = 'Bild-URL', placeholder='http://...')
    with ui.row():
        width_input = ui.input(label = 'Ziel-Breite').props('type="number"')
        height_input = ui.input(label = 'Ziel_Höhe').props('type="number"')

    submit_button = ui.button('Bearbeiten', on_click = lambda: submit_resize())

ui.separator().classes('my-6')

# leere Tabelle erstellen + Spaltendefinition
columns = {
    "name": "preview",
    "label": "Vorschau"
}
ui.label('Verarbeitete Bilder').classes('text-h5')
image_table = ui.table(columns=columns, rows=(''), row_key='id').classes('w-full')


# 2. Asynchrone API-Funktionen

# Aktualisiert die Tabelle
async def update_table():
    try:
        response = await api_client.get('/images')
        response.raise_for_status()
        image_table.rows = response.json().get('images',)
    except httpx.RequestError as e:
        ui.notify(f"Fehler beim Laden der Bilder: {e}", color="negative")
    image_table.update()

# Löscht ein Bild über API und aktualisiert die Tabelle
async def delete_image(image_id: int):
    try:
        response = await api_client.delete(f"/image/{image_id}")
        response.raise_for_status()
        ui.notify("Bild erfolgreich gelöscht", color = 'positive')
        await update_table()
    except httpx.RequestError as e:
        ui.notify(f"Fehler beim Löschen: {e}", color = "negative")

# Sendet Daten an den /resize Endpunkt
async def submit_resize():
    if not url_input.value or not width_input.value or not height_input.value:
        ui.notify("Bitte alle Felder ausfüllen", color = "warning")
        return
    
    data = {
        "url": url_input.value,
        "width": int(width_input.value),
        "height": int(height_input.value)
    }

    submit_button.set_text("Bearbeite...")
    submit_button.disable()
    try:
        response = await api_client.post('/resize', json = data, timeout = 30.0)
        response.raise_for_status()

        ui.notify("Bild erfolgreich bearbeitet", color = 'positive')
        url_input.value, width_input.value, height_input.value = "", "", ""
        await update_table()
    
    except httpx.HTTPStatusError as e:
        error_msg = e.response.json().get("error", "Unbekannter API-Fehler")
        ui.notify(f"Fehler: {error_msg}", color = "negative")
    except httpx.RequestError as e:
        ui.notify(f"Netzwerkfehler: {e}", color = "negative")
    finally:
        submit_button.set_text("Bearbeiten")
        submit_button.enable

# 3. Tabellen Slots

with image_table.add_slot("body-cell-preview"):
    ui.images().bind_source_from(app.storage.extra, "props", lambda p: p["row"]["new_url"]).classes("w-32 h32 object cover")

with image_table.add_slot("body-cell dimensions"):
    ui.label().bind_text_from(app.storage.extra, "props", lambda p:f"{p["row"]["target_width"]} * {p["row"]["target_height"]}" )

with image_table.add_slot("body-cell-actions"):
    ui.button(icon="delete", color = "red", on_click=lambda: delete_image(app.storage.extra["props"]["row"]["id"])).props("flat round dense")

# Initiales Laden

app.on_startup(update_table)

ui.run()
