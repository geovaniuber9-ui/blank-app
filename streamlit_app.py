import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO E ESTILO
st.set_page_config(page_title="GS Consultoria v19.0", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E0E0E0; }
    .card-trabalho {
        background: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #00D4FF;
        padding: 15px; border-radius: 8px; margin-bottom: 10px;
    }
    .valor { color: #00E676; font-size: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS EXPANDIDO (Conforme Imagens)
dados_trabalhos = {
    "🏥 Saúde": [
        ("Acompanhante Idoso", 120.0, "Vila Yara"),
        ("Cuidador Hospitalar", 180.0, "Centro"),
        ("Instrumentador Cirúrgico", 250.0, "Saúde"),
        ("Técnico de Enfermagem", 150.0, "Km 18")
    ],
    "🧹 Zeladoria": [
        ("Varrição de Vias e Praças", 45.0, "Centro"),
        ("Limpeza de Bueiros", 75.0, "Rochdale"),
        ("Pintura de Guias e Meio-fio", 90.0, "IAPI"),
        ("Pequenos Reparos (Loteamentos)", 130.0, "Piratininga"),
        ("Conservação de Monumentos", 110.0, "Bela Vista")
    ],
    "♻️ Resíduos": [
        ("Coleta de Lixo Seletiva", 65.0, "Km 18"),
        ("Triagem em Cooperativa", 55.0, "Mutinga"),
        ("Agente de Reciclagem (Condomínios)", 80.0, "Umuarama"),
        ("Coleta de Óleo de Cozinha", 40.0, "Centro")
    ],
    "🌱 Jardinagem": [
        ("Roçagem de Praças", 85.0, "Ayrosa"),
        ("Plantio de Mudas", 70.0, "City Bussocaba"),
        ("Manutenção de Áreas Verdes", 95.0, "Jardim Abril"),
        ("Limpeza de Terrenos Baldios", 120.0, "Adalgisa")
    ],
    "🎪 Eventos": [
        ("Montagem de Estruturas/Palcos", 150.0, "Estádio Municipal"),
        ("Logística de Grades/Cercas", 130.0, "Parque Continental"),
        ("Limpeza Pós-Evento", 100.0, "Centro de Eventos")
    ],
    "👨‍🍳 Cozinha": [
        ("Chef em Domicílio", 300.0, "Adalgisa"),
        ("Preparo de Marmitas", 140.0, "Bela Vista"),
        ("Ajudante de Buffet", 90.0, "Rochdale")
    ]
}

# 3. CONTROLE DE ESTADOS
if 'logado' not in st.session_state: st.session_state.logado = False
if 'status' not in st.session_state: st.session_state.status = "mural"
if 'missao' not in st.session_state: st.session_state.missao = None
if 'ganhos' not in st.session_state: st.session_state.ganhos = 0.0

# --- LOGIN ---
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center;'>⚡ GS CONSULTORIA</h1>", unsafe_allow_html=True)
    if st.button("ACESSAR DASHBOARD"):
        st.session_state.logado = True
        st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title(f"👤 Geovani Santi")
    st.metric("Saldo Acumulado", f"R$ {st.session_state.ganhos:.2f}")
    if st.button("🚪 Sair"):
        st.session_state.logado = False
        st.rerun()

# --- NAVEGAÇÃO ---

# ETAPA 1: MURAL
if st.session_state.status == "mural":
    st.title("📍 Mural de Missões Disponíveis")
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

# ETAPA 2: ROTA/MAPA
elif st.session_state.status == "gps":
    st.header(f"🧭 Indo para: {st.session_state.missao['local']}")
    st.info(f"Serviço: {st.session_state.missao['nome']}")
    
    # Botão para abrir o GPS externo
    st.markdown(f'<a href="https://www.google.com/maps/search/{st.session_state.missao["local"]}+Osasco" target="_blank"><button style="background:#FFB300; width:100%; border-radius:10px; padding:10px; font-weight:bold; border:none; color:black;">ABRIR NO GOOGLE MAPS</button></a>', unsafe_allow_html=True)
    
    st.map(pd.DataFrame({'lat': [-23.5325], 'lon': [-46.7915]})) # Centro de Osasco
    
    if st.button("✅ CHEGUEI NO LOCAL"):
        st.session_state.status = "evidencia_inicio"
        st.rerun()

# ETAPA 3: EVIDÊNCIAS DE INÍCIO (Selfie + Foto Antes)
elif st.session_state.status == "evidencia_inicio":
    st.header("📸 Registro de Início")
    st.warning("Obrigatório: Envie as fotos para liberar o início da tarefa.")
    
    selfie = st.camera_input("🤳 Tire uma Selfie para Validação")
    foto_antes = st.camera_input("📷 Foto do Local (COMO ESTÁ ANTES)")
    
    if selfie and foto_antes:
        if st.button("🚀 TUDO PRONTO! INICIAR TRABALHO"):
            st.session_state.status = "trabalhando"
            st.rerun()

# ETAPA 4: CRONÔMETRO/TRABALHO
elif st.session_state.status == "trabalhando":
    st.success(f"👷 TRABALHO EM ANDAMENTO: {st.session_state.missao['nome']}")
    st.markdown("Execute o serviço conforme as normas de segurança.")
    
    if st.button("🏁 CONCLUÍ O SERVIÇO"):
        st.session_state.status = "evidencia_fim"
        st.rerun()

# ETAPA 5: EVIDÊNCIA DE FINALIZAÇÃO (Foto Depois)
elif st.session_state.status == "evidencia_fim":
    st.header("📸 Registro de Entrega")
    st.info("Mostre o resultado final do seu trabalho.")
    
    foto_depois = st.camera_input("📷 Foto do Trabalho (DEPOIS / CONCLUÍDO)")
    
    if foto_depois:
        if st.button("💰 FINALIZAR E RECEBER"):
            st.session_state.ganhos += st.session_state.missao['valor']
            st.session_state.status = "concluido"
            st.rerun()

# ETAPA 6: PAGAMENTO CONCLUÍDO
elif st.session_state.status == "concluido":
    st.balloons()
    st.success(f"💎 Excelente trabalho! Pagamento de R$ {st.session_state.missao['valor']:.2f} creditado.")
    if st.button("VOLTAR AO MURAL"):
        st.session_state.status = "mural"
        st.rerun()
        
