import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(
    page_title="betmastery", 
    menu_items={}
)

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

# Výpočet úspěšnosti podle typu kurzu
def analyza_uspesnosti_kurzu(df):
    nizke_kurzy = df[df["kurz"] <= 2.0]
    stredni_kurzy = df[(df["kurz"] > 2.0) & (df["kurz"] <= 3.0)]
    vysoke_kurzy = df[df["kurz"] > 3.0]

    uspesnost_nizke = (nizke_kurzy["výhra"].sum() / nizke_kurzy["castka"].sum() * 100) if nizke_kurzy["castka"].sum() > 0 else 0
    uspesnost_stredni = (stredni_kurzy["výhra"].sum() / stredni_kurzy["castka"].sum() * 100) if stredni_kurzy["castka"].sum() > 0 else 0
    uspesnost_vysoke = (vysoke_kurzy["výhra"].sum() / vysoke_kurzy["castka"].sum() * 100) if vysoke_kurzy["castka"].sum() > 0 else 0

    return uspesnost_nizke, uspesnost_stredni, uspesnost_vysoke

uspesnost_nizke, uspesnost_stredni, uspesnost_vysoke = analyza_uspesnosti_kurzu(df) if st.session_state.tikety else (0, 0, 0)

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

# Zobrazení úspěšnosti podle kurzu
st.subheader("Úspěšnost podle typu kurzu")
st.markdown(f"Úspěšnost při nízkých kurzech (do 2.0): {uspesnost_nizke:.2f}%")
st.markdown(f"Úspěšnost při středních kurzech (2.0–3.0): {uspesnost_stredni:.2f}%")
st.markdown(f"Úspěšnost při vysokých kurzech (nad 3.0): {uspesnost_vysoke:.2f}%")

# Zobrazení všech tiketů
if st.session_state.tikety:
    st.header("Historie tiketů")

    def smazat_tiket(index):
        del st.session_state.tikety[index]
        save_tikety(st.session_state.tikety)

    # Smazání tiketu bez použití st.experimental_rerun()
    for i, tiket in enumerate(st.session_state.tikety):
        if tiket['vysledek'] == "Vyhrál":
            st.markdown(
                f'<div style="padding: 10px; background-color: #4CAF50; border-radius: 5px; color: white;">Tiket {i + 1}: {tiket["castka"]} Kč, Kurz: {tiket["kurz"]}, Výsledek: {tiket["vysledek"]}</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div style="padding: 10px; background-color: #FF5252; border-radius: 5px; color: white;">Tiket {i + 1}: {tiket["castka"]} Kč, Kurz: {tiket["kurz"]}, Výsledek: {tiket["vysledek"]}</div>',
                unsafe_allow_html=True)

        if st.button(f"Smazat {i + 1}", key=f"smazat_{i}"):
            smazat_tiket(i)
            save_tikety(st.session_state.tikety)
