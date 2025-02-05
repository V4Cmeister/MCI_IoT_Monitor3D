import streamlit as st
from credentials_page import credentials

st.set_page_config(
    page_title="Monitor3D",
    page_icon="🖨️",
)

def login():
    st.write("# Monitor3D")
    st.sidebar.error("Login for access!")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in credentials and credentials[username] == password:
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid username or password")
    if st.button("GUEST Login"):
        st.session_state["logged_in"] = True
        st.rerun()

    st.markdown(
            """
            - **Printer:** Start a print job.
            - **Reservation:** Book a slot if the printer is currently in use.
            - **Status:** Display the dashboard and enable video monitoring.
            """
        )

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    st.sidebar.success("Logged in!")
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()