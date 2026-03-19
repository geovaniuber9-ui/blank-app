import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="GS Consultoria - O.S. & Avaliação", page_icon="⭐", layout="wide")

# ESTILO VISUAL ECO-BUSINESS
st.markdown("""
    <style>
    .stApp { background-color: #E8F5E9 !important; }
    .card { background: white; padding: 15px; border-radius: 12px; border: 2px solid #2E7D32; margin-bottom: 10px; }
    .status-concluido { color: #2E7D32; font-weight: bold; }
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

# --- MODO EMPRESA (CONTRATANTE) ---
if modo == "🏢 Empresa":
    st.title("🏢 Gestão de Contratação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Abrir Nova O.S.")
        with st.form("nova_os"):
            nome_empresa = st.text_input("Nome da sua Empresa", value="GS Consultoria")
            servico = st.selectbox("Serviço", ["Zeladoria", "Saúde", "Logística", "Jardinagem"])
            cliente_final = st.text_input("Quem vai receber? (Cliente)")
            valor = st.number_input("Valor (R$)", min_value=10.0)
            if st.form_submit_button("LANÇAR NO RADAR"):
                # Simula o lançamento
                st.success("Missão lançada!")

    with col2:
        st.subheader("📊 Histórico e Avaliação")
        if not st.session_state.historico:
            st.info("Nenhuma missão concluída para avaliar ainda.")
        else:
            for i, os in enumerate(st.session_state.historico):
                with st.container():
                    st.markdown(f"""
                        <div class="card">
                            <span class="status-concluido">✅ CONCLUÍDO</span><br>
                            <b>Serviço:</b> {os['servico']}<br>
                            <b>Prestador:</b> {os['prestador']}<br>
                            <b>Cliente:</b> {os['cliente']}
                        </div>
                    """, unsafe_allow_html=True)
                    # Sistema de Estrelas
                    nota = st.select_slider(f"Avalie o prestador {os['prestador']}:", 
                                          options=[1, 2, 3, 4, 5], key=f"nota_{i}")
                    st.write("⭐" * nota)

# --- MODO PRESTADOR (GEOVANI) ---
else:
    st.title("🚀 Radar de Missões")
    
    # Exemplo de Missão Disponível
    st.markdown("""
        <div class="card">
            <small>EMPRESA CHAMANDO: <b>Prefeitura de Osasco</b></small>
            <h3>Pintura de Meio-Fio</h3>
            <p>📍 Local: Bela Vista | 👤 Receber de: <b>Fiscal Adauto</b></p>
            <h2 style="color: green;">R$ 85,00</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("FINALIZAR ESTA MISSÃO AGORA"):
        # Quando o Geovani finaliza, os dados vão para o histórico da empresa
        nova_concluida = {
            "servico": "Pintura de Meio-Fio",
            "empresa": "Prefeitura de Osasco",
            "prestador": "Geovani Santi",
            "cliente": "Fiscal Adauto",
            "valor": 85.0
        }
        st.session_state.historico.append(nova_concluida)
        st.balloons()
        st.success("Missão enviada para avaliação da empresa!")
        
