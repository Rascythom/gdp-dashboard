import streamlit as st

# Inicializace session_state pro uchování tiketů
if 'tickets' not in st.session_state:
    st.session_state.tickets = []

st.title("Sázkový Tracker")

# Formulář pro přidání tiketu
with st.form("add_ticket_form"):
    amount = st.number_input("Vsazená částka (Kč):", min_value=1.0, step=1.0)
    odds = st.number_input("Kurz:", min_value=1.01, step=0.01)
    won = st.radio("Výsledek:", ["Vyhrál", "Prohrál"], horizontal=True)
    submit_button = st.form_submit_button("Přidat tiket")

if submit_button:
    st.session_state.tickets.append({"amount": amount, "odds": odds, "won": won})

# Zobrazení tiketů
for ticket in st.session_state.tickets:
    border_color = "#808080"  # Šedá pro neutrální zobrazení
    st.markdown(
        f'<div style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-bottom: 5px;">'
        f'Tiket přidán: {ticket["amount"]} Kč, Kurz: {ticket["odds"]}, Výsledek: {ticket["won"]}'
        f'</div>', unsafe_allow_html=True)

# Výpočty statistik
if st.session_state.tickets:
    total_bet = sum(t["amount"] for t in st.session_state.tickets)
    total_winnings = sum(t["amount"] * (t["odds"] if t["won"] == "Vyhrál" else 0) for t in st.session_state.tickets)
    net_profit = total_winnings - total_bet
    roi = (net_profit / total_bet) * 100 if total_bet > 0 else 0
    avg_odds = sum(t["odds"] for t in st.session_state.tickets) / len(st.session_state.tickets)
    successful_tickets = [t for t in st.session_state.tickets if t["won"] == "Vyhrál"]
    avg_successful_odds = sum(t["odds"] for t in successful_tickets) / len(successful_tickets) if successful_tickets else 0
    
    # Výběr barvy podle zisku
    result_color = "#00C851" if net_profit >= 0 else "#ff4444"  # Zelená pro zisk, červená pro ztrátu
    
    st.markdown(
        f'<div style="border: 2px solid {result_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">'
        f'<b>Celkový výsledek:</b><br>'
        f'Zisk: {net_profit:.2f} Kč<br>'
        f'ROI: {roi:.2f} %<br>'
        f'Průměrný kurz: {avg_odds:.2f}<br>'
        f'Průměrný úspěšný kurz: {avg_successful_odds:.2f}'
        f'</div>', unsafe_allow_html=True)
