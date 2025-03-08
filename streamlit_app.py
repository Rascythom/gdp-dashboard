import streamlit as st
import pandas as pd
import json
import os

# Cesta k souboru
DATA_FILE = "tikety.json"

# Funkce pro načtení tiketů ze souboru
def load_tikety():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# Funkce pro uložení tiketů do souboru
def save_tikety(tikety):
    with open(DATA_FILE, "w") as file:
        json.dump(tikety, file)

# Inicializace session state
if "tikety" not in st.session_state:
    st.session_state.tikety = load_tikety()

st.title("Sázková statistika")

# Vstupní formulář
st.header("Přidat tiket")
castka = st.number_input("Vložená částka", min_value=0.0, step=0.1, key="castka_input")
kurz = st.number_input("Kurz", min_value=1.0, step=0.01, key="kurz_input")
vysledek = st.radio("Výsledek", ["Vyhrál", "Prohrál"], horizontal=True, key="vysledek_input")

if st.button("Přidat tiket"):
    st.session_state.tikety.append({"castka": castka, "kurz": kurz, "vysledek": vysledek})
    save_tikety(st.session_state.tikety)
    st.success(f"Tiket přidán: {castka} Kč, Kurz: {kurz}, Výsledek: {vysledek}")

# Výpočty statistik
if st.session_state.tikety:
    df = pd.DataFrame(st.session_state.tikety)
    df["výhra"] = df.apply(lambda row: row["castka"] * row["kurz"] if row["vysledek"] == "Vyhrál" else 0, axis=1)
    celkovy_zisk = df["výhra"].sum() - df["castka"].sum()
    celkovy_zisk_procenta = (celkovy_zisk / df["castka"].sum() * 100) if df["castka"].sum() > 0 else 0
    prumerny_kurz = df["kurz"].mean()
else:
    celkovy_zisk = 0
    celkovy_zisk_procenta = 0
    prumerny_kurz = 0

# Výstup statistik
st.header("Celkový výsledek")
st.markdown(f"Celkový zisk: {celkovy_zisk_procenta:.2f}%")
st.markdown(f"Celkový zisk v penězích: {celkovy_zisk:.2f} Kč")
st.markdown(f"Průměrný kurz: {prumerny_kurz:.2f}")

# Zobrazení tiketů a mazání
def smazat_tiket(index):
    del st.session_state.tikety[index]
    save_tikety(st.session_state.tikety)

if st.session_state.tikety:
    st.header("Historie tiketů")
    for i, tiket in enumerate(st.session_state.tikety):
        st.markdown(f"Tiket {i+1}: {tiket['castka']} Kč, Kurz: {tiket['kurz']}, Výsledek: {tiket['vysledek']}")
        if st.button(f"Smazat {i+1}", key=f"smazat_{i}"):
            smazat_tiket(i)
            st.experimental_rerun()
