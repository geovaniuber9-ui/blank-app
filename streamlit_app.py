import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS LuzSocial v15.0", page_icon="⚡", layout="wide")

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

# --- SIDEBAR ---
if st.session_state.logado:
    with st.sidebar:
        st.markdown(f"### 👤 Geovani Santi\n## 💰 R$ {st.session_state.saldo:.2f}")
        st.divider()
        if st.button("🚪 Sair"): 
            st.session_state.logado = False
            st.rerun()

# --- LOGIN ---
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center; color: #00D4FF;'>⚡ GS CONSULTORIA</h1>", unsafe_allow_html=True)
    if st.button("ACESSAR DASHBOARD"):
        st.session_state.logado = True; st.rerun()
    st.stop()

# --- TELA 1: MURAL DE OPORTUNIDADES ---
if st.session_state.status == "menu":
    st.title("📍 Radar de Missões")
    tabs = st.tabs(["🩺 Saúde", "👩‍🍳 Cozinha", "🧹 Zeladoria", "🔌 Reparos", "🐾 PetCare"])

    missoes_data = {
        "Saúde": [("Acompanhante Idoso", 102.0, "Vila Yara"), ("Cuidador Noturno", 210.0, "Centro")],
        "Cozinha": [("Preparo de Marmitas", 150.0, "Bela Vista"), ("Ajudante de Cozinha", 85.0, "Km 18")],
        "Zeladoria": [("Limpeza de Bueiro", 63.75, "Rochdale"), ("Jardinagem Completa", 85.0, "IAPI")],
        "Reparos": [("Manutenção Elétrica", 120.0, "Poli Osasco"), ("Pequenos Reparos", 55.0, "Saúde")],
        "PetCare": [("Dog Walker", 45.0, "Campesina"), ("Banho em Domicílio", 75.0, "Vila Yara")]
    }

    for i, (nome_tab, lista) in enumerate(zip(tabs, missoes_data.values())):
        with nome_tab:
            for m in lista:
                st.markdown(f'<div class="card-premium"><h3>{m[0]}</h3><p>📍 {m[2]}</p><div class="valor-liq">R$ {m[1]:.2f}</div></div>', unsafe_allow_html=True)
                st.button(f"ACEITAR: {m[0]}", key=f"btn_{m[0]}", on_click=aceitar, args=(m[0], m[1], m[2]))

# --- TELA 2: NAVEGAÇÃO GPS ---
elif st.session_state.status == "mapa":
    st.header(f"📍 Rota para {st.session_state.missao_atual['local']}")
    st.info(f"Serviço: {st.session_state.missao_atual['nome']}")
    
    # Simulação de Link para Maps
    st.markdown(f"""
        <a href="https://www.google.com/maps/search/{st.session_state.missao_atual['local']}+Osasco" target="_blank">
            <button style="background:#FFB300; color:black; width:100%; border-radius:12px; padding:15px; font-weight:bold; border:none; margin-bottom:10px;">
                🧭 ABRIR NO GOOGLE MAPS / WAZE
            </button>
        </a>
    """, unsafe_allow_html=True)
    
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("✅ CHEGUEI AO LOCAL"):
        st.session_state.status = "iniciar"
        st.rerun()

# --- TELA 3: INICIAR SERVIÇO ---
elif st.session_state.status == "iniciar":
    st.header("🤳 Início do Serviço")
    st.info("Tire uma selfie no local para validar sua chegada.")
    st.camera_input("Selfie de Validação")
    if st.button("🚀 INICIAR TRABALHO"):
        st.session_state.status = "executando"
        st.rerun()

# --- TELA 4: EXECUTANDO ---
elif st.session_state.status == "executando":
    st.warning(f"⚠️ TRABALHO EM ANDAMENTO: {st.session_state.missao_atual['nome']}")
    st.markdown("Execute o serviço com excelência conforme os padrões GS.")
    if st.button("🏁 CONCLUIR SERVIÇO"):
        st.session_state.status = "finalizar"
        st.rerun()

# --- TELA 5: FINALIZAR E RECEBER ---
elif st.session_state.status == "finalizar":
    st.header("📸 Comprovação de Entrega")
    st.camera_input("Foto do Serviço Concluído")
    if st.button("💎 FINALIZAR E RECEBER PAGAMENTO"):
        st.session_state.saldo += st.session_state.missao_atual['valor']
        st.session_state.status = "sucesso"
        st.rerun()

elif st.session_state.status == "sucesso":
    st.balloons()
    st.success(f"Pagamento de R$ {st.session_state.missao_atual['valor']:.2f} confirmado!")
    if st.button("VOLTAR AO INÍCIO"):
        st.session_state.status = "menu"; st.rerun()
    
