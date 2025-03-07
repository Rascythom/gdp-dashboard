import streamlit as st
import pandas as pd
import os

# Funkce pro načtení dat z CSV souboru (pokud existuje)
def load_data():
    if os.path.exists("tikety.csv"):
        return pd.read_csv("tikety.csv")
    else:
        return pd.DataFrame(columns=["Sázka", "Kurz", "Výsledek", "Zisk"])

# Funkce pro přidání nového tiketu
def add_ticket(sazka, kurz, vysledek):
    data = load_data()
    zisk = 0
    if vysledek == "Vyhrál":
        zisk = sazka * (kurz - 1)
    # Přidání nového tiketu do dataframe
    new_data = pd.DataFrame([[sazka, kurz, vysledek, zisk]], columns=["Sázka", "Kurz", "Výsledek", "Zisk"])
    data = pd.concat([data, new_data], ignore_index=True)
    data.to_csv("tikety.csv", index=False)

    return data

# Funkce pro výpočet celkového zisku a průměrného kurzu
def calculate_statistics(data):
    if len(data) == 0:
        return 0, 0  # Pokud nejsou žádná data, vrátíme 0
    total_zisk = data["Zisk"].sum()
    total_sazka = data["Sázka"].sum()
    prumerny_kurz = (data["Sázka"] * data["Kurz"]).sum() / total_sazka if total_sazka > 0 else 0
    prumerny_uspesny_kurz = (data[data["Výsledek"] == "Vyhrál"]["Sázka"] * data[data["Výsledek"] == "Vyhrál"]["Kurz"]).sum() / data[data["Výsledek"] == "Vyhrál"]["Sázka"].sum() if data[data["Výsledek"] == "Vyhrál"]["Sázka"].sum() > 0 else 0
    return total_zisk / total_sazka * 100, total_zisk, prumerny_kurz, prumerny_uspesny_kurz

# Streamlit UI
st.title("Sportovní Sázky Statistiky")
st.subheader("Zadání nového tiketu")

# Zadání vstupních údajů
sazka = st.number_input("Zadejte částku sázky", min_value=0.0, step=1.0)
kurz = st.number_input("Zadejte kurz", min_value=1.0, step=0.01)
vysledek = st.selectbox("Výsledek", ["Vyhrál", "Prohrál"])

# Přidání tiketu
if st.button("Přidat tiket"):
    data = add_ticket(sazka, kurz, vysledek)
    st.success(f"Tiket přidán: {sazka} Kč, Kurz: {kurz}, Výsledek: {vysledek}")
    
    # Výpočty
    total_percent, total_zisk, prumerny_kurz, prumerny_uspesny_kurz = calculate_statistics(data)
    
    st.subheader("Celkový Výsledek")
    st.write(f"Celkový zisk: {total_percent:.2f}%")
    st.write(f"Celkový zisk v penězích: {total_zisk:.2f} Kč")
    st.write(f"Průměrný kurz: {prumerny_kurz:.2f}")
    st.write(f"Průměrný úspěšný kurz: {prumerny_uspesny_kurz:.2f}")
    
    st.subheader("Historie tiketů")
    st.write(data)
