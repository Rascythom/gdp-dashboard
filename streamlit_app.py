import streamlit as st
import pandas as pd
import json
import os

st.markdown("""
    <style>
        body {
            background: linear-gradient(180deg, hsl(241, 100%, 10%) 0%, hsl(75, 93%, 74%) 100%);
            color: white;
            font-family: Arial, sans-serif;
        }

        h1 {
            font-family: 'Montserrat', sans-serif;
            font-size: 3.5em;
            letter-spacing: 5px;
            background: linear-gradient(90deg, hsl(241, 100%, 10%) 0%, #ffffff 100%);
            -webkit-background-clip: text;
            color: transparent;
        }

        h2 {
            font-size: 1.5em;
            font-family: 'Arial', sans-serif;
            text-align: center;
        }

        .motto {
            font-size: 1.2em;
            font-family: 'Arial', sans-serif;
            text-align: center;
            margin-top: -15px;
            color: #ffffff;
        }

        .result-box {
            padding: 10px;
            border-radius: 5px;
            color: white;
            margin-bottom: 20px;
        }

        .history-box {
            padding: 10px;
            border-radius: 5px;
            color: white;
            margin-bottom: 10px;
        }

        .button-container {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
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

# 1. Title and motto
st.title("ANALYTIK")
st.markdown('<p class="motto">Vyhodnocujte své sázky jako profesionál.</p>', unsafe_allow_html=True)

# 2. Adding bet ticket
st.header("Přidat tiket")
castka = st.number_input("Vložená částka", min_value=0.0, step=0.1, key="castka_input")
kurz = st.number_input("Kurz", min_value=1.0, step=0.01, key="kurz_input")
vysledek = st.radio("Výsledek", ["Vyhrál", "Prohrál"], horizontal=True, key="vysledek_input")

if st.button("Přidat tiket"):
    st.session_state.tikety.append({"castka": castka, "kurz": kurz, "vysledek": vysledek})
    save_tikety(st.session_state.tikety)
    st.success(f"Tiket přidán: {castka} Kč, Kurz: {kurz}, Výsledek: {vysledek}")

# 3. Showing overall results
if st.session_state.tikety:
    df = pd.DataFrame(st.session_state.tikety)
    df["výhra"] = df.apply(lambda row: row["castka"] * row["kurz"] if row["vysledek"] == "Vyhrál" else 0, axis=1)

    celkovy_zisk = df["výhra"].sum() - df["castka"].sum()
    celkovy_zisk_procenta = (celkovy_zisk / df["castka"].sum() * 100) if df["castka"].sum() > 0 else 0
    prumerny_kurz = df["kurz"].mean()
    uspesne_kurzy = df[df["výhra"] > 0]["kurz"]
    prumerny_uspesny_kurz = uspesne_kurzy.mean() if not uspesne_kurzy.empty else 0

st.header("Celkový výsledek")
st.markdown(
    f'<div class="result-box" style="background-color: {"#4CAF50" if celkovy_zisk_procenta >= 0 else "#FF5252"};">Celkový zisk: {celkovy_zisk_procenta:.2f}%</div>',
    unsafe_allow_html=True)

st.markdown(f"Průměrný kurz: {prumerny_kurz:.2f}")
st.markdown(f"Průměrný úspěšný kurz: {prumerny_uspesny_kurz:.2f}")

# 4. Showing history of tickets
st.header("Historie tiketů")

def smazat_tiket(index):
    del st.session_state.tikety[index]
    save_tikety(st.session_state.tikety)
    st.rerun()

for i in range(len(st.session_state.tikety) - 1, -1, -1):
    tiket = st.session_state.tikety[i]
    barva = "#4CAF50" if tiket['vysledek'] == "Vyhrál" else "#FF5252"
    st.markdown(
        f'<div class="history-box" style="background-color: {barva};">Tiket {i + 1}: {tiket["castka"]} Kč, Kurz: {tiket["kurz"]}, Výsledek: {tiket["vysledek"]}</div>',
        unsafe_allow_html=True)
    if st.button(f"Smazat {i + 1}", key=f"smazat_{i}"):
        smazat_tiket(i)
