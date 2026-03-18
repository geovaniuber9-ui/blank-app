import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS LuzSocial v12.1", page_icon="⚡", layout="wide")

# ESTILO PREMIUM
st.markdown("""
    <style>
    .main { background-color: #0B0E14; color: #E0E0E0; }
    [data-testid="stSidebar"] { background-image: linear-gradient(#050A30, #001219) !important; }
    .card-premium {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 15px; margin-bottom: 10px;
    }
    .valor-liq { color: #00E676; font-size: 24px; font-weight: bold; }
    .stButton>button { background: linear-gradient(90deg, #00D4FF, #0052D4); color: white; border-radius: 10px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO DE ESTADOS
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 0.0
if 'status' not in st.session_state: st.session_state.status = "menu"
if 'missao_selecionada' not in st.session_state: st.session_state.missao_selecionada = None

# FUNÇÃO PARA ACEITAR MISSÃO (CORRIGE O ERRO DO BOTÃO)
def aceitar_missao(nome, valor):
    st.session_state.missao_atual = {"nome": nome, "valor": valor}
    st.session_state.status = "mapa"
    st.toast(f"Missão {nome} Aceita!")

# --- LOGIN ---
if not st.session_state.logado:
    st.title("⚡ GS CONSULTORIA")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")
    if st.button("ACESSAR"):
        st.session_state.logado = True
        st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f"### 👤 Geovani Santi")
    st.markdown(f"## 💰 R$ {st.session_state.saldo:.2f}")
    st.divider()
    menu = st.radio("Ir para:", ["Mural", "Escola", "Suporte"])
    if st.button("🚪 Sair"): 
        st.session_state.logado = False
        st.rerun()

# --- MURAL DE MISSÕES (ESTRUTURA DE BOTÃO REFEITA) ---
if menu == "Mural" and st.session_state.status == "menu":
    st.title("📍 Radar de Missões")
    
    tabs = st.tabs(["🩺 Saúde", "👩‍🍳 Cozinha", "🧹 Zeladoria"])

    with tabs[0]: # ABA SAÚDE
        v = {"n": "Acompanhante Idoso", "l": "Vila Yara", "b": 120.0}
        liq = v['b'] * 0.85
        st.markdown(f'<div class="card-premium"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><div class="valor-liq">R$ {liq:.2f}</div></div>', unsafe_allow_html=True)
        # O segredo é usar o on_click para mudar o estado imediatamente
        st.button("ACEITAR ESTA MISSÃO", key="btn_saude", on_click=aceitar_missao, args=(v['n'], liq))

    with tabs[1]: # ABA COZINHA
        v = {"n": "Marmitas do Dia", "l": "Bela Vista", "b": 150.0}
        liq = v['b'] * 0.85
        st.markdown(f'<div class="card-premium"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><div class="valor-liq">R$ {liq:.2f}</div></div>', unsafe_allow_html=True)
        st.button("ACEITAR ESTA MISSÃO", key="btn_cozinha", on_click=aceitar_missao, args=(v['n'], liq))

    with tabs[2]: # ABA ZELADORIA
        v = {"n": "Limpeza de Praça", "l": "Centro", "b": 40.0}
        liq = v['b'] * 0.85
        st.markdown(f'<div class="card-premium"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><div class="valor-liq">R$ {liq:.2f}</div></div>', unsafe_allow_html=True)
        st.button("ACEITAR ESTA MISSÃO", key="btn_zeladoria", on_click=aceitar_missao, args=(v['n'], liq))

# --- FLUXO DE EXECUÇÃO (MAPA -> FOTO) ---
if st.session_state.status == "mapa":
    st.header(f"📍 Rota: {st.session_state.missao_atual['nome']}")
    st.info("Siga para o local indicado no GPS.")
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("CHEGUEI AO LOCAL"):
        st.session_state.status = "foto"
        st.rerun()

elif st.session_state.status == "foto":
    st.header("📸 Finalizar Serviço")
    st.camera_input("Tire uma foto do trabalho concluído")
    if st.button("CONFIRMAR CONCLUSÃO"):
        st.session_state.saldo += st.session_state.missao_atual['valor']
        st.session_state.status = "pago"
        st.rerun()

elif st.session_state.status == "pago":
    st.balloons()
    st.success(f"Pagamento de R$ {st.session_state.missao_atual['valor']:.2f} creditado!")
    if st.button("VOLTAR AO MURAL"):
        st.session_state.status = "menu"
        st.rerun()
        
