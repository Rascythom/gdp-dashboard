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
        .form-container {
            width: 350px;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
        }
        .button-container {
            margin-top: 20px;
            display: flex;
            justify-content: center;
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

# Funkce pro zobrazení přihlášení a registrace
def show_login_register_form():
    st.title("Sázková statistika")
    option = st.selectbox("Vyberte možnost", ["Přihlášení", "Registrace", "Obnovit heslo"])
    
    if option == "Přihlášení":
        email = st.text_input("Email")
        password = st.text_input("Heslo", type="password")
        if st.button("Přihlásit"):
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.user_password = password
            st.success("Úspěšně přihlášeno!")
            
    elif option == "Registrace":
        email = st.text_input("Email")
        password = st.text_input("Heslo", type="password")
        confirm_password = st.text_input("Potvrďte heslo", type="password")
        if st.button("Registrovat"):
            if password == confirm_password:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_password = password
                st.success("Úspěšná registrace!")
            else:
                st.error("Hesla se neshodují")
    
    elif option == "Obnovit heslo":
        email = st.text_input("Zadejte svůj email")
        if st.button("Obnovit heslo"):
            st.success("Odkaz pro obnovu hesla byl odeslán na váš email!")
            
# Pokud je uživatel přihlášen, zobrazí se hlavní stránka s přehledem tiketů
if "logged_in" in st.session_state and st.session_state.logged_in:
    st.title("Sázková statistika")
    
    # Formulář pro přidání tiketu
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

    # Výstup statistik
    st.header("Celkový výsledek")
    st.markdown(
        f'<div style="padding: 10px; background-color: {"#4CAF50" if celkovy_zisk_procenta >= 0 else "#FF5252"}; border-radius: 5px; color: white;">Celkový zisk: {celkovy_zisk_procenta:.2f}%</div>',
        unsafe_allow_html=True)
    st.markdown(
        f'<div style="padding: 10px; background-color: {"#4CAF50" if celkovy_zisk_penez >= 0 else "#FF5252"}; border-radius: 5px; color: white;">Celkový zisk v penězích: {celkovy_zisk_penez:.2f} Kč</div>',
        unsafe_allow_html=True)

    st.markdown(f"Průměrný kurz: {prumerny_kurz:.2f}")
    st.markdown(f"Průměrný úspěšný kurz: {prumerny_uspesny_kurz:.2f}")

# Pokud není uživatel přihlášen, zobrazí se formulář pro přihlášení, registraci nebo obnovu hesla
else:
    show_login_register_form()
