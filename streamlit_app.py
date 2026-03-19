import streamlit as st
import time

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="GS Consultoria - Radar Completo", page_icon="🚀", layout="wide")

# ESTILO VISUAL (Eco-Business)
st.markdown("""
    <style>
    .stApp { background-color: #F0F9F1 !important; }
    .card { 
        background: white; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #2E7D32; box-shadow: 2px 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 15px; 
    }
    .valor { color: #2E7D32; font-size: 28px; font-weight: bold; }
    .pix-box { 
        background-color: #E0F2F1; padding: 5px 10px; border-radius: 5px; 
        color: #00796B; font-weight: bold; font-size: 14px; display: inline-block;
    }
    .btn-maps { 
        background-color: #4285F4; color: white !important; 
        padding: 8px 15px; border-radius: 8px; text-decoration: none; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DE DADOS
if 'missoes_ativas' not in st.session_state:
    st.session_state.missoes_ativas = [
        {"id": 1, "empresa": "Residencial Osasco", "categoria": "⚡ Eletricista", "servico": "Troca de Disjuntor", "local": "Rochdale", "valor": 120.0},
        {"id": 2, "empresa": "Particular", "categoria": "🛋️ Montador", "servico": "Montar Guarda-Roupa", "local": "Km 18", "valor": 150.0}
    ]
if 'logado' not in st.session_state: st.session_state.logado = False

# 3. LOGIN (1/1)
if not st.session_state.logado:
    st.title("GS Consultoria 🌱")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")
    if st.button("ACESSAR"):
        if u == "1" and s == "1":
            st.session_state.logado = True
            st.rerun()
    st.stop()

# 4. CATEGORIAS ATUALIZADAS
categorias_master = [
    "🧹 Zeladoria", "💅 Beleza", "🛠️ Reparos", "🛋️ Montador", 
    "🪚 Marceneiro", "🚰 Encanador", "⚡ Eletricista", "🔑 Chaveiro",
    "🌳 Jardinagem", "🧼 Limpeza", "📦 Entregas", "🚚 Carretos"
]

# SIDEBAR
with st.sidebar:
    st.write(f"### Olá, Geovani!")
    modo = st.radio("Visão:", ["🚀 Radar do Prestador", "🏢 Gestão da Empresa"])
    if st.button("SAIR"):
        st.session_state.logado = False
        st.rerun()

# --- MODO EMPRESA ---
if modo == "🏢 Gestão da Empresa":
    st.title("🏢 Painel de Lançamentos")
    with st.form("form_os"):
        col1, col2 = st.columns(2)
        with col1:
            emp_name = st.text_input("Cliente/Empresa", value="GS Consultoria")
            cat_sel = st.selectbox("Categoria", categorias_master)
            valor_os = st.number_input("Valor (R$)", min_value=1.0)
        with col2:
            serv_desc = st.text_input("O que precisa ser feito?")
            bairro_loc = st.text_input("Local (Bairro)")
        
        if st.form_submit_button("LANÇAR NO RADAR 🚀"):
            if serv_desc and bairro_loc:
                nova_m = {
                    "id": int(time.time()), "empresa": emp_name, 
                    "categoria": cat_sel, "servico": serv_desc, 
                    "local": bairro_loc, "valor": valor_os
                }
                st.session_state.missoes_ativas.append(nova_m)
                st.success("Publicado!")
                st.rerun()

    st.subheader("📋 Ativas")
    for i, m in enumerate(st.session_state.missoes_ativas):
        c_i, c_d = st.columns([5, 1])
        c_i.write(f"**{m['categoria']}**: {m['servico']} - {m['local']}")
        if c_d.button("❌", key=f"del_{m['id']}"):
            st.session_state.missoes_ativas.pop(i)
            st.rerun()

# --- MODO PRESTADOR ---
else:
    st.title("🚀 Radar GS - Osasco")
    tabs = st.tabs(categorias_master)

    for i, cat_nome in enumerate(categorias_master):
        with tabs[i]:
            servicos = [s for s in st.session_state.missoes_ativas if s['categoria'] == cat_nome]
            if not servicos:
                st.info(f"Sem chamados para {cat_nome} agora.")
            else:
                for s in servicos:
                    st.markdown(f"""
                        <div class="card">
                            <div style="display: flex; justify-content: space-between;">
                                <small>Solicitante: {s['empresa']}</small>
                                <span class="pix-box">🔹 PAGAMENTO VIA PIX</span>
                            </div>
                            <h2>{s['servico']}</h2>
                            <p>📍 Local: {s['local']}</p>
                            <div class="valor">R$ {s['valor']:.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    c_gps, c_foto, c_fim = st.columns(3)
                    with c_gps:
                        link = f"https://www.google.com/maps/search/{s['local']}+Osasco"
                        st.markdown(f'<a href="{link}" target="_blank" class="btn-maps">🗺️ GPS</a>', unsafe_allow_html=True)
                    with c_foto:
                        st.file_uploader("📸 Comprovante", type=['jpg'], key=f"p_{s['id']}")
                    with c_fim:
                        if st.button("✅ FINALIZAR", key=f"f_{s['id']}"):
                            st.balloons()
                            st.success("Missão Concluída!")
            
