import streamlit as st
import pandas as pd
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
import time

def check_login():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.switch_page("Login.py")

check_login()

# Initialize TinyDB
db = TinyDB('/app/MCI_IoT_Monitor3D/db/filament_weight.json')
Weight = Query()

# Streamlit setup
st.set_page_config(page_title="Filament Observer", page_icon="📈")
st.markdown("#Filament Observer")
st.sidebar.header("MQTT Plotting Demo")
st.write(
    """Filamentgewichtsdaten werden von einem ESP32-Mikrocontroller über MQTT empfangen und in einer TinyDB-Datenbank gespeichert."""
)

chart = st.empty()

# Keep the script running and update the chart in the main thread
while True:
    # Remove data older than 7 days
    seven_days_ago = datetime.now() - timedelta(days=7)
    db.remove(Weight.timestamp < seven_days_ago.isoformat())

    # Get data from the last 24 hours
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    recent_data = db.search(Weight.timestamp >= twenty_four_hours_ago.isoformat())

    # Convert to pandas DataFrame for plotting
    if recent_data:
        df = pd.DataFrame(recent_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')
        df = df.resample('1T').mean().interpolate()  # Resample to 1-minute intervals and interpolate missing values
        chart.line_chart(df['weight'])

    time.sleep(1)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")