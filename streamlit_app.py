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

# Výpočty statistik
celkovy_zisk = 0
celkovy_zisk_penez = 0
prumerny_kurz = 0
prumerny_uspesny_kurz = 0

if st.session_state.tikety:
    df = pd.DataFrame(st.session_state.tikety)
    df["výhra"] = df.apply(lambda row: row["castka"] * row["kurz"] if row["vysledek"] == "Vyhrál" else 0, axis=1)
    
    # Výstup statistik
    celkovy_zisk = df["výhra"].sum() - df["castka"].sum()
    celkovy_zisk_penez = celkovy_zisk
    prumerny_kurz = df["kurz"].mean()
    uspesne_kurzy = df[df["výhra"] > 0]["kurz"]
    prumerny_uspesny_kurz = uspesne_kurzy.mean() if not uspesne_kurzy.empty else 0

# Výstup statistik
st.header("Celkový výsledek")
st.markdown(f'<div style="padding: 10px; background-color: {"#4CAF50" if celkovy_zisk >= 0 else "#FF5252"}; border-radius: 5px; color: white;">Celkový zisk: {celkovy_zisk:.2f}%</div>', unsafe_allow_html=True)
st.markdown(f'<div style="padding: 10px; background-color: {"#4CAF50" if celkovy_zisk_penez >= 0 else "#FF5252"}; border-radius: 5px; color: white;">Celkový zisk v penězích: {celkovy_zisk_penez:.2f} Kč</div>', unsafe_allow_html=True)

# Průměrný kurz a průměrný úspěšný kurz bez barevného pozadí
st.markdown(f"Průměrný kurz: {prumerny_kurz:.2f}")
st.markdown(f"Průměrný úspěšný kurz: {prumerny_uspesny_kurz:.2f}")

# Zobrazení všech tiketů
if st.session_state.tikety:
    st.header("Historie tiketů")
    
    # Možnost editace a smazání tiketů
    def upravit_tiket(index, castka, kurz, vysledek):
        st.session_state.tikety[index] = {"castka": castka, "kurz": kurz, "vysledek": vysledek}
        st.success(f"Tiket upraven: {castka} Kč, Kurz: {kurz}, Výsledek: {vysledek}")

    def smazat_tiket(index):
        del st.session_state.tikety[index]
        st.success("Tiket byl smazán")

    # Výpis tiketů s tlačítky pro editaci a smazání
    for i, tiket in enumerate(st.session_state.tikety):
        st.write(f"Tiket {i+1}: {tiket['castka']} Kč, Kurz: {tiket['kurz']}, Výsledek: {tiket['vysledek']}")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"Upravit {i+1}"):
                castka_upravit = st.number_input(f"Nová částka pro tiket {i+1}", value=tiket['castka'], min_value=0.0, step=0.1)
                kurz_upravit = st.number_input(f"Nový kurz pro tiket {i+1}", value=tiket['kurz'], min_value=1.0, step=0.01)
                vysledek_upravit = st.radio(f"Nový výsledek pro tiket {i+1}", ["Vyhrál", "Prohrál"], index=["Vyhrál", "Prohrál"].index(tiket['vysledek']))
                if st.button(f"Upravit tiket {i+1}"):
                    upravit_tiket(i, castka_upravit, kurz_upravit, vysledek_upravit)
        with col2:
            if st.button(f"Smazat {i+1}"):
                smazat_tiket(i)
