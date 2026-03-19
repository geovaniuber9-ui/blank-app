import streamlit as st
import time

# 1. CONFIGURAÇÃO E ESTILO (VERDE CLARO E DESIGN LIMPO)
st.set_page_config(page_title="GS Radar Pro", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    /* Fundo Verde Claro Suave */
    .stApp { 
        background-color: #E8F5E9 !important; 
    }
    
    .wallet-box {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    
    .profile-box {
        background: white; padding: 15px; border-radius: 15px;
        border: 1px solid #C8E6C9; margin-bottom: 20px;
    }
    
    .status-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border-left: 6px solid #2E7D32; margin-bottom: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    }
    
    .verified-badge {
        color: #1E88E5; font-weight: bold; font-size: 11px;
        background: #E3F2FD; padding: 4px 8px; border-radius: 10px;
    }
    
    .stars { color: #FFB300; font-weight: bold; }
    .price-tag { color: #2E7D32; font-size: 26px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DE DADOS (SIMULANDO UM PERFIL LOGADO)
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 50.00  
if 'missoes' not in st.session_state: st.session_state.missoes = []
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "nome": "Antônio Silva",
        "cpf": "123.***.***-00",
        "estrelas": 4.9,
        "corridas": 32
    }

# --- 3. LOGIN ---
if not st.session_state.logado:
    st.title("GS Consultoria 🌱")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("ACESSAR SISTEMA", use_container_width=True):
        if user == "1" and password == "1":
            st.session_state.logado = True
            st.rerun()
    st.stop()

# --- 4. BARRA LATERAL (MENU E PERFIL) ---
with st.sidebar:
    # Foto e Perfil na Barra Lateral
    st.markdown(f"""
        <div class="profile-box">
            <small style="color: #666;">BEM-VINDO,</small><br>
            <b>{st.session_state.user_data['nome']}</b><br>
            <span class="stars">⭐ {st.session_state.user_data['estrelas']}</span> | 
            <small>🏃 {st.session_state.user_data['corridas']} serviços</small>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="wallet-box"><small>SALDO GS</small><br><span style="font-size: 28px;">R$ {st.session_state.saldo:.2f}</span></div>', unsafe_allow_html=True)
    
    modo = st.radio("Selecione o Painel:", ["🚀 Radar de Serviços", "🏢 Painel da Empresa"])
    
    st.divider()
    if st.button("Sair da Conta"):
        st.session_state.logado = False
        st.rerun()

# --- 5. MODO RADAR (O QUE O PRESTADOR VÊ) ---
if modo == "🚀 Radar de Serviços":
    st.title("📲 Radar GS - Osasco")
    
    categorias = ["🧹 Zeladoria", "🚰 Encanador", "🔨 Marcenaria", "🛠️ Montador", "💅 Beleza", "🏠 Diarista", "🏥 Saúde", "🌳 Jardinagem"]
    tabs = st.tabs(categorias)
    
    for i, tab in enumerate(tabs):
        with tab:
            nome_cat = categorias[i].split(" ")[1]
            servicos_filtro = [m for m in st.session_state.missoes if m['cat'] == nome_cat]
            
            if not servicos_filtro:
                st.info(f"Nenhum pedido de {nome_cat} aguardando...")
            else:
                for idx, m in enumerate(servicos_filtro):
                    selo = '<span class="verified-badge">✅ CONTA VERIFICADA</span>' if m['cpf'] else ''
                    st.markdown(f"""
                    <div class="status-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 13px; color: #555;"><b>Empresa:</b> {m['empresa']}</span>
                            {selo}
                        </div>
                        <div style="font-size: 12px; color: #888;">👤 Responsável: {m['nome_resp']}</div>
                        <hr style="margin: 10px 0; border: 0; border-top: 1px solid #eee;">
                        <h2 style="margin:0; font-size: 22px;">{m['serv']}</h2>
                        <p style="color:#444; margin: 5px 0;">📍 {m['loc']}</p>
                        <div class="price-tag">R$ {m['val']:.2f}</div>
                        <p style="margin-top:10px;"><small>💳 {m['pag']} | 📝 {m['obs']}</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("✅ ACEITAR E CHAMAR CORRIDA", key=f"ac_{nome_cat}_{idx}", use_container_width=True):
                        st.success("Missão aceita! O cliente foi notificado.")

# --- 6. PAINEL DA EMPRESA ---
else:
    st.title("🏢 Gestão de Chamados")
    
    with st.form("form_os"):
        st.subheader("Informações da Empresa")
        c1, c2 = st.columns(2)
        with c1:
            empresa_nome = st.text_input("Nome da Empresa", value="GS Consultoria")
            nome_usuario = st.text_input("Seu Nome")
        with c2:
            cpf_usuario = st.text_input("CPF (Para Verificação)")
            cat_selecionada = st.selectbox("Tipo de Serviço", ["Zeladoria", "Encanador", "Marcenaria", "Montador", "Beleza", "Diarista", "Saúde", "Jardinagem"])
        
        st.divider()
        st.subheader("Detalhes da Solicitação")
        servico_txt = st.text_input("Descrição do que precisa")
        bairro_txt = st.text_input("Endereço / Bairro")
        
        cv, cp = st.columns(2)
        with cv: valor_serv = st.number_input("Valor ao Prestador (R$)", min_value=1.0, value=70.0)
        with cp: pag_tipo = st.selectbox("Meio de Pagamento", ["Pix", "Máquina", "Dinheiro"])
            
        obs_txt = st.text_area("Observações importantes")
        
        taxa = valor_serv * 0.07
        st.warning(f"Será descontado **R$ {taxa:.2f}** (7%) do seu saldo para publicar.")
        
        if st.form_submit_button("🚀 PUBLICAR NO RADAR"):
            if not (nome_usuario and servico_txt):
                st.error("Campos obrigatórios faltando!")
            elif st.session_state.saldo < taxa:
                st.error("Saldo insuficiente para cobrir a taxa de 7%.")
            else:
                st.session_state.saldo -= taxa
                st.session_state.missoes.append({
                    "empresa": empresa_nome, "nome_resp": nome_usuario, "cpf": cpf_usuario,
                    "cat": cat_selecionada, "serv": servico_txt, "loc": bairro_txt, 
                    "val": valor_serv, "pag": pag_tipo, "obs": obs_txt
                })
                st.balloons()
                st.success("Chamado enviado para o Radar!")
                time.sleep(1)
                st.rerun()
                
