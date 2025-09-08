import streamlit as st
import pandas as pd

# --- Configuração da página ---
st.set_page_config(
    page_title="Comparador de Ganhos TVDE",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("🚗 Comparador de Ganhos TVDE")
st.markdown("""
Compare os ganhos e o custo por km entre usar carro alugado ou próprio como motorista TVDE.
*Insira os seus dados reais para obter resultados mais precisos.*
""")

# --- Inicialização dos parâmetros com valores padrão ---
if 'params' not in st.session_state:
    st.session_state.params = {
        'show_params': False,
        'rental_cost': 270.0,
        'rental_commission': 6.0,
        'own_insurance': 45.0,
        'own_maintenance': 50.0,
        'own_commission': 12.0,
        'extra_expenses': 0.0,
        'include_extra_expenses': False,
        'calculation_type': None,
        'weekly_earnings': 700.0,
        'weekly_hours': 40.0,
        'fuel_cost': 170.0,
        'weekly_km': 1200.0
    }

# --- Função para formatar moeda ---
def format_currency(value):
    return f"€{value:,.2f}".replace(',', ' ').replace('.', ',').replace(' ', '.')

# --- Entradas principais ---
st.header("📊 Dados de Entrada")
col1, col2 = st.columns(2)

with col1:
    st.session_state.params['weekly_earnings'] = st.number_input(
        "Ganhos Brutos Semanais (€):",
        min_value=0.0,
        value=st.session_state.params['weekly_earnings'],
        step=50.0,
        format="%.2f"
    )
    st.session_state.params['weekly_hours'] = st.number_input(
        "Horas Trabalhadas por Semana:",
        min_value=0.0,
        value=st.session_state.params['weekly_hours'],
        step=1.0
    )

with col2:
    st.session_state.params['fuel_cost'] = st.number_input(
        "Custo Semanal com Combustível (€):",
        min_value=0.0,
        value=st.session_state.params['fuel_cost'],
        step=10.0,
        format="%.2f"
    )
    st.session_state.params['weekly_km'] = st.number_input(
        "Quilómetros percorridos por semana:",
        min_value=0.0,
        value=st.session_state.params['weekly_km'],
        step=50.0
    )

# --- Despesas extras ---
st.header("💸 Despesas Extras (Opcionais)")
extra_col1, extra_col2 = st.columns(2)

with extra_col1:
    st.session_state.params['include_extra_expenses'] = st.checkbox(
        "Incluir despesas extras nos cálculos",
        value=st.session_state.params['include_extra_expenses']
    )

with extra_col2:
    if st.session_state.params['include_extra_expenses']:
        st.session_state.params['extra_expenses'] = st.number_input(
            "Valor das Despesas Extras Semanais (€):",
            min_value=0.0,
            value=st.session_state.params['extra_expenses'],
            step=5.0,
            format="%.2f"
        )
    else:
        st.session_state.params['extra_expenses'] = 0.0

# --- Parâmetros avançados ---
with st.expander("⚙️ Parâmetros Avançados", expanded=st.session_state.params['show_params']):
    st.session_state.params['show_params'] = True
    adv_col1, adv_col2 = st.columns(2)

    with adv_col1:
        st.subheader("Carro Alugado")
        st.session_state.params['rental_cost'] = st.number_input(
            "Custo do Aluguel (€/semana):",
            min_value=0.0,
            value=st.session_state.params['rental_cost'],
            step=10.0,
            format="%.2f"
        )
        st.session_state.params['rental_commission'] = st.number_input(
            "Comissão com Carro Alugado (%):",
            min_value=0.0,
            max_value=30.0,
            value=st.session_state.params['rental_commission'],
            step=0.5,
            format="%.1f"
        )

    with adv_col2:
        st.subheader("Carro Próprio")
        st.session_state.params['own_insurance'] = st.number_input(
            "Seguro (€/semana):",
            min_value=0.0,
            value=st.session_state.params['own_insurance'],
            step=5.0,
            format="%.2f"
        )
        st.session_state.params['own_maintenance'] = st.number_input(
            "Manutenção (€/semana):",
            min_value=0.0,
            value=st.session_state.params['own_maintenance'],
            step=5.0,
            format="%.2f"
        )
        st.session_state.params['own_commission'] = st.number_input(
            "Comissão com Carro Próprio (%):",
            min_value=0.0,
            max_value=30.0,
            value=st.session_state.params['own_commission'],
            step=0.5,
            format="%.1f"
        )

# --- Botões de cálculo ---
st.header("🧮 Calcular")
calc_col1, calc_col2, calc_col3 = st.columns(3)

with calc_col1:
    if st.button("Calcular Carro Alugado"):
        st.session_state.params['calculation_type'] = "alugado"

with calc_col2:
    if st.button("Calcular Carro Próprio"):
        st.session_state.params['calculation_type'] = "proprio"

with calc_col3:
    if st.button("Comparar Ambos"):
        st.session_state.params['calculation_type'] = "comparar"

# --- Função de cálculo ---
def calcular_ganhos(params):
    resultados = {}
    weekly_earnings = params['weekly_earnings']
    weekly_hours = params['weekly_hours']
    fuel_cost = params['fuel_cost']
    weekly_km = params['weekly_km']
    extra_expenses = params['extra_expenses'] if params['include_extra_expenses'] else 0

    # Cálculo para carro alugado
    if params['calculation_type'] in ["alugado", "comparar"]:
        rental_comm = weekly_earnings * (params['rental_commission'] / 100)
        rental_net = weekly_earnings - rental_comm - params['rental_cost'] - fuel_cost - extra_expenses
        custo_km_alugado = (params['rental_cost'] + fuel_cost + rental_comm + extra_expenses) / weekly_km if weekly_km > 0 else 0
        resultados["alugado"] = {
            "bruto": weekly_earnings,
            "líquido": rental_net,
            "hora": rental_net / weekly_hours if weekly_hours > 0 else 0,
            "custo_km": custo_km_alugado,
            "comissao": rental_comm,
            "aluguel": params['rental_cost']
        }

    # Cálculo para carro próprio
    if params['calculation_type'] in ["proprio", "comparar"]:
        own_comm = weekly_earnings * (params['own_commission'] / 100)
        own_net = weekly_earnings - own_comm - params['own_insurance'] - params['own_maintenance'] - fuel_cost - extra_expenses
        custo_km_proprio = (params['own_insurance'] + params['own_maintenance'] + fuel_cost + own_comm + extra_expenses) / weekly_km if weekly_km > 0 else 0
        resultados["proprio"] = {
            "bruto": weekly_earnings,
            "líquido": own_net,
            "hora": own_net / weekly_hours if weekly_hours > 0 else 0,
            "custo_km": custo_km_proprio,
            "comissao": own_comm,
            "seguro": params['own_insurance'],
            "manutencao": params['own_maintenance']
        }

    # Cálculo da diferença (quando comparar)
    if params['calculation_type'] == "comparar":
        resultados["diferença"] = {
            "líquido": resultados["alugado"]["líquido"] - resultados["proprio"]["líquido"],
            "hora": resultados["alugado"]["hora"] - resultados["proprio"]["hora"],
            "custo_km": resultados["alugado"]["custo_km"] - resultados["proprio"]["custo_km"]
        }

    return resultados

# --- Executar cálculo e exibir resultados ---
if st.session_state.params['calculation_type']:
    resultados = calcular_ganhos(st.session_state.params)
    st.header("📈 Resultados")

    if st.session_state.params['calculation_type'] == "alugado":
        alugado = resultados["alugado"]
        col1, col2, col3 = st.columns(3)
        col1.metric("Líquido Semanal", format_currency(alugado['líquido']))
        col2.metric("Média Horária", format_currency(alugado['hora']))
        col3.metric("Custo por Km", format_currency(alugado['custo_km']))

        st.subheader("Detalhes:")
        st.write(f"- **Ganho Bruto:** {format_currency(alugado['bruto'])}")
        st.write(f"- **Comissão ({st.session_state.params['rental_commission']}%):** {format_currency(alugado['comissao'])}")
        st.write(f"- **Aluguel:** {format_currency(alugado['aluguel'])}")
        st.write(f"- **Combustível:** {format_currency(st.session_state.params['fuel_cost'])}")
        if st.session_state.params['include_extra_expenses']:
            st.write(f"- **Despesas Extras:** {format_currency(st.session_state.params['extra_expenses'])}")

    elif st.session_state.params['calculation_type'] == "proprio":
        proprio = resultados["proprio"]
        col1, col2, col3 = st.columns(3)
        col1.metric("Líquido Semanal", format_currency(proprio['líquido']))
        col2.metric("Média Horária", format_currency(proprio['hora']))
        col3.metric("Custo por Km", format_currency(proprio['custo_km']))

        st.subheader("Detalhes:")
        st.write(f"- **Ganho Bruto:** {format_currency(proprio['bruto'])}")
        st.write(f"- **Comissão ({st.session_state.params['own_commission']}%):** {format_currency(proprio['comissao'])}")
        st.write(f"- **Seguro:** {format_currency(proprio['seguro'])}")
        st.write(f"- **Manutenção:** {format_currency(proprio['manutencao'])}")
        st.write(f"- **Combustível:** {format_currency(st.session_state.params['fuel_cost'])}")
        if st.session_state.params['include_extra_expenses']:
            st.write(f"- **Despesas Extras:** {format_currency(st.session_state.params['extra_expenses'])}")

    elif st.session_state.params['calculation_type'] == "comparar":
        alugado = resultados["alugado"]
        proprio = resultados["proprio"]
        diferenca = resultados["diferença"]

        st.subheader("Comparação Direta")
        col1, col2, col3 = st.columns(3)
        col1.metric("Alugado - Líquido", format_currency(alugado['líquido']))
        col2.metric("Próprio - Líquido", format_currency(proprio['líquido']))
        col3.metric("Diferença", format_currency(diferenca['líquido']),
                   delta_color="inverse" if diferenca['líquido'] < 0 else "normal")

        col1, col2, col3 = st.columns(3)
        col1.metric("Alugado - €/h", format_currency(alugado['hora']))
        col2.metric("Próprio - €/h", format_currency(proprio['hora']))
        col3.metric("Diferença - €/h", format_currency(diferenca['hora']),
                   delta_color="inverse" if diferenca['hora'] < 0 else "normal")

        col1, col2, col3 = st.columns(3)
        col1.metric("Alugado - €/km", format_currency(alugado['custo_km']))
        col2.metric("Próprio - €/km", format_currency(proprio['custo_km']))
        col3.metric("Diferença - €/km", format_currency(diferenca['custo_km']),
                   delta_color="inverse" if diferenca['custo_km'] > 0 else "normal")

        # Recomendação baseada nos resultados
        st.subheader("💡 Recomendação:")
        if diferenca['líquido'] > 0:
            st.success("Com os valores atuais, **alugar o carro** parece ser mais vantajoso economicamente.")
            st.write(f"Você ganharia **{format_currency(diferenca['líquido'])}** a mais por semana com o carro alugado.")
        elif diferenca['líquido'] < 0:
            st.success("Com os valores atuais, **usar carro próprio** parece ser mais vantajoso economicamente.")
            st.write(f"Você ganharia **{format_currency(-diferenca['líquido'])}** a mais por semana com o carro próprio.")
        else:
            st.info("Os dois cenários apresentam resultados financeiros semelhantes.")

# --- Informações adicionais ---
with st.expander("ⓘ Informações e Dicas"):
    st.markdown("""
    ### Como usar este comparador:
    1. Insira seus **ganhos brutos semanais** (o que você fatura antes de descontar qualquer despesa)
    2. Informe suas **horas trabalhadas** e **quilómetros percorridos** por semana
    3. Adicione o **custo com combustível** (você pode calcular isso multiplicando os litros consumidos pelo preço do combustível)
    4. Nos parâmetros avançados, ajuste os valores conforme sua realidade (comissões, custos de aluguel, etc.)
    5. Clique nos botões para ver os resultados

    ### O que considerar:
    - **Carro alugado**: Geralmente tem comissões mais baixas, mas você paga o aluguel
    - **Carro próprio**: Comissões mais altas, mas você não paga aluguel (apenas manutenção e seguro)
    - **Despesas extras**: Portagens, lavagens, multas, etc. podem ser incluídas para um cálculo mais realista
    - **Depreciação**: Se usar carro próprio, considere a depreciação do veículo (não incluída nestes cálculos)

    ### Dicas para motoristas TVDE:
    - Mantenha um registro detalhado de todas as suas despesas
    - Considere fazer a declaração de IRS como trabalhador independente para deduzir despesas
    - Analise periodicamente se continua compensando usar carro alugado ou próprio
    """)
