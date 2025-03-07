import streamlit as st
import pandas as pd
import os

# Inicializace session_state pro uchování dat
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Sázka", "Kurz", "Výsledek", "Zisk"])

def load_data():
    if os.path.exists("tikety.csv"):
        return pd.read_csv("tikety.csv")
    return pd.DataFrame(columns=["Sázka", "Kurz", "Výsledek", "Zisk"])

def add_ticket(sazka, kurz, vysledek):
    zisk = sazka * (kurz - 1) if vysledek == "Vyhrál" else -sazka
    new_data = pd.DataFrame([[sazka, kurz, vysledek, zisk]], columns=["Sázka", "Kurz", "Výsledek", "Zisk"])
    
    st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
    st.session_state.data.to_csv("tikety.csv", index=False)

def calculate_statistics(data):
    if data.empty:
        return 0, 0, 0, 0
    total_zisk = data["Zisk"].sum()
    total_sazka = data["Sázka"].sum()
    prumerny_kurz = (data["Sázka"] * data["Kurz"]).sum() / total_sazka if total_sazka > 0 else 0
    prumerny_uspesny_kurz = (
        (data[data["Výsledek"] == "Vyhrál"]["Sázka"] * data[data["Výsledek"] == "Vyhrál"]["Kurz"]).sum() /
        data[data["Výsledek"] == "Vyhrál"]["Sázka"].sum()
        if data[data["Výsledek"] == "Vyhrál"]["Sázka"].sum() > 0 else 0
    )
    return total_zisk / total_sazka * 100, total_zisk, prumerny_kurz, prumerny_uspesny_kurz

if st.session_state.data.empty:
    st.session_state.data = load_data()

st.title("Sportovní Sázky Statistiky")

st.subheader("Zadání nového tiketu")
sazka = st.number_input("Zadejte částku sázky", min_value=0.0, step=1.0)
kurz = st.number_input("Zadejte kurz", min_value=1.0, step=0.01)
vysledek = st.selectbox("Výsledek", ["Vyhrál", "Prohrál"])

if st.button("Přidat tiket"):
    add_ticket(sazka, kurz, vysledek)
    st.success(f"Tiket přidán: {sazka} Kč, Kurz: {kurz}, Výsledek: {vysledek}", icon="ℹ️")
    st.markdown("<style>.stSuccess{border-left: 5px solid grey !important;}</style>", unsafe_allow_html=True)

total_percent, total_zisk, prumerny_kurz, prumerny_uspesny_kurz = calculate_statistics(st.session_state.data)

st.subheader("Celkový Výsledek")
color = "green" if total_zisk >= 0 else "red"
st.markdown(f'<div style="border: 2px solid {color}; padding: 10px; border-radius: 5px;">📊 <b>Celkový zisk:</b> {total_percent:.2f}%</div>', unsafe_allow_html=True)
st.markdown(f'<div style="border: 2px solid {color}; padding: 10px; border-radius: 5px;">💰 <b>Celkový zisk v Kč:</b> {total_zisk:.2f} Kč</div>', unsafe_allow_html=True)
st.markdown(f'<div style="border: 2px solid grey; padding: 10px; border-radius: 5px;">📈 <b>Průměrný kurz:</b> {prumerny_kurz:.2f}</div>', unsafe_allow_html=True)
st.markdown(f'<div style="border: 2px solid grey; padding: 10px; border-radius: 5px;">🏆 <b>Průměrný úspěšný kurz:</b> {prumerny_uspesny_kurz:.2f}</div>', unsafe_allow_html=True)

st.subheader("Historie tiketů")
st.write(st.session_state.data)
