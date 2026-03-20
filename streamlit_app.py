import streamlit as st
import pandas as pd
import random

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="GS Radar Master", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F0F2F0; }
    
    .wallet-box {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    
    .status-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border-left: 6px solid #2E7D32; margin-bottom: 10px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08); position: relative;
    }

    .urgent-card {
        border: 2px solid #FFD700 !important;
        background-color: #FFFDF0 !important;
    }

    .urgent-label {
        background: #FFD700; color: #000; font-size: 10px; font-weight: bold;
        padding: 2px 10px; border-radius: 5px; position: absolute; top: 10px; right: 10px;
    }

    .distance-tag { color: #666; font-size: 13px; font-weight: bold; }
    .price-tag { color: #2E7D32; font-size: 24px; font-weight: bold; margin-top: 10px; }
    
    /* Ajuste para botões dentro de cards */
    .stButton button { width: 100%; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DE ESTADOS (MEMÓRIA DO APP) ---
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 50.00
if 'missoes' not in st.session_state: 
    # Missão de exemplo para teste inicial
    st.session_state.missoes = [
        {
            "id": 5657, "empresa": "GS Consultoria", "nome_resp": "Antonia", 
            "cat": "Beleza", "serv": "Pé e Mão", "loc": "Rua Emília Pilon, 47 - Osasco", 
            "val": 120.0, "urgente": True, "km": 1.2, "obs": "Cor vermelha"
        }
    ]
if 'missao_ativa' not in st.session_state: st.session_state.missao_ativa = None
if 'historico' not in st.session_state: st.session_state.historico = []

# --- 3. TELA DE LOGIN ---
if not st.session_state.logado:
    st.title("GS Consultoria 🌱")
    u = st.text_input("Usuário")
    p = st.text_input("Senha", type="password")
    if st.button("ACESSAR SISTEMA"):
        if u == "1" and p == "1":
            st.session_state.logado = True
            st.rerun()
    st.stop()

# --- 4. MENU LATERAL ---
with st.sidebar:
    st.markdown(f"""
        <div class="wallet-box">
            <small>SALDO DISPONÍVEL</small><br>
            <span style="font-size: 28px; font-weight: bold;">R$ {st.session_state.saldo:.2f}</span>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Navegação:", ["🚀 Radar de Missões", "🏢 Lançar Serviço", "📊 Meus Ganhos"])
    
    if st.button("Sair"):
        st.session_state.logado = False
        st.rerun()

# --- 5. LÓGICA DAS TELAS ---

# --- TELA: RADAR ---
if menu == "🚀 Radar de Missões":
    if st.session_state.missao_ativa:
        m = st.session_state.missao_ativa
        st.subheader("🛠️ Missão em Andamento")
        
        st.info(f"📍 Destino: {m['loc']}")
        
        # Link Direto para o Google Maps
        maps_url = f"https://www.google.com/maps/search/?api=1&query={m['loc'].replace(' ', '+')}"
        st.link_button("🗺️ ABRIR GPS (INICIAR ROTA)", maps_url, type="primary", use_container_width=True)
        
        st.divider()
        st.write(f"**Serviço:** {m['serv']} | **Valor:** R$ {m['val']:.2f}")
        
        with st.expander("Finalizar e Receber", expanded=True):
            foto = st.file_uploader("Tire uma foto do trabalho concluído", type=['jpg', 'png'])
            nota = st.select_slider("Avalie o cliente/local", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], value="⭐⭐⭐⭐⭐")
            
            if st.button("CONCLUIR MISSÃO E RECEBER"):
                if foto:
                    st.session_state.saldo += m['val']
                    st.session_state.historico.append(m)
                    st.session_state.missao_ativa = None
                    st.success(f"R$ {m['val']:.2f} creditados na sua conta!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("É necessário anexar a foto do serviço para finalizar.")
        
        if st.button("Cancelar e Voltar ao Radar"):
            st.session_state.missao_ativa = None
            st.rerun()

    else:
        st.title("📲 Radar GS - Osasco")
        categorias = ["Zeladoria", "Encanador", "Montador", "Beleza", "Diarista"]
        tabs = st.tabs([f"📍 {c}" for c in categorias])
        
        for i, tab in enumerate(tabs):
            with tab:
                cat_atual = categorias[i]
                vagas = [m for m in st.session_state.missoes if m['cat'] == cat_atual]
                
                if not vagas:
                    st.info(f"Nenhum pedido de {cat_atual} no momento.")
                else:
                    for m in vagas:
                        # RENDERIZAÇÃO DO CARD (CORRIGIDO)
                        u_class = "urgent-card" if m['urgente'] else ""
                        card_html = f"""
                        <div class="status-card {u_class}">
                            {f'<div class="urgent-label">⚡ URGENTE</div>' if m['urgente'] else ''}
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <b style="color: #1B5E20;">{m['empresa']}</b>
                                <span class="distance-tag">📍 {m['km']} km</span>
                            </div>
                            <h3 style="margin: 10px 0 5px 0; color: #333;">{m['serv']}</h3>
                            <p style="color: #666; font-size: 14px; margin-bottom: 5px;">{m['loc']}</p>
                            <div class="price-tag">R$ {m['val']:.2f}</div>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        if st.button(f"ACEITAR MISSÃO #{m['id']}", key=f"aceitar_{m['id']}"):
                            st.session_state.missao_ativa = m
                            # Remove do radar
                            st.session_state.missoes = [x for x in st.session_state.missoes if x['id'] != m['id']]
                            st.rerun()

# --- TELA: LANÇAR SERVIÇO ---
elif menu == "🏢 Lançar Serviço":
    st.title("🏢 Publicar Nova Vaga")
    
    with st.form("form_vaga"):
        c1, c2 = st.columns(2)
        with c1:
            empresa = st.text_input("Nome da Empresa", value="GS Consultoria")
            cliente = st.text_input("Nome do Responsável")
            endereco = st.text_input("Endereço (Rua, Número, Bairro)")
        with c2:
            categoria = st.selectbox("Categoria", ["Zeladoria", "Encanador", "Montador", "Beleza", "Diarista"])
            valor = st.number_input("Valor para o Prestador", min_value=10.0, value=100.0)
            impulsionar = st.checkbox("⚡ Impulsionar (Custo R$ 5,00)")
        
        descricao = st.text_input("Descrição Curta (O que deve ser feito?)")
        
        # Cálculo de Taxa
        taxa_plataforma = (valor * 0.10) + (5.0 if impulsionar else 0)
        st.warning(f"Taxa de publicação: R$ {taxa_plataforma:.2f}")
        
        if st.form_submit_button("🚀 PUBLICAR NO RADAR"):
            if st.session_state.saldo >= taxa_plataforma:
                st.session_state.saldo -= taxa_plataforma
                nova_vaga = {
                    "id": random.randint(1000, 9999),
                    "empresa": empresa, "nome_resp": cliente, "cat": categoria,
                    "serv": descricao, "loc": endereco, "val": valor,
                    "urgente": impulsionar, "km": round(random.uniform(0.5, 12.0), 1)
                }
                st.session_state.missoes.append(nova_vaga)
                st.success("Vaga publicada! Saldo debitado.")
                st.rerun()
            else:
                st.error("Saldo insuficiente para publicar.")

# --- TELA: GANHOS ---
elif menu == "📊 Meus Ganhos":
    st.title("📊 Histórico de Lucros")
    if st.session_state.historico:
        df = pd.DataFrame(st.session_state.historico)
        st.metric("Total Ganho", f"R$ {df['val'].sum():.2f}")
        st.table(df[['serv', 'val', 'cat']])
    else:
        st.info("Nenhuma missão concluída ainda.")
            
