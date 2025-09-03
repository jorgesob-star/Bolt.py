import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora de Descontos (sem Uber)", layout="centered")
st.title("💸 Calculadora de Descontos (sem Uber)")
st.markdown("Calcule rapidamente os descontos do Patrão, Seguro e Combustível.")

# Entradas
st.subheader("Insira os valores:")

valor_inicial = st.number_input("💰 Valor inicial", min_value=0.0, value=100.0, step=10.0)
perc_pat = st.number_input("👔 Percentagem Patrão (%)", min_value=0.0, value=12.0, step=1.0)
desc_seguro = st.number_input("🛡️ Aluguer ou Seguro", min_value=0.0, value=6.0, step=1.0)
desc_combustivel = st.number_input("⛽ Desconto Combustível", min_value=0.0, value=30.0, step=1.0)

st.markdown("---")

if st.button("Calcular 🔹", use_container_width=True):
    st.subheader("📊 Resultado detalhado:")

    valor = valor_inicial

    # Patrão
    desconto_pat = valor * (perc_pat / 100)
    valor -= desconto_pat
    st.markdown(f"<div style='background-color:#CCE5FF;padding:10px;border-radius:5px'>"
                f"- {perc_pat}% Patrão: -{desconto_pat:.2f} → {valor:.2f}</div>", unsafe_allow_html=True)

    # Seguro
    valor -= desc_seguro
    st.markdown(f"<div style='background-color:#CCFFCC;padding:10px;border-radius:5px'>"
                f"- Seguro: -{desc_seguro:.2f} → {valor:.2f}</div>", unsafe_allow_html=True)

    # Combustível
    valor -= desc_combustivel
    st.markdown(f"<div style='background-color:#FFF2CC;padding:10px;border-radius:5px'>"
                f"- Combustível: -{desc_combustivel:.2f} → {valor:.2f}</div>", unsafe_allow_html=True)

    st.success(f"💰 Valor final após descontos: {valor:.2f}")
