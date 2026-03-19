import streamlit as st

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="GS Consultoria - Radar Pro", page_icon="🌱", layout="wide")

# ESTILO VISUAL MELHORADO
st.markdown("""
    <style>
    .stApp { background-color: #F0F9F1 !important; }
    .card { 
        background: white; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #2E7D32; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px; 
    }
    .valor { color: #2E7D32; font-size: 26px; font-weight: bold; }
    .btn-maps { background-color: #4285F4; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS TEMPORÁRIO
if 'missoes_ativas' not in st.session_state:
    st.session_state.missoes_ativas = []
if 'logado' not in st.session_state: st.session_state.logado = False

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
    st.write(f"👤 **Operador:** Geovani Santi")
    modo = st.radio("ESCOLHA O MODO:", ["🚀 Prestador (Executar)", "🏢 Empresa (Gerenciar)"])
    if st.button("SAIR DO SISTEMA"):
        st.session_state.logado = False
        st.rerun()

# --- MODO EMPRESA (GERENCIAR E EXCLUIR) ---
if modo == "🏢 Empresa (Gerenciar)":
    st.title("🏢 Painel de Controle")
    
    with st.expander("➕ LANÇAR NOVA MISSÃO NO RADAR", expanded=True):
        with st.form("nova_os"):
            col_a, col_b = st.columns(2)
            with col_a:
                emp = st.text_input("Sua Empresa", value="GS Consultoria")
                cat = st.selectbox("Categoria", ["Zeladoria", "Saúde", "Resíduos", "Jardinagem"])
            with col_b:
                serv = st.text_input("O que fazer? (Serviço)")
                loc = st.text_input("Onde? (Bairro/Rua)")
            val = st.number_input("Valor do Pagamento (R$)", min_value=1.0)
            
            if st.form_submit_button("PUBLICAR NO RADAR"):
                if serv and loc:
                    st.session_state.missoes_ativas.append({
                        "id": len(st.session_state.missoes_ativas),
                        "empresa": emp, "categoria": cat, "servico": serv, "local": loc, "valor": val
                    })
                    st.success("Missão publicada!")
                    st.rerun()

    st.subheader("📋 Missões Atuais no Radar")
    if not st.session_state.missoes_ativas:
        st.info("Nenhuma missão ativa.")
    else:
        for i, m in enumerate(st.session_state.missoes_ativas):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**[{m['categoria']}]** {m['servico']} - {m['local']} (R$ {m['valor']})")
            with col2:
                if st.button("❌ Excluir", key=f"del_{i}"):
                    st.session_state.missoes_ativas.pop(i)
                    st.rerun()

# --- MODO PRESTADOR (EXECUTAR, MAPS E FOTO) ---
else:
    st.title("🚀 Radar GS - Osasco")
    categorias = ["Zeladoria", "Saúde", "Resíduos", "Jardinagem"]
    tabs = st.tabs([f"🧹 {c}" if c=="Zeladoria" else f"🌳 {c}" if c=="Jardinagem" else c for c in categorias])

    for i, cat_nome in enumerate(categorias):
        with tabs[i]:
            missoes = [m for m in st.session_state.missoes_ativas if m['categoria'] == cat_nome]
            
            if not missoes:
                st.info(f"Sem missões de {cat_nome} agora.")
            else:
                for idx, m in enumerate(missoes):
                    with st.container():
                        st.markdown(f"""
                            <div class="card">
                                <small>Contratante: {m['empresa']}</small>
                                <h3>{m['servico']}</h3>
                                <p>📍 {m['local']}</p>
                                <div class="valor">R$ {m['valor']:.2f}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        c1, c2, c3 = st.columns([1, 1, 1])
                        with c1:
                            # LINK PARA O GOOGLE MAPS
                            url_maps = f"https://www.google.com/maps/search/?api=1&query={m['local']}+Osasco"
                            st.markdown(f'<a href="{url_maps}" target="_blank" class="btn-maps">🗺️ Ver no Mapa</a>', unsafe_allow_html=True)
                        
                        with c2:
                            # CAMPO PARA FOTO
                            st.file_uploader("📸 Foto da Conclusão", type=['png', 'jpg'], key=f"foto_{m['id']}")
                        
                        with c3:
                            if st.button("✅ Finalizar", key=f"fin_{m['id']}"):
                                st.balloons()
                                st.success("Missão Concluída!")
                                
