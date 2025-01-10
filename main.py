import streamlit as st

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
