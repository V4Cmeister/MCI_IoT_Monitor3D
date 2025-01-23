import streamlit as st

""" import paho.mqtt.client as mqtt
from credentials import MQTT_USERNAME, MQTT_PASSWORD, MQTT_BROKER, MQTT_PORT

# Define the callback function for when a message is received
def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")

# Define the callback function for when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected successfully")
        # Subscribe to a topic
        client.subscribe("Filament_Supervision/Microcontroller_Last_Seen")
    else:
        print(f"Connection failed with code {rc}")

# Create an MQTT client instance
client = mqtt.Client()

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the loop to process received messages
client.loop_forever() """

def main():
    # Set Streamlit app to centered layout
    st.set_page_config(page_title="Uni Login", layout="centered")

    # Dummy user data
    users = {
        "N.Soukopf": "Test",
        "L.Maier": "Test"
    }

    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["username"] = ""

    # Login logic
    if not st.session_state["authenticated"]:
        st.title("Login")

        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")

        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Ungültiger Benutzername oder Passwort.")
    else:
        st.success(f"Login erfolgreich! Willkommen, {st.session_state['username']}!")
        st.write("Success")

        if st.button("Logout"):
            st.session_state["authenticated"] = False
            st.session_state["username"] = ""
            st.rerun()

if __name__ == "__main__":
    main()
