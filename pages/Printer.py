import streamlit as st
import requests
import serial
import pandas as pd
from tinydb import TinyDB, Query
#from datetime import datetime, timedelta
import datetime
import time
import json

def check_login():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.switch_page("Login.py")

check_login()

# IP-Adresse des Raspberry Pi über Tailscale
raspberry_pi_ip = "http://100.65.7.53:5002"

#printer_port = "/dev/ttyUSB0"
#baud_rate = 115200

st.title("3D-Drucker Web Interface")
# Hochladen von G-Code
temp_file = st.file_uploader("G-Code hochladen", type="gcode")
if temp_file is not None:
    files = {"file": temp_file}
    response = requests.post(f"{raspberry_pi_ip}/upload", files=files)
    st.success(response.json()["message"])

# G-Code-Dateien abrufen
if "files" not in st.session_state:
    st.session_state.files = []

if st.button("Liste der G-Code-Dateien aktualisieren"):
    response = requests.get(f"{raspberry_pi_ip}/files")
    if response.status_code == 200:
        st.session_state.files = response.json()
    else:
        st.error("Fehler beim Laden der Dateien")

# Auswahlmenü für die G-Code-Dateien
selected_file = st.selectbox("Wähle eine Datei", st.session_state.files, index=0 if st.session_state.files else None)

# Load the latest filament weight from the TinyDB
db = TinyDB('/app/MCI_IoT_Monitor3D/db/filament_weight.json')
Filament = Query()

# Find the latest weight entry based on the timestamp
entries_with_timestamp = [entry for entry in db.all() if 'timestamp' in entry]
if entries_with_timestamp:
    latest_entry = max(entries_with_timestamp, key=lambda x: datetime.datetime.fromisoformat(x['timestamp']))
    latest_filament_weight = latest_entry['weight']
else:
    latest_filament_weight = 0  # or handle this case as needed

if st.button("Datei anzeigen") and selected_file:
    file_response = requests.get(f"{raspberry_pi_ip}/view/{selected_file}")
    weight_response = requests.get(f"{raspberry_pi_ip}/get_weight/{selected_file}")
    if file_response.status_code == 200:
        col4, col5 = st.columns([1, 1])  # Erhöht den Anteil der Bildspalte
    with col4:
        weight_data = weight_response.json()
        file_weight = weight_data['weight']

        # Compare weights and determine the message and color
        if latest_filament_weight > file_weight + 10:
            weight_message = "Enough Filament loaded"
            weight_color = "green"
        elif latest_filament_weight >= file_weight:
            weight_message = "Maybe enough Filament loaded (Warning)"
            weight_color = "yellow"
        else:
            weight_message = "Not enough Filament loaded (Error)"
            weight_color = "red"

        st.text_area("Aktuelles Filamentgewicht", f"{latest_filament_weight}g", height=100)
        st.text_area("Dateigewicht", f"{weight_data['weight']}g", height=100)
        st.markdown(f"<p style='color:{weight_color};'>{weight_message}</p>", unsafe_allow_html=True)
        st.text_area("Dateiinhalt", file_response.text, height=150)
    with col5:
        st.image(f"{raspberry_pi_ip}/visualize/{selected_file}",
        caption="G-Code Visualisierung",
        use_container_width=True)



# Buttons für Aktionen
col2, col3 = st.columns(2)
with col2:
    if st.button("Druck starten") and selected_file:
        requests.post(f"{raspberry_pi_ip}/start", json={"filename": selected_file})
        st.success("Druck gestartet")

with col3:
    if st.button("Druck stoppen"):
        requests.post(f"{raspberry_pi_ip}/stop")
        st.warning("Druck gestoppt")


st.title("Raspberry Pi Video Stream")

# Video anzeigen
st.markdown(
    f"""
    <div style="text-align: center;">
        <iframe src="{raspberry_pi_ip}/video_feed" width="700" height="394" frameborder="0"></iframe>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("Druckerüberwachung")

# Platzhalter für den Druckerstatus und die Metriken
status_placeholder = st.empty()
metrics_placeholder = st.empty()

while True:
    try:
        response = requests.get(f"{raspberry_pi_ip}/status")
        if response.status_code == 200:
            data = response.json()
            # Beispielhafte Extraktion aus den verschachtelten Daten:
            # M27 liefert den Druckstatus als Liste im Schlüssel "response". Wir nehmen den ersten Eintrag.
            m27 = data.get("M27", {})
            printer_status = m27.get("response", ["Unbekannt"])[0] if m27.get("response") else "Unbekannt"
            
            # Extrahiere Temperaturwerte aus dem M105-Dictionary
            m105 = data.get("M105", {})
            nozzle_temp = m105.get("nozzle_temperature", "-")
            bed_temp = m105.get("bed_temperature", "-")
            
            # Extrahiere Positionen aus dem M114-Dictionary
            m114 = data.get("M114", {})
            x_val = m114.get("x", "-")
            y_val = m114.get("y", "-")
            z_val = m114.get("z", "-")
            
            # Extrahiere die Lüftergeschwindigkeit aus dem M106-Dictionary
            m106 = data.get("M106", {})
            fan_speed = m106.get("fan_speed", "-")
            
            status_placeholder.markdown(f"**Druckerstatus (M27):** {printer_status}")
            
            # Erstelle sechs Spalten zur Anzeige der Kennzahlen
            col1, col2, col3, col4, col5, col6 = metrics_placeholder.columns(6)
            col1.metric("Nozzle Temp", f"{nozzle_temp} °C" if nozzle_temp != "-" else "-")
            col2.metric("Bed Temp", f"{bed_temp} °C" if bed_temp != "-" else "-")
            col3.metric("X", x_val)
            col4.metric("Y", y_val)
            col5.metric("Z", z_val)
            col6.metric("Fan Speed", f"{fan_speed} %" if fan_speed != "-" else "-")
    except Exception:
        status_placeholder.markdown("**Druckerstatus:** Printer disconnected")
        col1, col2, col3, col4, col5, col6 = metrics_placeholder.columns(6)
        col1.metric("Nozzle Temp", "-")
        col2.metric("Bed Temp", "-")
        col3.metric("X", "-")
        col4.metric("Y", "-")
        col5.metric("Z", "-")
        col6.metric("Fan Speed", "-")
    
    time.sleep(2)

