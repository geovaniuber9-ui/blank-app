import streamlit as st
import time

# CONFIGURAÇÃO VISUAL GS CONSULTORIA
st.set_page_config(page_title="LuzSocial - Uber da Cidadania", page_icon="⚡", layout="centered")

# ESTILO CSS PARA DEIXAR COM CARA DE APLICATIVO PROFISSIONAL
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { border-radius: 20px; height: 3.5em; font-weight: bold; width: 100%; border: none; }
    .btn-gov { background-color: #1A237E; color: white; text-align: center; padding: 15px; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 15px; border: 1px solid #cfd8dc; }
    .card-missao { background-color: white; padding: 25px; border-radius: 20px; border-left: 10px solid #00E676; margin-bottom: 20px; box-shadow: 0px 4px 15px rgba(0,0,0,0.1); color: #333; }
    .status-badge { background-color: #e8f5e9; color: #2e7d32; padding: 5px 15px; border-radius: 50px; font-size: 14px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# GERENCIAMENTO DE ESTADO DO APP
if 'status' not in st.session_state: st.session_state.status = "login"
if 'saldo' not in st.session_state: st.session_state.saldo = 0.0

# --- TELA DE LOGIN ---
if st.session_state.status == "login":
    st.image("https://via.placeholder.com/150x50.png?text=GS+CONSULTORIA", width=180)
    st.title("⚡ LuzSocial")
    st.subheader("Trabalho, Dignidade e Pagamento Instantâneo")
    
    user = st.text_input("CPF ou Usuário")
    senha = st.text_input("Senha", type="password")
    
    if st.button("ENTRAR NO SISTEMA"):
        if user and senha:
            st.session_state.status = "menu"
            st.rerun()
        else:
            st.error("Por favor, preencha os campos.")
            
    st.markdown('<div class="btn-gov">🏛️ ENTRAR COM GOV.BR</div>', unsafe_allow_html=True)

# --- MENU DE MISSÕES (ESTILO UBER) ---
elif st.session_state.status == "menu":
    st.sidebar.title("Olá, Geovani!")
    st.sidebar.metric("Sua Carteira", f"R$ {st.session_state.saldo:.2f}")
    
    st.header("📍 Mural de Missões")
    st.write("Escolha uma atividade próxima para começar:")
    
    # CARD DA MISSÃO 1
    st.markdown("""
        <div class="card-missao">
            <span class="status-badge">DISPONÍVEL</span>
            <h3>Varrer Praça da Matriz</h3>
            <p><b>📍 Local:</b> Centro, Osasco</p>
            <p><b>📦 Ponto de Apoio:</b> Base GS - Rua 15 (Retirar Vassoura/Pá)</p>
            <h2 style="color: #00E676; margin-top: 10px;">R$ 25,00</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("ACEITAR MISSÃO: PRAÇA DA MATRIZ"):
        st.session_state.status = "executando"
        st.rerun()

    if st.sidebar.button("Sair"):
        st.session_state.status = "login"
        st.rerun()

# --- EXECUÇÃO DA MISSÃO ---
elif st.session_state.status == "executando":
    st.header("🚀 Missão em Andamento")
    st.info("Passo 1: Dirija-se à Base GS para retirar o equipamento e bater o ponto.")
    
    st.divider()
    
    st.subheader("Finalização do Serviço")
    st.write("Tire uma foto do local limpo para validar o pagamento:")
    st.camera_input("Foto de comprovação")
    
    st.warning("⚠️ O pagamento será liberado após a devolução do material na Base.")
    
    if st.button("FINALIZAR E DEVOLVER MATERIAL"):
        st.session_state.status = "processando_pix"
        st.rerun()

# --- LIQUIDAÇÃO INSTANTÂNEA ---
elif st.session_state.status == "processando_pix":
    st.header("🔄 Processando Pagamento...")
    st.write("Verificando devolução de equipamento e fotos...")
    
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.02)
        progress_bar.progress(percent_complete + 1)
        
    st.session_state.saldo += 25.0
    st.session_state.status = "pago"
    st.rerun()

elif st.session_state.status == "pago":
    st.balloons()
    st.success("✅ SUCESSO! O valor foi enviado para sua carteira (LuzCoin/Caixa Tem).")
    st.write(f"### Seu novo saldo: R$ {st.session_state.saldo:.2f}")
    
    if st.button("BUSCAR NOVA MISSÃO"):
        st.session_state.status = "menu"
        st.rerun()
        
