import streamlit as st
import time

# 1. CONFIGURAÇÃO E ESTILO
st.set_page_config(page_title="GS Radar Pro", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F7F9FB !important; }
    .sidebar-info { background: #1B5E20; color: white; padding: 20px; border-radius: 15px; text-align: center; }
    .login-box { background: white; padding: 30px; border-radius: 15px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DO SISTEMA
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'saldo' not in st.session_state:
    st.session_state.saldo = 10.00
if 'missoes' not in st.session_state:
    st.session_state.missoes = []

# --- 3. TELA DE LOGIN (A PORTARIA) ---
if not st.session_state.logado:
    st.title("GS Consultoria 🌱")
    with st.container():
        st.subheader("Acesso Restrito")
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        
        if st.button("ENTRAR NO SISTEMA", use_container_width=True):
            if user == "1" and password == "1":
                st.session_state.logado = True
                st.success("Acesso liberado!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos!")
    st.stop() # PARA O CÓDIGO AQUI SE NÃO ESTIVER LOGADO

# --- 4. SE CHEGOU AQUI, ESTÁ LOGADO (CONTEÚDO DO APP) ---

with st.sidebar:
    st.markdown(f'<div class="sidebar-info"><small>SALDO ATUAL</small><br><span style="font-size: 25px;">R$ {st.session_state.saldo:.2f}</span></div>', unsafe_allow_html=True)
    
    st.divider()
    modo = st.radio("Selecione o Módulo:", ["🚀 Radar de Pedidos", "🏢 Lançar Serviço"])
    
    if st.button("SAIR / LOGOUT"):
        st.session_state.logado = False
        st.rerun()

# --- MODO PRESTADOR ---
if modo == "🚀 Radar de Pedidos":
    st.title("📲 Radar GS - Osasco")
    if not st.session_state.missoes:
        st.info("Nenhum pedido no radar no momento.")
    else:
        for m in st.session_state.missoes:
            st.write(f"**{m['job']}** - {m['loc']} (R$ {m['val']})")
            if st.button(f"Aceitar #{m['id']}", key=f"ac_{m['id']}"):
                st.success("Missão aceita!")

# --- MODO EMPRESA (COM BOTÃO DE SUBMIT) ---
else:
    st.title("🏢 Painel de Gestão")
    with st.form("form_novo"):
        st.write("### Abrir Nova O.S.")
        job = st.text_input("Serviço")
        loc = st.text_input("Bairro")
        val = st.number_input("Valor", min_value=1.0)
        
        # O botão obrigatório do formulário
        enviar = st.form_submit_button("LANÇAR NO RADAR")
        
        if enviar:
            if job and loc:
                st.session_state.missoes.append({
                    "id": int(time.time()), "job": job, "loc": loc, "val": val
                })
                st.success("Lançado com sucesso!")
                time.sleep(1)
                st.rerun()
                
