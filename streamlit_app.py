import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
st.markdown(f'<div style="padding: 10px; background-color: {"#4CAF50" if celkovy_zisk_procenta >= 0 else "#FF5252"}; border-radius: 5px; color: white;">Celkový zisk: {celkovy_zisk_procenta:.2f}%</div>', unsafe_allow_html=True)
st.markdown(f'<div style="padding: 10px; background-color: {"#4CAF50" if celkovy_zisk_penez >= 0 else "#FF5252"}; border-radius: 5px; color: white;">Celkový zisk v penězích: {celkovy_zisk_penez:.2f} Kč</div>', unsafe_allow_html=True)

st.markdown(f"Průměrný kurz: {prumerny_kurz:.2f}")
st.markdown(f"Průměrný úspěšný kurz: {prumerny_uspesny_kurz:.2f}")

# Vytvoření grafu
if st.session_state.tikety:
    # Vytvoření seznamu zisků a proher pro graf
    zisky_a_ztraty = []
    for i, tiket in enumerate(st.session_state.tikety):
        zisk = tiket["castka"] * tiket["kurz"] if tiket["vysledek"] == "Vyhrál" else -tiket["castka"]
        zisky_a_ztraty.append(zisk)

    # Graf
    fig, ax = plt.subplots()
    ax.plot(range(1, len(zisky_a_ztraty) + 1), zisky_a_ztraty, color='green' if zisky_a_ztraty[-1] >= 0 else 'red', marker='o')
    
    # Nastavení grafu
    ax.set_title("Růst/Zisk vs Pokles/Ztráta")
    ax.set_xlabel("Počet tiketů")
    ax.set_ylabel("Zisk/Ztráta (Kč)")
    ax.set_facecolor('#1e1e1e')  # tmavé pozadí
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Zobrazení grafu
    st.pyplot(fig)

# Zobrazení všech tiketů
if st.session_state.tikety:
    st.header("Historie tiketů")
    
    # Funkce pro smazání tiketů
    def smazat_tiket(index):
        del st.session_state.tikety[index]
        # Namísto st.experimental_rerun() použijeme st.session_state.refresh()
        st.session_state.tikety = st.session_state.tikety  # force refresh the state
        st.success("Tiket byl smazán")

    for i, tiket in enumerate(st.session_state.tikety):
        st.write(f"Tiket {i+1}: {tiket['castka']} Kč, Kurz: {tiket['kurz']}, Výsledek: {tiket['vysledek']}")
        if st.button(f"Smazat {i+1}", key=f"smazat_{i}"):
            smazat_tiket(i)
