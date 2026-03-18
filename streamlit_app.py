import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS LuzSocial v13.0", page_icon="⚡", layout="wide")

# ESTILO DARK MODE ELITE (RECUPERADO E MELHORADO)
st.markdown("""
    <style>
    .main { background-color: #0B0E14; color: #E0E0E0; }
    [data-testid="stSidebar"] { background-image: linear-gradient(#050A30, #001219) !important; border-right: 1px solid #1A237E; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    .card-premium {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px; border-radius: 20px; margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    .valor-liq { color: #00E676; font-size: 28px; font-weight: bold; text-shadow: 0 0 10px rgba(0,230,118,0.3); }
    .badge { background: #1A237E; color: #00D4FF; padding: 5px 15px; border-radius: 50px; font-size: 12px; font-weight: bold; border: 1px solid #00D4FF; }
    .stButton>button {
        background: linear-gradient(90deg, #00D4FF, #0052D4);
        color: white; border: none; border-radius: 12px; font-weight: bold; padding: 15px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO DE VARIÁVEIS
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 0.0
if 'status' not in st.session_state: st.session_state.status = "menu"
if 'missao_atual' not in st.session_state: st.session_state.missao_atual = None

# FUNÇÕES DE FLUXO
def aceitar(nome, valor):
    st.session_state.missao_atual = {"nome": nome, "valor": valor}
    st.session_state.status = "mapa"

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center; color: #00D4FF;'>⚡ GS CONSULTORIA</h1>", unsafe_allow_html=True)
    with st.container():
        u = st.text_input("Usuário (CPF)")
        s = st.text_input("Senha", type="password")
        if st.button("ACESSAR DASHBOARD"):
            st.session_state.logado = True; st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 👤 Geovani Santi")
    st.markdown(f"## 💰 Saldo: R$ {st.session_state.saldo:.2f}")
    st.progress(min(st.session_state.saldo / 500.0, 1.0))
    st.divider()
    menu = st.radio("Menu:", ["Mural de Elite", "Meu Extrato", "Suporte"])
    if st.button("🚪 Sair"): st.session_state.logado = False; st.rerun()

# --- TELA PRINCIPAL: MURAL ---
if st.session_state.status == "menu":
    st.title("🚀 Radar de Missões Osasco")
    t1, t2, t3, t4 = st.tabs(["🩺 Saúde", "👩‍🍳 Cozinha", "🧹 Zeladoria", "♻️ Reciclagem"])

    with t1:
        v = {"n": "Acompanhante Idoso", "l": "Vila Yara", "b": 120.0}
        liq = v['b'] * 0.85
        st.markdown(f'<div class="card-premium"><span class="badge">SAÚDE</span><h2>{v["n"]}</h2><p>📍 {v["l"]}</p><div class="valor-liq">R$ {liq:.2f}</div></div>', unsafe_allow_html=True)
        st.button("ACEITAR ESTA MISSÃO", key="saude", on_click=aceitar, args=(v['n'], liq))

    with t2:
        v = {"n": "Marmitas do Dia", "l": "Bela Vista", "b": 150.0}
        liq = v['b'] * 0.85
        st.markdown(f'<div class="card-premium"><span class="badge">COZINHA</span><h2>{v["n"]}</h2><p>📍 {v["l"]}</p><div class="valor-liq">R$ {liq:.2f}</div></div>', unsafe_allow_html=True)
        st.button("ACEITAR ESTA MISSÃO", key="cozinha", on_click=aceitar, args=(v['n'], liq))

    with t3:
        v = {"n": "Varrição de Praça", "l": "Centro", "b": 40.0}
        liq = v['b'] * 0.85
        st.markdown(f'<div class="card-premium"><span class="badge">ZELADORIA</span><h2>{v["n"]}</h2><p>📍 {v["l"]}</p><div class="valor-liq">R$ {liq:.2f}</div></div>', unsafe_allow_html=True)
        st.button("ACEITAR ESTA MISSÃO", key="zeladoria", on_click=aceitar, args=(v['n'], liq))

    with t4:
        v = {"n": "Coleta de Óleo", "l": "Km 18", "b": 30.0}
        liq = v['b'] * 0.90
        st.markdown(f'<div class="card-premium"><span class="badge">RECICLAGEM</span><h2>{v["n"]}</h2><p>📍 {v["l"]}</p><div class="valor-liq">R$ {liq:.2f}</div></div>', unsafe_allow_html=True)
        st.button("ACEITAR ESTA MISSÃO", key="recicla", on_click=aceitar, args=(v['n'], liq))

# --- FLUXO DE EXECUÇÃO ---
elif st.session_state.status == "mapa":
    st.header(f"📍 Destino: {st.session_state.missao_atual['nome']}")
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("CHEGUEI NO LOCAL"):
        st.session_state.status = "selfie"
        st.rerun()

elif st.session_state.status == "selfie":
    st.header("🤳 Selfie de Validação")
    st.info("Tire uma selfie no local para validar o início do serviço.")
    selfie = st.camera_input("Selfie de Segurança")
    if selfie:
        if st.button("VALIDAR E INICIAR"):
            st.session_state.status = "foto_final"
            st.rerun()

elif st.session_state.status == "foto_final":
    st.header("📸 Conclusão de Serviço")
    st.info("Tire uma foto do trabalho finalizado para liberação do pagamento.")
    foto = st.camera_input("Foto do Trabalho")
    if foto:
        if st.button("FINALIZAR E RECEBER"):
            st.session_state.saldo += st.session_state.missao_atual['valor']
            st.session_state.status = "pago"
            st.rerun()

elif st.session_state.status == "pago":
    st.balloons()
    st.success(f"Pagamento de R$ {st.session_state.missao_atual['valor']:.2f} concluído!")
    if st.button("VOLTAR AO DASHBOARD"):
        st.session_state.status = "menu"
        st.rerun()
    
