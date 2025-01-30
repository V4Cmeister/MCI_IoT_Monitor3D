import streamlit as st
import requests
import serial

# IP-Adresse des Raspberry Pi über Tailscale
raspberry_pi_ip = "http://100.93.75.50:5002"

printer_port = "/dev/ttyUSB0"
baud_rate = 115200

st.title("Raspberry Pi Video Stream")

# Video anzeigen
st.markdown(
    f"""
    <div style="text-align: center;">
        <iframe src="{raspberry_pi_ip}/video_feed" width="640" height="480" frameborder="0"></iframe>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("Das ist der Live-Stream vom Raspberry Pi!")

# Datei-Upload für G-code
st.header("G-code hochladen")
uploaded_file = st.file_uploader("Lade eine G-code-Datei hoch", type=["gcode"])
if uploaded_file is not None:
    # Speichere die Datei lokal
    gcode_path = f"/tmp/{uploaded_file.name}"
    with open(gcode_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success(f"Datei {uploaded_file.name} erfolgreich gespeichert!")

    # Druck starten
    if st.button("Drucken starten"):
        try:
            # Datei an den Drucker senden
            with serial.Serial(printer_port, baud_rate, timeout=2) as ser:
                with open(gcode_path, "r") as file:
                    for line in file:
                        ser.write((line.strip() + "\n").encode())
                        ser.flush()
            st.success("Druck erfolgreich gestartet!")
        except Exception as e:
            st.error(f"Fehler beim Drucken: {e}")