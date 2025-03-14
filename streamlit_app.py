import streamlit as st
import pandas as pd
import json
import os
import pyrebase

# Firebase konfigurace
firebase_config = {
    "apiKey": "AIzaSyAE0isG9T7Jn4zzauLmWNdRf2Acxr-cUrE",
    "authDomain": "betmastery-e028e.firebaseapp.com",
    "projectId": "betmastery-e028e",
    "storageBucket": "betmastery-e028e.firebasestorage.app",
    "messagingSenderId": "399566379009",
    "appId": "1:399566379009:web:d095f7d903ac5232fb8800",
    "measurementId": "G-PGNMJ4KGS7"
}

# Inicializace Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

st.set_page_config(page_title="betmastery")

st.markdown("""
    <style>
        body {
            background: linear-gradient(180deg, hsl(241, 100%, 10%) 0%, hsl(75, 93%, 74%) 100%);
            color: white;
            font-family: Arial, sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Přihlašovací formulář
st.sidebar.title("Přihlášení")
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Heslo", type="password")

if st.sidebar.button("Přihlásit se"):
    try:
        # Přihlášení uživatele
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state["user"] = user
        st.sidebar.success("Přihlášení úspěšné!")
    except Exception as e:
        st.sidebar.error("Chyba při přihlašování!")

if st.sidebar.button("Odhlásit se"):
    st.session_state.pop("user", None)
    st.sidebar.success("Odhlášení úspěšné!")

# Registrování nových uživatelů
st.sidebar.subheader("Registrace")
new_email = st.sidebar.text_input("Nový email")
new_password = st.sidebar.text_input("Nové heslo", type="password")

if st.sidebar.button("Registrovat"):
    try:
        # Registrace nového uživatele
        auth.create_user_with_email_and_password(new_email, new_password)
        st.sidebar.success("Registrace úspěšná! Přihlaste se.")
    except Exception as e:
        st.sidebar.error("Chyba při registraci!")

# Soubor pro uložení tiketů
DATA_FILE = "tikety.json"

def load_tikety():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_tikety(tikety):
    with open(DATA_FILE, "w") as file:
        json.dump(tikety, file)

if "tikety" not in st.session_state:
    st.session_state.tikety = load_tikety()

st.title("Sázková statistika")

if "user" in st.session_state:
    # Hlavní aplikace pro přihlášené uživatele
    st.header("Přidat tiket")
    castka = st.number_input("Vložená částka", min_value=0.0, step=0.1)
    kurz = st.number_input("Kurz", min_value=1.0, step=0.01)
    vysledek = st.radio("Výsledek", ["Vyhrál", "Prohrál"], horizontal=True)
    
    if st.button("Přidat tiket"):
        st.session_state.tikety.append({"castka": castka, "kurz": kurz, "vysledek": vysledek})
        save_tikety(st.session_state.tikety)
        st.success(f"Tiket přidán: {castka} Kč, Kurz: {kurz}, Výsledek: {vysledek}")
    
    if st.session_state.tikety:
        st.header("Historie tiketů")
        df = pd.DataFrame(st.session_state.tikety)
        st.dataframe(df)
else:
    st.warning("Přihlašte se pro přístup k aplikaci.")
