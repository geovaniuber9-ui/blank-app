import streamlit as st
import pandas as pd
import random

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="GS Radar Master", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAF8; }
    .wallet-box {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    .status-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border-left: 6px solid #2E7D32; margin-bottom: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08); position: relative;
    }
    .urgent-card { border: 2px solid #FFD700 !important; background-color: #FFFDF0 !important; }
    .urgent-label {
        background: #FFD700; color: #000; font-size: 10px; font-weight: bold;
        padding: 2px 10px; border-radius: 5px; position: absolute; top: 10px; right: 10px;
    }
    .distance-tag { color: #666; font-size: 14px; font-weight: 500; }
    .price-tag { color: #2E7D32; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE ESTADOS ---
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 50.00
if 'missoes' not in st.session_state: 
    # Mock inicial para teste
    st.session_state.missoes = [
        {"id": 1, "empresa": "GS Consultoria", "nome_resp": "Antonia", "cpf": "123", "cat": "Beleza", "serv": "Pe e mão", "loc": "Rua Emília Pilon, 47", "val": 120.0, "pag": "Pix", "obs": "Cor vermelha", "urgente": True, "km": 2.5}
    ]
if 'missao_ativa' not in st.session_state: st.session_state.missao_ativa = None
if 'historico' not in st.session_state: st.session_state.historico = []

# --- 3. LOGIN (Simplificado) ---
if not st.session_state.logado:
    st.title("GS Consultoria 🌱")
    if st.button("ACESSAR SISTEMA"):
        st.session_state.logado = True
        st.rerun()
    st.stop()

# --- 4. MENU LATERAL ---
with st.sidebar:
    st.markdown(f'<div class="wallet-box"><small>SALDO GS</small><br><span style="font-size: 28px;">R$ {st.session_state.saldo:.2f}</span></div>', unsafe_allow_html=True)
    aba = st.radio("Menu GS:", ["🚀 Radar", "🏢 Empresa", "📊 Ganhos", "🏆 Ranking"])
    if st.button("Logout"):
        st.session_state.logado = False
        st.rerun()

# --- 5. LÓGICA DAS TELAS ---

if aba == "🚀 Radar":
    # Se houver uma missão em andamento, mostra a tela de execução em vez do radar
    if st.session_state.missao_ativa:
        m = st.session_state.missao_ativa
        st.title("🛠️ Missão em Andamento")
        
        with st.container():
            st.info(f"Você está a caminho de: **{m['loc']}**")
            col1, col2 = st.columns(2)
            with col1:
                # Link para o Google Maps simulado
                maps_url = f"https://www.google.com/maps/search/?api=1&query={m['loc'].replace(' ', '+')}"
                st.link_button("📍 ABRIR GPS (MAPS)", maps_url, use_container_width=True)
            with col2:
                st.markdown(f"**Cliente:** {m['nome_resp']}\n\n**Valor:** R$ {m['val']:.2f}")

            st.divider()
            st.subheader("Finalizar Serviço")
            foto = st.file_uploader("Tire uma foto do serviço concluído", type=['png', 'jpg'])
            aval = st.select_slider("Avalie o atendimento", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"])
            
            if st.button("CONCLUIR E RECEBER", use_container_width=True, type="primary"):
                if foto:
                    st.session_state.saldo += m['val']
                    st.session_state.historico.append(m)
                    st.session_state.missao_ativa = None
                    st.success("Parabéns! O valor foi creditado na sua conta.")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Por favor, envie a foto do comprovante do serviço.")
            
            if st.button("Cancelar Missão", use_container_width=True):
                st.session_state.missao_ativa = None
                st.rerun()

    else:
        st.title("📲 Radar GS - Osasco")
        cats = ["Zeladoria", "Encanador", "Montador", "Beleza", "Diarista", "Saúde"]
        tabs = st.tabs([f"📍 {c}" for c in cats])
        
        for i, tab in enumerate(tabs):
            with tab:
                cat_nome = cats[i]
                lista = [m for m in st.session_state.missoes if m['cat'] == cat_nome]
                
                if not lista:
                    st.info(f"Nenhum pedido de {cat_nome} agora.")
                else:
                    for idx, m in enumerate(lista):
                        u_class = "urgent-card" if m['urgente'] else ""
                        st.markdown(f"""
                        <div class="status-card {u_class}">
                            {f'<div class="urgent-label">⚡ URGENTE</div>' if m['urgente'] else ''}
                            <div style="display: flex; justify-content: space-between;">
                                <b>{m['empresa']}</b>
                                <span class="distance-tag">📍 {m['km']} km de você</span>
                            </div>
                            <h2 style="margin:5px 0;">{m['serv']}</h2>
                            <p style="color:#555;">{m['loc']} | {m['nome_resp']}</p>
                            <div class="price-tag">R$ {m['val']:.2f}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"ACEITAR MISSÃO #{m['id']}", key=f"btn_{m['id']}", use_container_width=True):
                            st.session_state.missao_ativa = m
                            # Remove do radar para outros não verem
                            st.session_state.missoes = [item for item in st.session_state.missoes if item['id'] != m['id']]
                            st.rerun()

elif aba == "🏢 Empresa":
    st.title("🏢 Lançar Serviço")
    with st.form("f_os"):
        col1, col2 = st.columns(2)
        with col1:
            emp = st.text_input("Empresa", "GS Consultoria")
            resp = st.text_input("Nome do Cliente")
            loc = st.text_input("Endereço Completo")
        with col2:
            cat = st.selectbox("Categoria", ["Zeladoria", "Encanador", "Montador", "Beleza", "Diarista", "Saúde"])
            val = st.number_input("Valor ao Prestador (R$)", value=100.0)
            urgente = st.checkbox("⚡ IMPULSIONAR (Custo R$ 5,00)")
        
        serv = st.text_input("Título do Serviço (Ex: Pintura de Parede)")
        taxa = (val * 0.10) + (5.0 if urgente else 0)
        
        st.info(f"Custo de publicação: R$ {taxa:.2f} (Taxa GS)")
        
        if st.form_submit_button("🚀 PUBLICAR NO RADAR"):
            if st.session_state.saldo >= taxa:
                st.session_state.saldo -= taxa
                nova_missao = {
                    "id": random.randint(1000, 9999),
                    "empresa": emp, "nome_resp": resp, "cat": cat,
                    "serv": serv, "loc": loc, "val": val, "urgente": urgente,
                    "km": round(random.uniform(0.5, 15.0), 1), # Simula distância
                    "pag": "App", "obs": ""
                }
                st.session_state.missoes.append(nova_missao)
                st.success("Serviço publicado com sucesso!")
                st.rerun()
            else:
                st.error("Saldo insuficiente para cobrir as taxas de publicação.")

elif aba == "📊 Ganhos":
    st.title("📊 Extrato de Ganhos")
    if st.session_state.historico:
        df = pd.DataFrame(st.session_state.historico)
        st.metric("Total Acumulado", f"R$ {df['val'].sum():.2f}")
        st.dataframe(df[['serv', 'val', 'cat', 'loc']], use_container_width=True)
    else:
        st.info("Você ainda não concluiu missões.")
        
