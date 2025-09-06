import streamlit as st
import plotly.graph_objects as go

# --- Configuração da página ---
st.set_page_config(page_title="Comparador de Descontos", layout="centered")
st.title("💸 Comparador de Descontos")

# --- Valores padrão ---
DEFAULTS = {
    'aluguer': 280.0,
    'perc_aluguer': 7.0,
    'seguro': 45.0,
    'perc_seguro': 12.0,
    'manutencao': 50.0
}

# Inicializa o estado da sessão
if 'show_inputs' not in st.session_state:
    st.session_state.show_inputs = False
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Entradas ---
st.header("Entradas do Usuário")
apuro = st.number_input("💰 Apuro total (€)", min_value=0.0, value=700.0, step=10.0)
desc_combustivel = st.number_input("⛽ Desconto de Combustível (€)", min_value=0.0, value=200.0, step=1.0)
horas_trabalho = st.number_input("⏱️ Número de horas trabalhadas", min_value=1.0, value=40.0, step=1.0)
st.markdown("---")

# --- Opções ---
st.header("Opções da Empresa")
if st.button("Modificar Opções Padrão"):
    st.session_state.show_inputs = not st.session_state.show_inputs

if st.session_state.show_inputs:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Alugado")
        st.number_input("🏠 Aluguer (€)", min_value=0.0, value=st.session_state.aluguer, step=1.0, key='aluguer')
        st.number_input("👔 Percentual (%)", min_value=0.0, value=st.session_state.perc_aluguer, step=0.5, key='perc_aluguer')
    with col2:
        st.subheader("Próprio")
        st.number_input("🛡️ Seguro (€)", min_value=0.0, value=st.session_state.seguro, step=1.0, key='seguro')
        st.number_input("👔 Percentual (%)", min_value=0.0, value=st.session_state.perc_seguro, step=0.5, key='perc_seguro')
        st.number_input("🛠️ Manutenção (€)", min_value=0.0, value=st.session_state.manutencao, step=1.0, key='manutencao')
else:
    st.info("Valores padrão das opções estão sendo usados. Clique no botão acima para modificá-los.")

st.markdown("---")

# --- Cálculo e Dashboard Interativo ---
if st.button("Calcular 🔹", type="primary"):
    # Preparar dados
    apuro_liquido = apuro - desc_combustivel
    opcoes = {k: st.session_state[k] for k in ['aluguer', 'perc_aluguer', 'seguro', 'perc_seguro', 'manutencao']}

    # Cálculos
    sobra_opcao1 = apuro_liquido - (apuro * opcoes['perc_aluguer'] / 100) - opcoes['aluguer']
    sobra_opcao2 = apuro_liquido - (apuro * opcoes['perc_seguro'] / 100) - opcoes['seguro'] - opcoes['manutencao']

    ganho_hora_opcao1 = sobra_opcao1 / max(horas_trabalho, 1)
    ganho_hora_opcao2 = sobra_opcao2 / max(horas_trabalho, 1)

    st.subheader("📊 Resultados:")
    st.metric("Apuro Líquido", f"{apuro_liquido:,.2f} €")
    st.metric("Horas Trabalhadas", f"{horas_trabalho:,.0f} h")
    st.markdown("---")

    # Determinar a melhor opção com base na sobra
    if sobra_opcao1 > sobra_opcao2:
        melhor_idx = 0
    elif sobra_opcao2 > sobra_opcao1:
        melhor_idx = 1
    else:
        melhor_idx = -1  # empate

    # Abas
    tab1, tab2 = st.tabs(["📈 Dashboard", "🧮 Detalhes dos Cálculos"])
    with tab1:
        st.write("### Comparação Financeira com Destaque de Melhor Opção")

        categorias = ["Opção 1 (Alugado)", "Opção 2 (Próprio)"]

        # Cores condicionais
        cores_sobra = ['#4caf50' if melhor_idx == 0 else '#a5d6a7', '#2196f3' if melhor_idx == 1 else '#90caf9']
        cores_ganho = ['#4caf50' if melhor_idx == 0 else '#a5d6a7', '#2196f3' if melhor_idx == 1 else '#90caf9']

        fig = go.Figure()

        # Barra da Sobra (€)
        fig.add_trace(go.Bar(
            y=categorias,
            x=[sobra_opcao1, sobra_opcao2],
            name='Sobra (€)',
            orientation='h',
            marker_color=cores_sobra,
            text=[f"{'🏆 ' if melhor_idx==0 else ''}{sobra_opcao1:,.2f} €",
                  f"{'🏆 ' if melhor_idx==1 else ''}{sobra_opcao2:,.2f} €"],
            textposition='auto'
        ))

        # Barra do Ganho/Hora (€)
        fig.add_trace(go.Bar(
            y=categorias,
            x=[ganho_hora_opcao1, ganho_hora_opcao2],
            name='Ganho/Hora (€/h)',
            orientation='h',
            marker_color=cores_ganho,
            text=[f"{'🏆 ' if melhor_idx==0 else ''}{ganho_hora_opcao1:,.2f} €/h",
                  f"{'🏆 ' if melhor_idx==1 else ''}{ganho_hora_opcao2:,.2f} €/h"],
            textposition='auto'
        ))

        fig.update_layout(
            barmode='group',
            title="💰 Comparativo Financeiro",
            xaxis_title="Valor",
            yaxis_title="Opções",
            legend_title="Indicadores",
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)

        # Mensagem complementar
        if melhor_idx == 0:
            st.success(f"🎉 Melhor escolha: **Opção 1 (Alugado)**, diferença de **{sobra_opcao1 - sobra_opcao2:,.2f} €**")
        elif melhor_idx == 1:
            st.success(f"🎉 Melhor escolha: **Opção 2 (Próprio)**, diferença de **{sobra_opcao2 - sobra_opcao1:,.2f} €**")
        else:
            st.info("As duas opções resultam no mesmo valor.")

    with tab2:
        st.write("### Detalhes dos Cálculos")
        st.markdown(f"""
**Opção 1 (Alugado):**
- Apuro Líquido: {apuro_liquido:,.2f} €
- Dedução da Empresa: {apuro:,.2f} € * ({opcoes['perc_aluguer']}%) = {(apuro*opcoes['perc_aluguer']/100):,.2f} €
- Dedução de Aluguer: {opcoes['aluguer']:,.2f} €
- Valor Final: {sobra_opcao1:,.2f} €
- Ganho por Hora: {ganho_hora_opcao1:,.2f} €/h

**Opção 2 (Próprio):**
- Apuro Líquido: {apuro_liquido:,.2f} €
- Dedução da Empresa: {apuro:,.2f} € * ({opcoes['perc_seguro']}%) = {(apuro*opcoes['perc_seguro']/100):,.2f} €
- Dedução de Seguro: {opcoes['seguro']:,.2f} €
- Dedução de Manutenção: {opcoes['manutencao']:,.2f} €
- Valor Final: {sobra_opcao2:,.2f} €
- Ganho por Hora: {ganho_hora_opcao2:,.2f} €/h
""")
