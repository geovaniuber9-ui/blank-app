import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="GS Consultoria - Radar", page_icon="🌱", layout="wide")

# ESTILO VISUAL ECO-BUSINESS (Ajustado para o verde claro que você pediu)
st.markdown("""
    <style>
    .stApp { background-color: #F0F9F1 !important; }
    .card { 
        background: white; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #2E7D32; 
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px; 
    }
    .status-concluido { color: #2E7D32; font-weight: bold; }
    .valor { color: #2E7D32; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# CONTROLE DE SESSÃO
if 'logado' not in st.session_state: st.session_state.logado = False
if 'historico' not in st.session_state: st.session_state.historico = []

# LOGIN 1/1
if not st.session_state.logado:
    st.title("GS Consultoria 🌱")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")
    if st.button("ENTRAR"):
        if u == "1" and s == "1":
            st.session_state.logado = True
            st.rerun()
    st.stop()

# SIDEBAR
with st.sidebar:
    st.write(f"👤 **Usuário:** Geovani Santi")
    modo = st.radio("MODO:", ["🚀 Prestador", "🏢 Empresa"])
    if st.button("SAIR"):
        st.session_state.logado = False
        st.rerun()

# --- MODO EMPRESA ---
if modo == "🏢 Empresa":
    st.title("🏢 Gestão de Contratação")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Abrir Nova O.S.")
        with st.form("nova_os"):
            st.text_input("Nome da sua Empresa", value="GS Consultoria")
            st.selectbox("Categoria", ["Zeladoria", "Saúde", "Resíduos", "Jardinagem"])
            st.text_input("Serviço Específico (ex: Varrição)")
            st.number_input("Valor (R$)", min_value=10.0)
            if st.form_submit_button("LANÇAR NO RADAR"):
                st.success("Missão lançada no sistema!")

    with col2:
        st.subheader("📊 Histórico e Avaliação")
        if not st.session_state.historico:
            st.info("Aguardando conclusões...")
        else:
            for i, os in enumerate(st.session_state.historico):
                st.markdown(f'<div class="card">✅ <b>{os["servico"]}</b> - Finalizado</div>', unsafe_allow_html=True)

# --- MODO PRESTADOR (COM O MENU DE CATEGORIAS) ---
else:
    st.title("🌱 Radar GS - Osasco")
    
    # CRIAÇÃO DO MENU (Abas)
    tab1, tab2, tab3, tab4 = st.tabs(["🧹 Zeladoria", "🏥 Saúde", "♻️ Resíduos", "🌳 Jardinagem"])

    with tab1:
        # Missão 1
        st.markdown("""
            <div class="card">
                <p style="color: #666; margin-bottom: 5px;">📍 Centro</p>
                <b style="font-size: 18px;">Varrição de Vias</b>
                <div class="valor">R$ 55,00</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ACEITAR: VARRIÇÃO DE VIAS"):
            st.success("Missão aceita!")

        # Missão 2
        st.markdown("""
            <div class="card">
                <p style="color: #666; margin-bottom: 5px;">📍 Bela Vista</p>
                <b style="font-size: 18px;">Pintura de Meio-Fio</b>
                <div class="valor">R$ 85,00</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ACEITAR: PINTURA DE MEIO-FIO"):
            st.session_state.historico.append({"servico": "Pintura de Meio-Fio", "status": "Concluído"})
            st.balloons()
            st.success("Missão enviada para avaliação!")

        # Missão 3
        st.markdown("""
            <div class="card">
                <p style="color: #666; margin-bottom: 5px;">📍 Rochdale</p>
                <b style="font-size: 18px;">Limpeza de Bueiro</b>
                <div class="valor">R$ 120,00</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("ACEITAR: LIMPEZA DE BUEIRO"):
            st.info("Missão adicionada à sua agenda.")

    with tab2:
        st.info("Nenhuma missão de Saúde disponível no momento.")
    
    with tab3:
        st.info("Nenhuma missão de Resíduos disponível no momento.")
        
    with tab4:
        st.info("Nenhuma missão de Jardinagem disponível no momento.")
        
