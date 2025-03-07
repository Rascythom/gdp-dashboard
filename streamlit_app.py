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
    st.experimental_set_query_params(updated="true")
    st.success(f"Tiket přidán: {castka} Kč, Kurz: {kurz}, Výsledek: {vysledek}")

# Výpočty statistik
if st.session_state.tikety:
    df = pd.DataFrame(st.session_state.tikety)
    df["výhra"] = df.apply(lambda row: row["castka"] * row["kurz"] if row["vysledek"] == "Vyhrál" else 0, axis=1)

    celkovy_zisk = df["výhra"].sum() - df["castka"].sum()
    celkovy_zisk_penez = celkovy_zisk
    prumerny_kurz = df["kurz"].mean()
    uspesne_kurzy = df[df["výhra"] > 0]["kurz"]
    prumerny_uspesny_kurz = uspesne_kurzy.mean() if not uspesne_kurzy.empty else 0
else:
    celkovy_zisk = celkovy_zisk_penez = prumerny_kurz = prumerny_uspesny_kurz = 0

# Výstup statistik
st.header("Celkový výsledek")
st.markdown(
    f'<div style="padding: 10px; background-color: {"#4CAF50" if celkovy_zisk >= 0 else "#FF5252"}; border-radius: 5px; color: white;">'
    f'Celkový zisk: {celkovy_zisk:.2f} Kč</div>', unsafe_allow_html=True
)
st.markdown(
    f'<div style="padding: 10px; background-color: {"#4CAF50" if celkovy_zisk_penez >= 0 else "#FF5252"}; border-radius: 5px; color: white;">'
    f'Celkový zisk v penězích: {celkovy_zisk_penez:.2f} Kč</div>', unsafe_allow_html=True
)

st.markdown(f"Průměrný kurz: {prumerny_kurz:.2f}")
st.markdown(f"Průměrný úspěšný kurz: {prumerny_uspesny_kurz:.2f}")

# Zobrazení všech tiketů
if st.session_state.tikety:
    st.header("Historie tiketů")

    # Výpis tiketů s tlačítky pro editaci a smazání
    for i, tiket in enumerate(st.session_state.tikety):
        with st.container():
            st.write(f"Tiket {i+1}: {tiket['castka']} Kč, Kurz: {tiket['kurz']}, Výsledek: {tiket['vysledek']}")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"Upravit {i+1}", key=f"edit_{i}"):
                    castka_upravit = st.number_input(f"Nová částka pro tiket {i+1}", value=tiket['castka'], min_value=0.0, step=0.1, key=f"castka_{i}")
                    kurz_upravit = st.number_input(f"Nový kurz pro tiket {i+1}", value=tiket['kurz'], min_value=1.0, step=0.01, key=f"kurz_{i}")
                    vysledek_upravit = st.radio(f"Nový výsledek pro tiket {i+1}", ["Vyhrál", "Prohrál"], 
                                                index=["Vyhrál", "Prohrál"].index(tiket['vysledek']), key=f"vysledek_{i}")
                    
                    if st.button(f"Potvrdit úpravy {i+1}", key=f"confirm_{i}"):
                        st.session_state.tikety[i] = {"castka": castka_upravit, "kurz": kurz_upravit, "vysledek": vysledek_upravit}
                        st.experimental_set_query_params(updated="true")
                        st.success(f"Tiket {i+1} upraven: {castka_upravit} Kč, Kurz: {kurz_upravit}, Výsledek: {vysledek_upravit}")

            with col2:
                if st.button(f"Smazat {i+1}", key=f"delete_{i}"):
                    st.session_state.tikety.pop(i)
                    st.experimental_set_query_params(updated="true")
                    st.success(f"Tiket {i+1} byl smazán")
                    break 
