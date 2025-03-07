import streamlit as st

# Funkce pro výpočet procentuální úspěšnosti
def calculate_success_rate(total_bet, total_profit):
    if total_bet == 0:
        return 0
    return (total_profit / total_bet) * 100

# Inicializace proměnných
if 'total_bet' not in st.session_state:
    st.session_state.total_bet = 0
if 'total_profit' not in st.session_state:
    st.session_state.total_profit = 0
if 'bets_count' not in st.session_state:
    st.session_state.bets_count = 0

# Úvodní nadpis
st.title('Sportovní sázení - Statistiky')

# Zadávání údajů
bet_amount = st.number_input('Zadejte částku sázky (Kč)', min_value=0, step=1)
bet_odds = st.number_input('Zadejte kurz tiketu', min_value=1.0, step=0.1)
bet_result = st.selectbox('Výsledek tiketu', ['Vyhrál', 'Prohrál'])

# Výpočet výsledku tiketu
if bet_result == 'Vyhrál':
    profit = bet_amount * bet_odds - bet_amount  # Zisk po odečtení vkladu
else:
    profit = -bet_amount  # Ztráta, pokud tiket nevyjde

# Aktualizace celkového sázení a zisku
st.session_state.total_bet += bet_amount
st.session_state.total_profit += profit
st.session_state.bets_count += 1

# Zobrazení výsledků
st.write(f"Celkové sázení: {st.session_state.total_bet} Kč")
st.write(f"Celkový zisk/ztráta: {st.session_state.total_profit} Kč")
st.write(f"Počet tiketů: {st.session_state.bets_count}")

# Výpočet a zobrazení úspěšnosti
success_rate = calculate_success_rate(st.session_state.total_bet, st.session_state.total_profit)
st.write(f"Úspěšnost: {success_rate:.2f}%")
