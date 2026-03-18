import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS LuzSocial v16.0", page_icon="⚡", layout="wide")

# ESTILO PREMIUM DARK MODE
st.markdown("""
    <style>
    .main { background-color: #0B0E14; color: #E0E0E0; }
    [data-testid="stSidebar"] { background-image: linear-gradient(#050A30, #001219) !important; border-right: 1px solid #1A237E; }
    .card-premium {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 15px; margin-bottom: 15px;
    }
    .valor-liq { color: #00E676; font-size: 26px; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(90deg, #00D4FF, #0052D4);
        color: white; border-radius: 12px; font-weight: bold; padding: 12px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO DE ESTADOS
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 0.0
if 'status' not in st.session_state: st.session_state.status = "menu"
if 'missao_atual' not in st.session_state: st.session_state.missao_atual = None

def aceitar(nome, valor, local):
    st.session_state.missao_atual = {"nome": nome, "valor": valor, "local": local}
    st.session_state.status = "mapa"

# --- LOGIN ---
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center; color: #00D4FF;'>⚡ GS CONSULTORIA</h1>", unsafe_allow_html=True)
    if st.button("ACESSAR DASHBOARD"):
        st.session_state.logado = True; st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f"### 👤 Geovani Santi\n## 💰 R$ {st.session_state.saldo:.2f}")
    st.divider()
    if st.button("🚪 Sair"): st.session_state.logado = False; st.rerun()

# --- TELA 1: MURAL ---
if st.session_state.status == "menu":
    st.title("📍 Radar de Missões")
    tabs = st.tabs(["🩺 Saúde", "👩‍🍳 Cozinha", "🧹 Zeladoria", "🔌 Reparos", "🐾 PetCare"])
    
    # Exemplo de missão para teste
    with tabs[0]:
        v = ("Acompanhante Idoso", 102.0, "Vila Yara")
        st.markdown(f'<div class="card-premium"><h3>{v[0]}</h3><p>📍 {v[2]}</p><div class="valor-liq">R$ {v[1]:.2f}</div></div>', unsafe_allow_html=True)
        st.button("ACEITAR MISSÃO", on_click=aceitar, args=(v[0], v[1], v[2]))

# --- TELA 2: NAVEGAÇÃO ---
elif st.session_state.status == "mapa":
    st.header(f"🧭 Rota: {st.session_state.missao_atual['local']}")
    st.markdown(f'<a href="https://www.google.com/maps/search/{st.session_state.missao_atual["local"]}+Osasco" target="_blank"><button style="background:#FFB300; color:black; width:100%; border-radius:12px; padding:15px; font-weight:bold; border:none; cursor:pointer;">🧭 ABRIR GPS (WAZE/MAPS)</button></a>', unsafe_allow_html=True)
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("✅ CHEGUEI NO LOCAL"):
        st.session_state.status = "selfie_entrada"
        st.rerun()

# --- TELA 3: SELFIE E FOTO DO ANTES ---
elif st.session_state.status == "selfie_entrada":
    st.header("🤳 Início e Registro")
    st.info("Tire uma selfie e a foto do local/item ANTES do serviço.")
    st.camera_input("1. Selfie de Validação")
    st.camera_input("2. Foto do ANTES")
    if st.button("🚀 INICIAR SERVIÇO AGORA"):
        st.session_state.status = "executando"
        st.rerun()

# --- TELA 4: EM ANDAMENTO ---
elif st.session_state.status == "executando":
    st.warning(f"⚠️ EM EXECUÇÃO: {st.session_state.missao_atual['nome']}")
    if st.button("🏁 FINALIZAR TRABALHO"):
        st.session_state.status = "foto_depois"
        st.rerun()

# --- TELA 5: FOTO DO DEPOIS E CONCLUIR ---
elif st.session_state.status == "foto_depois":
    st.header("📸 Comprovação Final")
    st.info("Tire a foto do serviço CONCLUÍDO (Depois).")
    st.camera_input("Foto do DEPOIS")
    if st.button("💎 ENVIAR E RECEBER"):
        st.session_state.saldo += st.session_state.missao_atual['valor']
        st.session_state.status = "sucesso"
        st.rerun()

# --- TELA 6: SUCESSO ---
elif st.session_state.status == "sucesso":
    st.balloons()
    st.success(f"Excelente! R$ {st.session_state.missao_atual['valor']:.2f} creditados.")
    if st.button("VOLTAR AO MURAL"):
        st.session_state.status = "menu"; st.rerun()
        
