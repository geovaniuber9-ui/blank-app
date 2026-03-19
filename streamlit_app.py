import streamlit as st
import time

# 1. CONFIGURAÇÃO E ESTILO
st.set_page_config(page_title="GS Radar Pro", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F7F9FB !important; }
    .wallet-box {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    .status-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border-left: 6px solid #2E7D32; margin-bottom: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    }
    .verified-badge {
        color: #1E88E5; font-weight: bold; font-size: 12px;
        background: #E3F2FD; padding: 3px 8px; border-radius: 10px;
    }
    .stars { color: #FFB300; font-weight: bold; }
    .price-tag { color: #2E7D32; font-size: 26px; font-weight: bold; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'saldo' not in st.session_state:
    st.session_state.saldo = 0.00  
if 'missoes' not in st.session_state:
    st.session_state.missoes = []

# --- 3. LOGIN ---
if not st.session_state.logado:
    st.title("GS Consultoria 🌱")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("ENTRAR NO SISTEMA", use_container_width=True):
        if user == "1" and password == "1":
            st.session_state.logado = True
            st.rerun()
    st.stop()

# --- 4. BARRA LATERAL ---
with st.sidebar:
    st.markdown(f'<div class="wallet-box"><small>SALDO GS</small><br><span style="font-size: 28px;">R$ {st.session_state.saldo:.2f}</span></div>', unsafe_allow_html=True)
    
    modo = st.radio("Navegação:", ["🚀 Radar de Serviços", "🏢 Painel da Empresa"])
    
    st.divider()
    if st.button("Sair"):
        st.session_state.logado = False
        st.rerun()

# --- 5. MODO RADAR (VISUAL DO PRESTADOR) ---
if modo == "🚀 Radar de Serviços":
    st.title("🚀 Radar GS - Osasco")
    
    # Exemplo de Perfil do Prestador logado
    st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #ddd;">
            <b>Prestador:</b> Antônio Silva <br>
            <span class="stars">⭐ 4.9</span> | 🏃 <b>32 Missões concluídas</b>
        </div>
    """, unsafe_allow_html=True)

    categorias = ["🧹 Zeladoria", "🚰 Encanador", "🔨 Marcenaria", "🛠️ Montador", "💅 Beleza", "🏠 Diarista", "🏥 Saúde", "🌳 Jardinagem"]
    tabs = st.tabs(categorias)
    
    for i, tab in enumerate(tabs):
        with tab:
            nome_cat = categorias[i].split(" ")[1]
            servicos_filtro = [m for m in st.session_state.missoes if m['cat'] == nome_cat]
            
            if not servicos_filtro:
                st.info(f"Sem chamados para {nome_cat}.")
            else:
                for idx, m in enumerate(servicos_filtro):
                    # Lógica do Selo de Verificado
                    selo_html = '<span class="verified-badge">✅ CONTA VERIFICADA</span>' if m['cpf'] else ''
                    
                    st.markdown(f"""
                    <div class="status-card">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="font-size: 13px; color: #555;"><b>Empresa:</b> {m['empresa']}</span>
                            {selo_html}
                        </div>
                        <div style="font-size: 13px; color: #777;">👤 Resp: {m['nome_resp']}</div>
                        <hr style="margin: 10px 0; border: 0; border-top: 1px solid #eee;">
                        <h2 style="margin:0;">{m['serv']}</h2>
                        <p style="color:#666; margin: 5px 0;">📍 {m['loc']}</p>
                        <div class="price-tag">R$ {m['val']:.2f}</div>
                        <p><small>Pagamento: <b>{m['pag']}</b> | Obs: {m['obs']}</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("✅ ACEITAR MISSÃO", key=f"ac_{nome_cat}_{idx}", use_container_width=True):
                        st.success("Missão aceita! Inicie o trajeto.")

# --- 6. PAINEL DA EMPRESA (CADASTRO) ---
else:
    st.title("🏢 Painel de Gestão")
    
    with st.form("form_os"):
        st.subheader("Identificação do Solicitante")
        col1, col2 = st.columns(2)
        with col1:
            empresa_nome = st.text_input("Nome da Empresa", value="GS Consultoria")
            nome_usuario = st.text_input("Seu Nome")
        with col2:
            cpf_usuario = st.text_input("CPF (Para selo de verificado)")
            cat_selecionada = st.selectbox("Categoria", ["Zeladoria", "Encanador", "Marcenaria", "Montador", "Beleza", "Diarista", "Saúde", "Jardinagem"])
        
        st.divider()
        st.subheader("Dados do Serviço")
        servico_txt = st.text_input("Descrição do Serviço")
        bairro_txt = st.text_input("Bairro / Ponto de Referência")
        
        c_v, c_p = st.columns(2)
        with c_v: valor_serv = st.number_input("Valor (R$)", min_value=1.0, value=60.0)
        with c_p: pag_tipo = st.selectbox("Pagamento", ["Pix", "Máquina", "Dinheiro"])
            
        obs_txt = st.text_area("Observações")
        
        taxa = valor_serv * 0.07
        st.warning(f"Custo para chamar (7%): **R$ {taxa:.2f}**")
        
        if st.form_submit_button("🚀 LANÇAR NO RADAR"):
            if not (nome_usuario and servico_txt):
                st.error("Preencha ao menos seu nome e o serviço!")
            elif st.session_state.saldo < taxa:
                st.error(f"Saldo insuficiente! Recarregue R$ {taxa:.2f}")
            else:
                st.session_state.saldo -= taxa
                st.session_state.missoes.append({
                    "empresa": empresa_nome, "nome_resp": nome_usuario, "cpf": cpf_usuario,
                    "cat": cat_selecionada, "serv": servico_txt, "loc": bairro_txt, 
                    "val": valor_serv, "pag": pag_tipo, "obs": obs_txt
                })
                st.success("Publicado!")
                time.sleep(1)
                st.rerun()
    
