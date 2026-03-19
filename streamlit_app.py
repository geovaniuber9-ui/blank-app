import streamlit as st

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="GS Consultoria - Radar", page_icon="🌱", layout="wide")

# ESTILO VISUAL (Verde Claro e Cards)
st.markdown("""
    <style>
    .stApp { background-color: #F0F9F1 !important; }
    .card { 
        background: white; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #2E7D32; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px; 
    }
    .valor { color: #2E7D32; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DO BANCO DE DADOS (SESSÃO)
if 'missoes_ativas' not in st.session_state:
    # Algumas missões iniciais para não vir vazio
    st.session_state.missoes_ativas = [
        {"empresa": "Prefeitura", "categoria": "Zeladoria", "servico": "Varrição de Vias", "local": "Centro", "valor": 55.0},
        {"empresa": "GS Consultoria", "categoria": "Zeladoria", "servico": "Pintura de Meio-Fio", "local": "Bela Vista", "valor": 85.0}
    ]
if 'logado' not in st.session_state: st.session_state.logado = False

# --- LOGIN ---
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
    st.write(f"👤 **Geovani Santi**")
    modo = st.radio("MODO:", ["🚀 Prestador", "🏢 Empresa"])
    if st.button("SAIR"):
        st.session_state.logado = False
        st.rerun()

# --- MODO EMPRESA (ONDE LANÇA A MISSÃO) ---
if modo == "🏢 Empresa":
    st.title("🏢 Gestão de Contratação")
    
    with st.form("nova_os"):
        st.subheader("📝 Abrir Nova O.S.")
        emp = st.text_input("Nome da sua Empresa", value="GS Consultoria")
        cat = st.selectbox("Categoria", ["Zeladoria", "Saúde", "Resíduos", "Jardinagem"])
        serv = st.text_input("Serviço Específico (ex: Varrição)")
        loc = st.text_input("Localização (Bairro)")
        val = st.number_input("Valor (R$)", min_value=10.0)
        
        if st.form_submit_button("LANÇAR NO RADAR"):
            if serv and loc:
                # ADICIONA NA LISTA GLOBAL
                nova_missao = {"empresa": emp, "categoria": cat, "servico": serv, "local": loc, "valor": val}
                st.session_state.missoes_ativas.append(nova_missao)
                st.success(f"Missão de {serv} lançada em {cat}!")
            else:
                st.error("Preencha o serviço e o local!")

# --- MODO PRESTADOR (ONDE APARECE A MISSÃO) ---
else:
    st.title("🌱 Radar GS - Osasco")
    
    # Criamos as abas
    categorias = ["Zeladoria", "Saúde", "Resíduos", "Jardinagem"]
    tabs = st.tabs([f"🧹 Zeladoria", "🏥 Saúde", "♻️ Resíduos", "🌳 Jardinagem"])

    for i, cat_nome in enumerate(categorias):
        with tabs[i]:
            # Filtra as missões que pertencem a esta categoria
            missoes_da_aba = [m for m in st.session_state.missoes_ativas if m['categoria'] == cat_nome]
            
            if not missoes_da_aba:
                st.info(f"Nenhuma missão de {cat_nome} disponível no momento.")
            else:
                for idx, m in enumerate(missoes_da_aba):
                    st.markdown(f"""
                        <div class="card">
                            <small>{m['empresa']} chamando...</small>
                            <h3>{m['servico']}</h3>
                            <p>📍 Local: {m['local']}</p>
                            <div class="valor">R$ {m['valor']:.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"ACEITAR: {m['servico']} #{idx}", key=f"btn_{cat_nome}_{idx}"):
                        st.success(f"Você aceitou: {m['servico']}!")
                        # Opcional: remover da lista após aceitar
                        # st.session_state.missoes_ativas.remove(m)
                
