import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="GS Consultoria v18.0", page_icon="⚡", layout="wide")

# 2. ESTILO DARK MODE PROFISSIONAL
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E0E0E0; }
    .card-trabalho {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #1A237E;
        padding: 15px; border-radius: 12px; margin-bottom: 10px;
    }
    .valor { color: #00E676; font-size: 22px; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(90deg, #00D4FF, #0052D4);
        color: white; border-radius: 10px; font-weight: bold; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BANCO DE DADOS DE TRABALHOS (Mais opções adicionadas)
dados_trabalhos = {
    "Saúde": [
        ("Acompanhante Idoso", 120.0, "Vila Yara"),
        ("Cuidador Hospitalar", 180.0, "Centro"),
        ("Instrumentador Cirúrgico", 250.0, "Saúde"),
        ("Técnico de Enfermagem", 150.0, "Km 18"),
        ("Fisioterapeuta Domiciliar", 200.0, "Campesina")
    ],
    "Cozinha": [
        ("Chef em Domicílio", 300.0, "Adalgisa"),
        ("Preparo de Marmitas (Dia)", 140.0, "Bela Vista"),
        ("Ajudante de Buffet", 90.0, "Rochdale"),
        ("Cozinheiro Geral", 160.0, "Umuarama")
    ],
    "Reparos": [
        ("Eletricista Residencial", 130.0, "Mutinga"),
        ("Encanador 24h", 110.0, "Piratininga"),
        ("Pintura de Parede", 95.0, "IAPI"),
        ("Instalação de Ar", 200.0, "Ayrosa")
    ],
    "Zeladoria": [
        ("Jardinagem Completa", 85.0, "Bela Vista"),
        ("Limpeza de Piscina", 70.0, "City Bussocaba"),
        ("Limpeza de Bueiro", 65.0, "Rochdale")
    ]
}

# 4. CONTROLE DE ESTADOS (Login e Fluxo)
if 'logado' not in st.session_state: st.session_state.logado = False
if 'status' not in st.session_state: st.session_state.status = "mural"
if 'missao' not in st.session_state: st.session_state.missao = None
if 'ganhos' not in st.session_state: st.session_state.ganhos = 0.0

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center;'>⚡ GS CONSULTORIA</h1>", unsafe_allow_html=True)
    if st.button("ACESSAR DASHBOARD"):
        st.session_state.logado = True
        st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("👤 Geovani Santi")
    st.metric("Saldo Total", f"R$ {st.session_state.ganhos:.2f}")
    if st.button("🚪 Sair"):
        st.session_state.logado = False
        st.rerun()

# --- LÓGICA DE NAVEGAÇÃO DO APP ---

# ETAPA 1: MURAL DE TRABALHOS
if st.session_state.status == "mural":
    st.title("📍 Radar de Missões")
    tabs = st.tabs(list(dados_trabalhos.keys()))
    
    for i, categoria in enumerate(dados_trabalhos.keys()):
        with tabs[i]:
            for nome, valor, local in dados_trabalhos[categoria]:
                st.markdown(f"""
                <div class="card-trabalho">
                    <b>{nome}</b><br>📍 {local}<br>
                    <span class="valor">R$ {valor:.2f}</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"ACEITAR: {nome}", key=f"{nome}_{local}"):
                    st.session_state.missao = {"nome": nome, "valor": valor, "local": local}
                    st.session_state.status = "gps"
                    st.rerun()

# ETAPA 2: GPS E CHEGADA
elif st.session_state.status == "gps":
    st.header(f"🧭 Rota: {st.session_state.missao['local']}")
    st.info(f"Trabalho: {st.session_state.missao['nome']}")
    
    # Botão de GPS real
    st.markdown(f'<a href="https://www.google.com/maps/search/{st.session_state.missao["local"]}+Osasco" target="_blank"><button style="background:#FFB300; color:black; width:100%; border:12px; padding:15px; font-weight:bold; border:none; cursor:pointer;">🧭 ABRIR MAPS / WAZE</button></a>', unsafe_allow_html=True)
    
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]})) # Centro de Osasco
    
    if st.button("✅ CHEGUEI NO LOCAL"):
        st.session_state.status = "fotos_entrada"
        st.rerun()

# ETAPA 3: SELFIE E FOTO DO ANTES
elif st.session_state.status == "fotos_entrada":
    st.header("🤳 Início do Turno")
    st.warning("Para iniciar, precisamos da sua selfie e da foto do local.")
    
    foto1 = st.camera_input("1. Sua Selfie (Validação)")
    foto2 = st.camera_input("2. Foto do local (ANTES do serviço)")
    
    if foto1 and foto2:
        if st.button("🚀 INICIAR TAREFA AGORA"):
            st.session_state.status = "em_andamento"
            st.rerun()

# ETAPA 4: TRABALHANDO
elif st.session_state.status == "em_andamento":
    st.success(f"⚡ VOCÊ ESTÁ EM SERVIÇO: {st.session_state.missao['nome']}")
    st.markdown("Execute o trabalho com excelência. Ao terminar, clique no botão abaixo.")
    
    if st.button("🏁 FINALIZAR TAREFA"):
        st.session_state.status = "foto_depois"
        st.rerun()

# ETAPA 5: FOTO DO DEPOIS E RECEBIMENTO
elif st.session_state.status == "foto_depois":
    st.header("📸 Finalização")
    st.info("Tire uma foto de como ficou o serviço (DEPOIS).")
    
    foto3 = st.camera_input("Foto da Entrega (DEPOIS)")
    
    if foto3:
        if st.button("💎 ENVIAR E RECEBER PAGAMENTO"):
            st.session_state.ganhos += st.session_state.missao['valor']
            st.session_state.status = "concluido"
            st.rerun()

# ETAPA 6: SUCESSO
elif st.session_state.status == "concluido":
    st.balloons()
    st.success(f"Dinheiro na conta! Você recebeu R$ {st.session_state.missao['valor']:.2f}")
    if st.button("VOLTAR AO MURAL"):
        st.session_state.status = "mural"
        st.rerun()
    
