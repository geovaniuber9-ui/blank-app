import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DE PÁGINA (Sempre no topo)
st.set_page_config(page_title="GS LuzSocial v17.0", page_icon="⚡", layout="wide")

# 2. ESTILO DARK MODE FORÇADO (Para evitar o fundo branco das fotos)
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E0E0E0; }
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
    .stCameraInput { border: 2px solid #00D4FF; border-radius: 15px; padding: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. INICIALIZAÇÃO DE ESTADOS
for key, val in [('logado', False), ('saldo', 0.0), ('status', 'menu'), ('missao_atual', None)]:
    if key not in st.session_state: st.session_state[key] = val

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

# --- FLUXO PRINCIPAL ---
if st.session_state.status == "menu":
    st.title("📍 Mural de Missões")
    tabs = st.tabs(["🩺 Saúde", "👩‍🍳 Cozinha", "🧹 Zeladoria", "🔌 Reparos"])
    
    with tabs[0]:
        v = ("Acompanhante Idoso", 102.0, "Vila Yara")
        st.markdown(f'<div class="card-premium"><h3>{v[0]}</h3><p>📍 {v[2]}</p><div class="valor-liq">R$ {v[1]:.2f}</div></div>', unsafe_allow_html=True)
        st.button("ACEITAR MISSÃO", key="btn_acc_1", on_click=aceitar, args=(v[0], v[1], v[2]))

elif st.session_state.status == "mapa":
    st.header(f"🧭 Destino: {st.session_state.missao_atual['local']}")
    # Botão de GPS corrigido
    st.markdown(f'<a href="https://www.google.com/maps/search/{st.session_state.missao_atual["local"]}+Osasco" target="_blank"><button style="background:#FFB300; color:black; width:100%; border-radius:12px; padding:15px; font-weight:bold; border:none; cursor:pointer;">🧭 ABRIR GOOGLE MAPS</button></a>', unsafe_allow_html=True)
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("✅ CHEGUEI NO LOCAL"):
        st.session_state.status = "registro_inicio"
        st.rerun()

elif st.session_state.status == "registro_inicio":
    st.header("📸 Registro de Entrada")
    st.info("Obrigatório: Selfie + Foto do local ANTES do serviço.")
    selfie = st.camera_input("1. Sua Selfie")
    foto_antes = st.camera_input("2. Foto do ANTES")
    
    if selfie and foto_antes:
        if st.button("🚀 INICIAR TRABALHO"):
            st.session_state.status = "executando"
            st.rerun()

elif st.session_state.status == "executando":
    st.warning(f"⚠️ TRABALHO EM ANDAMENTO: {st.session_state.missao_atual['nome']}")
    st.markdown("Execute o serviço com capricho. Ao terminar, clique abaixo.")
    if st.button("🏁 FINALIZAR TRABALHO"):
        st.session_state.status = "registro_fim"
        st.rerun()

elif st.session_state.status == "registro_fim":
    st.header("📸 Comprovação de Saída")
    st.success("Trabalho concluído! Agora registre o DEPOIS.")
    foto_depois = st.camera_input("Foto do DEPOIS")
    
    if foto_depois:
        if st.button("💎 ENVIAR E RECEBER PAGAMENTO"):
            st.session_state.saldo += st.session_state.missao_atual['valor']
            st.session_state.status = "concluido"
            st.rerun()

elif st.session_state.status == "concluido":
    st.balloons()
    st.success(f"Excelente! Pagamento de R$ {st.session_state.missao_atual['valor']:.2f} creditado!")
    if st.button("VOLTAR AO DASHBOARD"):
        st.session_state.status = "menu"; st.rerun()
        
