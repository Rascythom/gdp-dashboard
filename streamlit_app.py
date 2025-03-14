import streamlit as st
import pandas as pd
import json
import os

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

# Přidání formulářů pro registraci a přihlášení
def registrace():
    st.subheader("Registrace")
    jmeno = st.text_input("Uživatelské jméno")
    heslo = st.text_input("Heslo", type="password")
    if st.button("Registrovat"):
        if jmeno and heslo:
            st.session_state.username = jmeno
            st.session_state.password = heslo
            st.success(f"Úspěšně jsi zaregistrován jako {jmeno}")
        else:
            st.error("Vyplň všechny údaje!")

def prihlaseni():
    st.subheader("Přihlášení")
    jmeno = st.text_input("Uživatelské jméno", key="login_username")
    heslo = st.text_input("Heslo", type="password", key="login_password")
    if st.button("Přihlásit se"):
        if jmeno == st.session_state.get("username") and heslo == st.session_state.get("password"):
            st.session_state.logged_in = True
            st.success(f"Úspěšně přihlášen jako {jmeno}")
        else:
            st.error("Chybné uživatelské jméno nebo heslo.")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.title("Sázková statistika")
    # Tady pokračuje tvůj původní kód s formuláři pro přidání tiketu, výpočty a statistiky
    # Vložil jsem to sem pro přehlednost, abys věděl, kde to máš použít
    st.header("Přidat tiket")
    castka = st.number_input("Vložená částka", min_value=0.0, step=0.1, key="castka_input")
    kurz = st.number_input("Kurz", min_value=1.0, step=0.01, key="kurz_input")
    vysledek = st.radio("Výsledek", ["Vyhrál", "Prohrál"], horizontal=True, key="vysledek_input")

    if st.button("Přidat tiket"):
        st.session_state.tikety.append({"castka": castka, "kurz": kurz, "vysledek": vysledek})
        save_tikety(st.session_state.tikety)
        st.success(f"Tiket přidán: {castka} Kč, Kurz: {kurz}, Výsledek: {vysledek}")

    # Výpočty statistik a zbytek tvého kódu...
else:
    option = st.radio("Vyber možnost", ["Registrace", "Přihlášení"])
    if option == "Registrace":
        registrace()
    elif option == "Přihlášení":
        prihlaseni()
