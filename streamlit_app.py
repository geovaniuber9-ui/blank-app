import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="GS LuzSocial v8.0", page_icon="⚡", layout="wide")

# ESTILO CSS PARA CORRIGIR VISIBILIDADE E DESIGN
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    /* Ajuste do Menu Lateral para Leitura */
    [data-testid="stSidebar"] { background-color: #1A237E !important; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    .card { background-color: white; padding: 20px; border-radius: 15px; border-left: 10px solid #1A237E; margin-bottom: 20px; box-shadow: 0px 4px 15px rgba(0,0,0,0.1); color: #333; }
    .liquido { color: #2e7d32; font-size: 22px; font-weight: bold; }
    .imposto { color: #d32f2f; font-size: 13px; font-weight: bold; }
    .bruto { color: #757575; font-size: 13px; text-decoration: line-through; }
    .whatsapp-btn { background-color: #25D366; color: white; padding: 12px; border-radius: 10px; text-align: center; font-weight: bold; display: block; text-decoration: none; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO DE VARIÁVEIS
if 'saldo' not in st.session_state: st.session_state.saldo = 0.0
if 'status' not in st.session_state: st.session_state.status = "menu"
if 'missao_atual' not in st.session_state: st.session_state.missao_atual = None

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("⚡ GS Consultoria")
    st.markdown(f"### Olá, Geovani Santi")
    st.markdown(f"💰 **Saldo: R$ {st.session_state.saldo:.2f}**")
    st.divider()
    
    escolha = st.radio("Ir para:", 
                      ["Mural de Missões", "Escola de Profissões", "Meu Extrato", "Suporte & Segurança"])
    
    if st.button("🔄 Resetar App (Se travar)"):
        st.session_state.status = "menu"
        st.rerun()
    
    st.divider()
    if st.button("🚨 BOTÃO DE PÂNICO", use_container_width=True):
        st.error("🚨 ALERTA ENVIADO!")

# --- LÓGICA DE TELAS ---

# Se o usuário clicar no menu lateral, volta para o estado de "menu" principal
if st.session_state.status != "menu" and st.session_state.status != "pago" and st.session_state.status != "mapa" and st.session_state.status != "foto":
     st.session_state.status = "menu"

if escolha == "Mural de Missões" and st.session_state.status == "menu":
    st.title("📍 Missões Disponíveis em Osasco")
    
    aba1, aba2, aba3, aba4 = st.tabs(["🧹 Zeladoria", "🏠 Domésticos", "🏥 Saúde", "🤝 Comunitário"])

    with aba1: # Zeladoria
        vagas = [{"n": "Varrer Praça da Matriz", "l": "Centro", "b": 35.0}, {"n": "Limpeza de Bueiro", "l": "Rochdale", "b": 75.0}]
        for v in vagas:
            liq = v['b'] * 0.85
            st.markdown(f'<div class="card"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><p class="liquido">R$ {liq:.2f} Líquido</p></div>', unsafe_allow_html=True)
            if st.button(f"Aceitar: {v['n']}", key=f"z_{v['n']}"):
                st.session_state.missao_atual = {"nome": v['n'], "valor": liq}
                st.session_state.status = "mapa"; st.rerun()

    with aba2: # Domésticos
        vagas = [{"n": "Cozinheira (Almoço)", "l": "Vila Yara", "b": 150.0}, {"n": "Passadeira", "l": "Bela Vista", "b": 90.0}]
        for v in vagas:
            liq = v['b'] * 0.85
            st.markdown(f'<div class="card"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><p class="liquido">R$ {liq:.2f} Líquido</p></div>', unsafe_allow_html=True)
            if st.button(f"Aceitar: {v['n']}", key=f"d_{v['n']}"):
                st.session_state.missao_atual = {"nome": v['n'], "valor": liq}
                st.session_state.status = "mapa"; st.rerun()

    with aba3: # SAÚDE (NOVO)
        vagas = [{"n": "Cuidador de Idoso (Turno)", "l": "Saúde", "b": 200.0}, {"n": "Acompanhante Hospitalar", "l": "Centro", "b": 180.0}]
        for v in vagas:
            liq = v['b'] * 0.85
            st.markdown(f'<div class="card"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><p class="liquido">R$ {liq:.2f} Líquido</p></div>', unsafe_allow_html=True)
            if st.button(f"Aceitar: {v['n']}", key=f"s_{v['n']}"):
                st.session_state.missao_atual = {"nome": v['n'], "valor": liq}
                st.session_state.status = "mapa"; st.rerun()

    with aba4: # Comunitário
        vagas = [{"n": "Passeador de Cães", "l": "Continental", "b": 45.0}]
        for v in vagas:
            liq = v['b'] * 0.85
            st.markdown(f'<div class="card"><h3>{v["n"]}</h3><p>📍 {v["l"]}</p><p class="liquido">R$ {liq:.2f} Líquido</p></div>', unsafe_allow_html=True)
            if st.button(f"Aceitar: {v['n']}", key=f"c_{v['n']}"):
                st.session_state.missao_atual = {"nome": v['n'], "valor": liq}
                st.session_state.status = "mapa"; st.rerun()

elif escolha == "Escola de Profissões":
    st.title("🎓 Escola de Profissões")
    st.write("Acesse os portais oficiais abaixo:")
    st.markdown('<a href="https://www.gov.br" class="whatsapp-btn">Portal GOV.BR</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.sebrae.com.br" class="whatsapp-btn" style="background-color:#007bff">Portal SEBRAE</a>', unsafe_allow_html=True)

elif escolha == "Suporte & Segurança":
    st.title("📞 Suporte GS")
    link_zap = f"https://wa.me/5511917529636?text=Oi%20Geovani"
    st.markdown(f'<a href="{link_zap}" target="_blank" class="whatsapp-btn">💬 FALAR COM GEOVANI</a>', unsafe_allow_html=True)

# --- TELAS DE FLUXO (MAPA -> FOTO -> PAGO) ---
if st.session_state.status == "mapa":
    st.header(f"🗺️ Rota: {st.session_state.missao_atual['nome']}")
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]}))
    if st.button("CHEGUEI"): st.session_state.status = "foto"; st.rerun()

elif st.session_state.status == "foto":
    st.header("📸 Finalizar")
    st.camera_input("Foto do serviço")
    if st.button("RECEBER PAGAMENTO"):
        st.session_state.saldo += st.session_state.missao_atual['valor']
        st.session_state.status = "pago"; st.rerun()

elif st.session_state.status == "pago":
    st.balloons()
    st.success("Pagamento realizado!")
    if st.button("VOLTAR AO MENU"): st.session_state.status = "menu"; st.rerun()
    
