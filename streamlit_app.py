import streamlit as st
import pandas as pd
import json
import os

# Nastavení stránky
st.set_page_config(page_title="betmastery")

st.markdown("""<style>
    body {
        background: linear-gradient(180deg, hsl(241, 100%, 10%) 0%, hsl(75, 93%, 74%) 100%);
        color: white;
        font-family: Arial, sans-serif;
    }
</style>""", unsafe_allow_html=True)

# Soubory a data
DATA_FILE = "tikety.json"

def load_tikety():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_tikety(tikety):
    with open(DATA_FILE, "w") as file:
        json.dump(tikety, file)

# Inicializace session_state pro tikety
if "tikety" not in st.session_state:
    st.session_state.tikety = load_tikety()

# Nastavení přihlášení a registrace
if "user" not in st.session_state:
    st.session_state.user = None

def login_user(username, password):
    # Tady by měla být logika pro ověření uživatele (připojení k databázi nebo kontrola souboru)
    st.session_state.user = {"username": username}

def register_user(username, password):
    # Uložení nového uživatele (tato logika je velmi zjednodušená)
    st.session_state.user = {"username": username}

# Rozbalovací menu
menu_option = st.sidebar.selectbox("Přihlásit se / Registrovat", ["Přihlásit se", "Registrovat"])

if menu_option == "Přihlásit se":
    st.sidebar.header("Přihlášení")
    username = st.sidebar.text_input("Uživatelské jméno")
    password = st.sidebar.text_input("Heslo", type="password")
    if st.sidebar.button("Přihlásit se"):
        login_user(username, password)
        st.sidebar.success(f"Úspěšně přihlášeno jako {username}")

elif menu_option == "Registrovat":
    st.sidebar.header("Registrace")
    username = st.sidebar.text_input("Uživatelské jméno")
    password = st.sidebar.text_input("Heslo", type="password")
    if st.sidebar.button("Registrovat"):
        register_user(username, password)
        st.sidebar.success(f"Úspěšná registrace {username}")

# Kontrola, zda je uživatel přihlášen
if st.session_state.user:
    st.header(f"Vítejte, {st.session_state.user['username']}!")

    # Hlavní obsah
    st.title("Sázková statistika")

    # Vstupní formulář pro přidání tiketu
    st.header("Přidat tiket")
    castka = st.number_input("Vložená částka", min_value=0.0, step=0.1, key="castka_input")
    kurz = st.number_input("Kurz", min_value=1.0, step=0.01, key="kurz_input")
    vysledek = st.radio("Výsledek", ["Vyhrál", "Prohrál"], horizontal=True, key="vysledek_input")

    if st.button("Přidat tiket"):
        st.session_state.tikety.append({"castka": castka, "kurz": kurz, "vysledek": vysledek})
        save_tikety(st.session_state.tikety)
        st.success(f"Tiket přidán: {castka} Kč, Kurz: {kurz}, Výsledek: {vysledek}")

    # Výpočty statistik
    celkovy_zisk = 0
    celkovy_zisk_penez = 0
    celkovy_zisk_procenta = 0
    prumerny_kurz = 0
    prumerny_uspesny_kurz = 0

    if st.session_state.tikety:
        df = pd.DataFrame(st.session_state.tikety)
        df["výhra"] = df.apply(lambda row: row["castka"] * row["kurz"] if row["vysledek"] == "Vyhrál" else 0, axis=1)

        celkovy_zisk = df["výhra"].sum() - df["castka"].sum()
        celkovy_zisk_penez = celkovy_zisk
        celkova_vlozena_castka = df["castka"].sum()
        celkovy_zisk_procenta = (celkovy_zisk / celkova_vlozena_castka * 100) if celkova_vlozena_castka > 0 else 0
        prumerny_kurz = df["kurz"].mean()
        uspesne_kurzy = df[df["výhra"] > 0]["kurz"]
        prumerny_uspesny_kurz = uspesne_kurzy.mean() if not uspesne_kurzy.empty else 0

    # Zobrazení statistik
    st.header("Celkový výsledek")
    st.markdown(f'Celkový zisk: {celkovy_zisk_procenta:.2f}%')
    st.markdown(f"Průměrný kurz: {prumerny_kurz:.2f}")
    st.markdown(f"Průměrný úspěšný kurz: {prumerny_uspesny_kurz:.2f}")
