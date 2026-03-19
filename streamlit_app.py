import streamlit as st
import time

# 1. CONFIGURAÇÃO E ESTILO
st.set_page_config(page_title="GS Radar Pro", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F7F9FB !important; }
    .status-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #2E7D32;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .price-tag { color: #2E7D32; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO
if 'logado' not in st.session_state:
    st.session_state.logado = False
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

# --- 4. NAVEGAÇÃO ---
with st.sidebar:
    st.header("Menu")
    modo = st.radio("Navegar para:", ["🚀 Radar de Missões", "🏢 Painel da Empresa"])
    if st.button("Sair"):
        st.session_state.logado = False
        st.rerun()

# --- MODO PRESTADOR (RADAR) ---
if modo == "🚀 Radar de Missões":
    st.title("🚀 Radar GS - Osasco")
    
    # Abas de Categorias como na foto
    tab1, tab2, tab3, tab4 = st.tabs(["🧹 Zeladoria", "🏥 Saúde", "♻️ Resíduos", "🌳 Jardinagem"])
    
    with tab1:
        if not st.session_state.missoes:
            st.info("Nenhum pedido no radar no momento.")
        else:
            for i, m in enumerate(st.session_state.missoes):
                with st.container():
                    st.markdown(f"""
                    <div class="status-card">
                        <small>Contratante: {m['empresa']}</small>
                        <h2>{m['job']}</h2>
                        <p>📍 {m['loc']}</p>
                        <p class="price-tag">R$ {m['val']:.2f}</p>
                        <small>Pagamento: {m['pagamento']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.button("🗺️ Ver no Mapa", key=f"map_{i}")
                    with col2:
                        st.file_uploader("📸 Foto da Conclusão", key=f"file_{i}")
                    
                    if st.button("✅ Finalizar Missão", key=f"fin_{i}", use_container_width=True):
                        st.success("Missão concluída com sucesso!")
                        # Aqui você poderia remover da lista após finalizar

# --- MODO EMPRESA (CADASTRO) ---
else:
    st.title("🏢 Painel de Gestão")
    st.subheader("Abrir Nova O.S.")
    
    with st.expander("Preencha os dados do serviço", expanded=True):
        empresa = st.text_input("Sua Empresa", value="GS Consultoria")
        categoria = st.selectbox("Categoria", ["Zeladoria", "Saúde", "Resíduos", "Jardinagem"])
        servico = st.text_input("O que fazer? (Serviço)", placeholder="Ex: Varrer praça")
        local = st.text_input("Onde? (Bairro/Rua)", placeholder="Ex: Rio Pequeno")
        
        col_v, col_p = st.columns(2)
        with col_v:
            valor = st.number_input("Valor do Pagamento (R$)", min_value=1.0, value=60.0)
        with col_p:
            pagamento = st.selectbox("Forma de Pagamento", ["Pix", "Máquina de Cartão", "Dinheiro"])
        
        observacao = st.text_area("Observações Adicionais")

        if st.button("🚀 PUBLICAR NO RADAR", use_container_width=True):
            if servico and local:
                nova_os = {
                    "empresa": empresa,
                    "categoria": categoria,
                    "job": servico,
                    "loc": local,
                    "val": valor,
                    "pagamento": pagamento,
                    "obs": observacao
                }
                st.session_state.missoes.append(nova_os)
                st.balloons()
                st.success("Serviço lançado no Radar!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Por favor, preencha o serviço e o local.")

    # Lista de Missões Atuais para a empresa gerenciar
    st.divider()
    st.subheader("📋 Missões Atuais no Radar")
    for i, m in enumerate(st.session_state.missoes):
        col_desc, col_btn = st.columns([4, 1])
        col_desc.write(f"**[{m['categoria']}]** {m['job']} - {m['loc']} (R$ {m['val']})")
        if col_btn.button("❌ Excluir", key=f"del_{i}"):
            st.session_state.missoes.pop(i)
            st.rerun()
                                         
