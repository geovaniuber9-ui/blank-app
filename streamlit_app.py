import streamlit as st
import pandas as pd
import random

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="GS Radar Master", page_icon="🚀", layout="wide")

# Estilos CSS Globais
st.markdown("""
    <style>
    .stApp { background-color: #F4F7F4; }
    
    .wallet-box {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    
    /* Card de Serviço */
    .service-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border-left: 8px solid #2E7D32;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 5px;
    }
    
    .urgent-border { border-left: 8px solid #FFD700 !important; background-color: #FFFDF0; }
    
    .price { color: #2E7D32; font-size: 22px; font-weight: bold; }
    .dist { color: #666; font-size: 14px; font-weight: bold; }
    .verified { color: #1E88E5; font-size: 12px; font-weight: bold; background: #E3F2FD; padding: 2px 6px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ESTADOS ---
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 50.00
if 'missoes' not in st.session_state: 
    st.session_state.missoes = [
        {"id": 3790, "emp": "GS Consultoria", "resp": "Antonia", "cat": "Beleza", "serv": "Pé e Mão", "loc": "Rua Emília Pilon, 47 - Osasco", "val": 120.0, "urg": True, "km": 1.2}
    ]
if 'missao_ativa' not in st.session_state: st.session_state.missao_ativa = None
if 'historico' not in st.session_state: st.session_state.historico = []

# --- 3. LOGIN ---
if not st.session_state.logado:
    st.title("GS Consultoria 🌱")
    if st.button("ACESSAR SISTEMA"):
        st.session_state.logado = True
        st.rerun()
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown(f'<div class="wallet-box"><small>SALDO GS</small><br><span style="font-size: 26px;">R$ {st.session_state.saldo:.2f}</span></div>', unsafe_allow_html=True)
    aba = st.radio("Menu:", ["🚀 Radar", "🏢 Empresa", "📊 Ganhos"])
    if st.button("Logout"):
        st.session_state.logado = False
        st.rerun()

# --- 5. TELAS ---

if aba == "🚀 Radar":
    if st.session_state.missao_ativa:
        m = st.session_state.missao_ativa
        st.title("🏃 Missão em Andamento")
        st.warning(f"Destino: {m['loc']}")
        
        url_maps = f"https://www.google.com/maps/search/?api=1&query={m['loc'].replace(' ', '+')}"
        st.link_button("📍 ABRIR GPS AGORA", url_maps, type="primary", use_container_width=True)
        
        st.divider()
        with st.container(border=True):
            st.subheader("Concluir Serviço")
            st.file_uploader("Foto da conclusão")
            if st.button("FINALIZAR E RECEBER", use_container_width=True):
                st.session_state.saldo += m['val']
                st.session_state.historico.append(m)
                st.session_state.missao_ativa = None
                st.success("Saldo creditado!")
                st.rerun()
        
        if st.button("Cancelar"):
            st.session_state.missao_ativa = None
            st.rerun()

    else:
        st.title("📲 Radar GS - Osasco")
        cats = ["Zeladoria", "Encanador", "Montador", "Beleza"]
        tabs = st.tabs([f"📍 {c}" for c in cats])
        
        for i, tab in enumerate(tabs):
            with tab:
                cat_nome = cats[i]
                vagas = [v for v in st.session_state.missoes if v['cat'] == cat_nome]
                
                if not vagas:
                    st.info(f"Sem pedidos de {cat_nome} no momento.")
                else:
                    for v in vagas:
                        # RENDERIZAÇÃO LIMPA E SEM ERRO
                        urg_class = "urgent-border" if v['urg'] else ""
                        
                        # Bloco HTML Puro para o Card
                        st.markdown(f"""
                        <div class="service-card {urg_class}">
                            <div style="display: flex; justify-content: space-between;">
                                <b>{v['emp']}</b>
                                <span class="dist">📍 {v['km']} km</span>
                            </div>
                            <h2 style="margin: 10px 0; color: #333;">{v['serv']}</h2>
                            <p style="color: #666; margin-bottom: 10px;">🏠 {v['loc']} | 👤 {v['resp']}</p>
                            <span class="price">R$ {v['val']:.2f}</span>
                            { '<br><span class="verified">✅ VERIFICADA</span>' if v['id'] else '' }
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # O segredo: o botão de aceitar logo abaixo, com chave única
                        if st.button(f"ACEITAR ESTA MISSÃO (#{v['id']})", key=f"btn_{v['id']}", use_container_width=True):
                            st.session_state.missao_ativa = v
                            st.session_state.missoes = [x for x in st.session_state.missoes if x['id'] != v['id']]
                            st.rerun()

elif aba == "🏢 Empresa":
    st.title("🏢 Lançar Serviço")
    with st.form("lancar"):
        c1, c2 = st.columns(2)
        with c1:
            emp = st.text_input("Sua Empresa/Nome", "GS Consultoria")
            serv = st.text_input("O que precisa ser feito?")
        with c2:
            cat = st.selectbox("Categoria", ["Zeladoria", "Encanador", "Montador", "Beleza"])
            val = st.number_input("Valor para o prestador", value=80.0)
        
        loc = st.text_input("Endereço em Osasco/Região")
        urg = st.checkbox("Impulsionar (Destaque)")
        
        if st.form_submit_button("PUBLICAR NO RADAR"):
            taxa = 5.0 if urg else 2.0
            if st.session_state.saldo >= taxa:
                st.session_state.saldo -= taxa
                nova = {
                    "id": random.randint(1000, 9999), "emp": emp, "resp": "User",
                    "cat": cat, "serv": serv, "loc": loc, "val": val, "urg": urg,
                    "km": round(random.uniform(0.5, 10.0), 1)
                }
                st.session_state.missoes.append(nova)
                st.success("Publicado com sucesso!")
                st.rerun()
            else:
                st.error("Saldo insuficiente para a taxa.")

elif aba == "📊 Ganhos":
    st.title("📊 Extrato")
    if st.session_state.historico:
        df = pd.DataFrame(st.session_state.historico)
        st.metric("Total Ganho", f"R$ {df['val'].sum():.2f}")
        st.dataframe(df[['serv', 'val', 'loc']], use_container_width=True)
    else:
        st.info("Trabalhe para ver seus ganhos aqui!")
                
