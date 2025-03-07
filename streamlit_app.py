import streamlit as st
import pandas as pd

# Inicializace session state pro ukládání tiketů
if "tikety" not in st.session_state:
    st.session_state.tikety = []

st.title("Sázková statistika")

# Vstupní formulář
st.header("Přidat tiket")
with st.form(key="pridat_tiket"):
    castka = st.number_input("Vložená částka", min_value=0.0, step=0.1)
    kurz = st.number_input("Kurz", min_value=1.0, step=0.01)
    vysledek = st.radio("Výsledek", ["Vyhrál", "Prohrál"], horizontal=True)
    pridat = st.form_submit_button("Přidat tiket")

    if pridat:
        st.session_state.tikety.append({"castka": castka, "kurz": kurz, "vysledek": vysledek})
        st.experimental_rerun()

# Výpočty statistik
if st.session_state.tikety:
    df = pd.DataFrame(st.session_state.tikety)
    df["výhra"] = df.apply(lambda row: row["castka"] * row["kurz"] if row["vysledek"] == "Vyhrál" else 0, axis=1)
    celkovy_zisk = df["výhra"].sum() - df["castka"].sum()
    prumerny_kurz = df["kurz"].mean()
    uspesne_kurzy = df[df["výhra"] > 0]["kurz"]
    prumerny_uspesny_kurz = uspesne_kurzy.mean() if not uspesne_kurzy.empty else 0

    # Výstup statistik
    st.header("Celkový výsledek")
    st.markdown(f'<div style="padding: 10px; background-color: {"#4CAF50" if celkovy_zisk >= 0 else "#FF5252"}; border-radius: 5px; color: white;">Celkový zisk: {celkovy_zisk:.2f} Kč</div>', unsafe_allow_html=True)
    st.markdown(f"Průměrný kurz: {prumerny_kurz:.2f}")
    st.markdown(f"Průměrný úspěšný kurz: {prumerny_uspesny_kurz:.2f}")

    # Zobrazení tiketů s možností úpravy a smazání
    st.header("Historie tiketů")
    for i, tiket in enumerate(st.session_state.tikety):
        with st.expander(f"Tiket {i+1}: {tiket['castka']} Kč, Kurz: {tiket['kurz']}, Výsledek: {tiket['vysledek']}"):
            with st.form(key=f"edit_tiket_{i}"):
                castka_upravit = st.number_input("Nová částka", value=tiket['castka'], min_value=0.0, step=0.1)
                kurz_upravit = st.number_input("Nový kurz", value=tiket['kurz'], min_value=1.0, step=0.01)
                vysledek_upravit = st.radio("Nový výsledek", ["Vyhrál", "Prohrál"], index=["Vyhrál", "Prohrál"].index(tiket['vysledek']))
                upravit = st.form_submit_button("Upravit")

                if upravit:
                    st.session_state.tikety[i] = {"castka": castka_upravit, "kurz": kurz_upravit, "vysledek": vysledek_upravit}
                    st.experimental_rerun()
            
            if st.button(f"Smazat tiket {i+1}", key=f"delete_{i}"):
                del st.session_state.tikety[i]
                st.experimental_rerun()
