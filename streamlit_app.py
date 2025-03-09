import streamlit as st
import pandas as pd
import json
import os

# Vlastní CSS pro stylování
st.markdown("""
    <style>
        body {
            background: linear-gradient(180deg, hsl(241, 100%, 10%) 0%, hsl(75, 93%, 74%) 100%);
            color: white;
            font-family: Arial, sans-serif;
        }
        h1 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 5rem;
            background: linear-gradient(90deg, rgba(241, 53, 80, 1) 0%, rgba(34, 193, 195, 1) 100%);
            -webkit-background-clip: text;
            color: transparent;
            text-align: center;
            margin-top: 20px;
            margin-bottom: 0;
        }
        h2 {
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 30px;
        }
        .stButton button {
            background-color: #1a73e8;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 1.2rem;
            transition: background-color 0.3s;
        }
        .stButton button:hover {
            background-color: #0c56b2;
        }
    </style>
""", unsafe_allow_html=True)

# Cesta k souboru s tikety
DATA_FILE = "tikety.json"

# Načtení tiketů ze souboru
def load_tikety():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# Uložení tiketů do souboru
def save_tikety(tikety):
    with open(DATA_FILE, "w") as file:
        json.dump(tikety, file)

# Pokud tiket není v session state, načteme ho
if "tikety" not in st.session_state:
    st.session_state.tikety = load_tikety()

# Hlavní nadpis s názvem aplikace
st.title("ANALYTIK")
st.header("Vyhodnocujte své sázky jako profesionál.")

# Sekce pro přidání nového tiketu
st.header("Přidat tiket")
castka = st.number_input("Vložená částka", min_value=0.0, step=0.1, key="castka_input")
kurz = st.number_input("Kurz", min_value=1.0, step=0.01, key="kurz_input")
vysledek = st.radio("Výsledek", ["Vyhrál", "Prohrál"], horizontal=True, key="vysledek_input")

if st.button("Přidat tiket"):
    st.session_state.tikety.append({"castka": castka, "kurz": kurz, "vysledek": vysledek})
    save_tikety(st.session_state.tikety)
    st.success(f"Tiket přidán: {castka} Kč, Kurz: {kurz}, Výsledek: {vysledek}")

# Výpočet celkového zisku a dalších statistik
if st.session_state.tikety:
    df = pd.DataFrame(st.session_state.tikety)
    df["výhra"] = df.apply(lambda row: row["castka"] * row["kurz"] if row["vysledek"] == "Vyhrál" else 0, axis=1)

    celkovy_zisk = df["výhra"].sum() - df["castka"].sum()
    celkovy_zisk_procenta = (celkovy_zisk / df["castka"].sum() * 100) if df["castka"].sum() > 0 else 0
    prumerny_kurz = df["kurz"].mean()
    uspesne_kurzy = df[df["výhra"] > 0]["kurz"]
    prumerny_uspesny_kurz = uspesne_kurzy.mean() if not uspesne_kurzy.empty else 0

# Zobrazení celkového výsledku
st.header("Celkový výsledek")
st.markdown(
    f'<div style="padding: 10px; background-color: {"#4CAF50" if celkovy_zisk_procenta >= 0 else "#FF5252"}; border-radius: 5px; color: white;">Celkový zisk: {celkovy_zisk_procenta:.2f}%</div>',
    unsafe_allow_html=True)

st.markdown(f"Průměrný kurz: {prumerny_kurz:.2f}")
st.markdown(f"Průměrný úspěšný kurz: {prumerny_uspesny_kurz:.2f}")

# Historie tiketů
st.header("Historie tiketů")

def smazat_tiket(index):
    del st.session_state.tikety[index]
    save_tikety(st.session_state.tikety)
    st.rerun()

for i in range(len(st.session_state.tikety) - 1, -1, -1):
    tiket = st.session_state.tikety[i]
    barva = "#4CAF50" if tiket['vysledek'] == "Vyhrál" else "#FF5252"
    st.markdown(
        f'<div style="padding: 10px; background-color: {barva}; border-radius: 5px; color: white;">Tiket {i + 1}: {tiket["castka"]} Kč, Kurz: {tiket["kurz"]}, Výsledek: {tiket["vysledek"]}</div>',
        unsafe_allow_html=True)
    if st.button(f"Smazat {i + 1}", key=f"smazat_{i}"):
        smazat_tiket(i)
