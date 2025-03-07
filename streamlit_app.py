import streamlit as st
import pandas as pd

# Inicializace session state pro ukládání tiketů
if "tikety" not in st.session_state:
    st.session_state.tikety = []

st.title("Sázková statistika")

# Vstupní formulář
st.header("Přidat tiket")
castka = st.number_input("Vložená částka", min_value=0.0, step=0.1)
kurz = st.number_input("Kurz", min_value=1.0, step=0.01)
vysledek = st.radio("Výsledek", ["Vyhrál", "Prohrál"], horizontal=True)

if st.button("Přidat tiket"):
    st.session_state.tikety.append({"castka": castka, "kurz": kurz, "vysledek": vysledek})
    st.success(f"Tiket přidán: {castka} Kč, Kurz: {kurz}, Výsledek: {vysledek}")

# Zobrazení všech tiketů
if st.session_state.tikety:
    st.header("Historie tiketů")
    df = pd.DataFrame(st.session_state.tikety)
    df["výhra"] = df.apply(lambda row: row["castka"] * row["kurz"] if row["vysledek"] == "Vyhrál" else 0, axis=1)
    st.dataframe(df, use_container_width=True)
    
    # Výpočty statistik
    celkovy_zisk = df["výhra"].sum() - df["castka"].sum()
    celkovy_zisk_penez = celkovy_zisk
    prumerny_kurz = df["kurz"].mean()
    uspesne_kurzy = df[df["výhra"] > 0]["kurz"]
    prumerny_uspesny_kurz = uspesne_kurzy.mean() if not uspesne_kurzy.empty else 0
    
    # Barvy podle zisku
    barva_zisk = "#4CAF50" if celkovy_zisk >= 0 else "#FF5252"
    barva_zisk_penez = "#4CAF50" if celkovy_zisk_penez >= 0 else "#FF5252"
    barva_prumerny_kurz = "#4CAF50" if prumerny_kurz >= 2 else "#FF5252"
    barva_uspesny_kurz = "#4CAF50" if prumerny_uspesny_kurz >= 2 else "#FF5252"
    
    # Výstup statistik
    st.header("Celkový výsledek")
    st.markdown(f'<div style="padding: 10px; background-color: {barva_zisk}; border-radius: 5px; color: white;">Celkový zisk: {celkovy_zisk:.2f}%</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="padding: 10px; background-color: {barva_zisk_penez}; border-radius: 5px; color: white;">Celkový zisk v penězích: {celkovy_zisk_penez:.2f} Kč</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="padding: 10px; background-color: {barva_prumerny_kurz}; border-radius: 5px; color: white;">Průměrný kurz: {prumerny_kurz:.2f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="padding: 10px; background-color: {barva_uspesny_kurz}; border-radius: 5px; color: white;">Průměrný úspěšný kurz: {prumerny_uspesny_kurz:.2f}</div>', unsafe_allow_html=True)
