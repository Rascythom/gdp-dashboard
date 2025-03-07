import streamlit as st
import pandas as pd

# Inicializace session state
if 'tickets' not in st.session_state:
    st.session_state.tickets = []

def add_ticket(amount, odds, won):
    st.session_state.tickets.append({'amount': amount, 'odds': odds, 'won': won})

def calculate_statistics():
    df = pd.DataFrame(st.session_state.tickets)
    if df.empty:
        return 0, 0, 0, 0
    
    df['payout'] = df.apply(lambda x: x['amount'] * x['odds'] if x['won'] else 0, axis=1)
    df['profit'] = df['payout'] - df['amount']
    total_profit = df['profit'].sum()
    total_amount = df['amount'].sum()
    profit_percentage = (total_profit / total_amount) * 100 if total_amount != 0 else 0
    avg_odds = df['odds'].mean()
    successful_bets = df[df['won']]
    avg_successful_odds = successful_bets['odds'].mean() if not successful_bets.empty else 0
    
    return total_profit, profit_percentage, avg_odds, avg_successful_odds

st.title("Sázková statistika")

amount = st.number_input("Částka na tiket", min_value=1, step=1)
odds = st.number_input("Kurz", min_value=1.0, step=0.01)
won = st.radio("Výsledek", ["Vyhrál", "Prohrál"])

if st.button("Přidat tiket"):
    add_ticket(amount, odds, won == "Vyhrál")
    st.success(f"Tiket přidán: {amount} Kč, Kurz: {odds}, Výsledek: {won}", icon="✅")

# Výpočty statistik
total_profit, profit_percentage, avg_odds, avg_successful_odds = calculate_statistics()

# Určení barvy podle výsledku
profit_color = "#90EE90" if total_profit >= 0 else "#FF7F7F"  # Zelená pro zisk, červená pro ztrátu

# Výpis celkových statistik
st.markdown(f'''<div style="background-color: {profit_color}; padding: 10px; border-radius: 5px; text-align: center;">
    <b>Celkový zisk: {profit_percentage:.2f}%</b><br>
    <b>Celkový zisk v penězích: {total_profit:.2f} Kč</b><br>
    <b>Průměrný kurz: {avg_odds:.2f}</b><br>
    <b>Průměrný úspěšný kurz: {avg_successful_odds:.2f}</b>
</div>''', unsafe_allow_html=True)
