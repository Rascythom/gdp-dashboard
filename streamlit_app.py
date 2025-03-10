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

# Zobrazení všech tiketů v opačném pořadí
if st.session_state.tikety:
    st.header("Historie tiketů")


    def smazat_tiket(index):
        del st.session_state.tikety[index]
        save_tikety(st.session_state.tikety)


    for i, tiket in enumerate(reversed(st.session_state.tikety)):
        index = len(st.session_state.tikety) - 1 - i  # Přepočítání indexu
        if tiket['vysledek'] == "Vyhrál":
            st.markdown(
                f'<div style="padding: 10px; background-color: #4CAF50; border-radius: 5px; color: white;">Tiket {index + 1}: {tiket["castka"]} Kč, Kurz: {tiket["kurz"]}, Výsledek: {tiket["vysledek"]}</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div style="padding: 10px; background-color: #FF5252; border-radius: 5px; color: white;">Tiket {index + 1}: {tiket["castka"]} Kč, Kurz: {tiket["kurz"]}, Výsledek: {tiket["vysledek"]}</div>',
                unsafe_allow_html=True)

        if st.button(f"Smazat {index + 1}", key=f"smazat_{index}"):
            smazat_tiket(index)
            save_tikety(st.session_state.tikety)
