import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="GS Consultoria - Super Radar", page_icon="🚀", layout="wide")

# ESTILO VISUAL (Verde Natureza + Cards Profissionais)
st.markdown("""
    <style>
    .stApp { background-color: #F0F9F1 !important; }
    .card { 
        background: white; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #2E7D32; box-shadow: 2px 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 15px; 
    }
    .valor { color: #2E7D32; font-size: 28px; font-weight: bold; margin-top: 5px; }
    .btn-maps { 
        background-color: #4285F4; color: white !important; 
        padding: 10px 20px; border-radius: 8px; 
        text-decoration: none; font-weight: bold; display: inline-block;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff; border-radius: 5px; padding: 10px; border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE DADOS (MEMÓRIA DO APP)
if 'missoes_ativas' not in st.session_state:
    st.session_state.missoes_ativas = [
        {"id": 101, "empresa": "GS Consultoria", "categoria": "💅 Beleza", "servico": "Manicure e Pedicure", "local": "Centro", "valor": 60.0},
        {"id": 102, "empresa": "Residencial Bela Vista", "categoria": "🛠️ Reparos", "servico": "Troca de Resistência Chuveiro", "local": "Bela Vista", "valor": 80.0}
    ]
if 'logado' not in st.session_state: st.session_state.logado = False

# 3. LOGIN SIMPLES (1/1)
if not st.session_state.logado:
    st.title("GS Consultoria 🌱")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")
    if st.button("ACESSAR SISTEMA"):
        if u == "1" and s == "1":
            st.session_state.logado = True
            st.rerun()
    st.stop()

# 4. DEFINIÇÃO DAS CATEGORIAS (O CORAÇÃO DO SEU MENU)
categorias_master = [
    "🧹 Zeladoria", "💅 Beleza", "🛠️ Reparos", "🔑 Chaveiro", 
    "🚰 Encanador", "🌳 Jardinagem", "🧼 Limpeza", "📦 Entregas", 
    "🚚 Carretos", "🐶 Pets"
]

# SIDEBAR (MENU LATERAL)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1048/1048953.png", width=100)
    st.write(f"### Bem-vindo, Geovani!")
    modo = st.radio("Selecione sua visão:", ["🚀 Radar do Prestador", "🏢 Gestão da Empresa"])
    st.divider()
    if st.button("DESLOGAR"):
        st.session_state.logado = False
        st.rerun()

# --- MODO EMPRESA (PARA VOCÊ CRIAR E EXCLUIR) ---
if modo == "🏢 Gestão da Empresa":
    st.title("🏢 Gerenciar Novas Missões")
    
    with st.expander("📝 CADASTRAR NOVO SERVIÇO", expanded=True):
        with st.form("form_os"):
            col1, col2 = st.columns(2)
            with col1:
                emp_name = st.text_input("Nome do Cliente/Empresa", value="GS Consultoria")
                cat_sel = st.selectbox("Categoria do Serviço", categorias_master)
                valor_os = st.number_input("Valor a Pagar (R$)", min_value=1.0, step=5.0)
            with col2:
                serv_desc = st.text_input("Descrição (Ex: Corte de Cabelo)")
                bairro_loc = st.text_input("Bairro/Local em Osasco")
            
            if st.form_submit_button("LANÇAR NO RADAR 🚀"):
                if serv_desc and bairro_loc:
                    import time
                    nova_m = {
                        "id": int(time.time()), 
                        "empresa": emp_name, "categoria": cat_sel, 
                        "servico": serv_desc, "local": bairro_loc, "valor": valor_os
                    }
                    st.session_state.missoes_ativas.append(nova_m)
                    st.success("Missão lançada com sucesso!")
                    st.rerun()

    st.subheader("📋 Serviços Ativos no Momento")
    for i, m in enumerate(st.session_state.missoes_ativas):
        c_info, c_del = st.columns([5, 1])
        c_info.info(f"**{m['categoria']}**: {m['servico']} | {m['local']} | R$ {m['valor']}")
        if c_del.button("Excluir", key=f"del_{m['id']}"):
            st.session_state.missoes_ativas.pop(i)
            st.rerun()

# --- MODO PRESTADOR (VISÃO DE QUEM VAI TRABALHAR) ---
else:
    st.title("🚀 Radar de Missões GS")
    
    # CRIA AS ABAS DINAMICAMENTE
    tabs = st.tabs(categorias_master)

    for i, cat_nome in enumerate(categorias_master):
        with tabs[i]:
            # Filtra apenas o que é daquela categoria
            servicos_da_aba = [s for s in st.session_state.missoes_ativas if s['categoria'] == cat_nome]
            
            if not servicos_da_aba:
                st.write("---")
                st.info(f"Nenhum serviço de **{cat_nome}** disponível agora. Tente outra categoria!")
            else:
                for s in servicos_da_aba:
                    st.markdown(f"""
                        <div class="card">
                            <small>Solicitante: <b>{s['empresa']}</b></small>
                            <h2>{s['servico']}</h2>
                            <p>📍 Bairro: {s['local']}</p>
                            <div class="valor">R$ {s['valor']:.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Funcionalidades Extras
                    col_gps, col_foto, col_fim = st.columns([1, 1, 1])
                    with col_gps:
                        maps_link = f"https://www.google.com/maps/search/{s['local']}+Osasco"
                        st.markdown(f'<a href="{maps_link}" target="_blank" class="btn-maps">🗺️ ABRIR GPS</a>', unsafe_allow_html=True)
                    with col_foto:
                        st.file_uploader("📸 Foto da Conclusão", type=['jpg', 'png'], key=f"pic_{s['id']}")
                    with col_fim:
                        if st.button("✅ FINALIZAR", key=f"fin_{s['id']}"):
                            st.balloons()
                            st.success("Missão concluída com sucesso!")
                
