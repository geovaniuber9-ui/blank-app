import streamlit as st
import pandas as pd
import random

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="GS Radar Master", page_icon="🚀", layout="wide")

# CSS Estilizado
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
    
    .stButton button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO ---
if 'logado' not in st.session_state: st.session_state.logado = False
if 'saldo' not in st.session_state: st.session_state.saldo = 50.00
if 'missoes' not in st.session_state: 
    st.session_state.missoes = [
        {
            "id": 3790, "empresa": "GS Consultoria", "nome_resp": "Antonia", 
            "cat": "Beleza", "serv": "Pé e Mão", "loc": "Rua Emília Pilon, 47 - Osasco", 
            "val": 100.0, "urgente": True, "km": 6.4
        }
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

# --- 4. MENU LATERAL ---
with st.sidebar:
    st.markdown(f'<div class="wallet-box"><small>SALDO</small><br><span style="font-size: 28px;">R$ {st.session_state.saldo:.2f}</span></div>', unsafe_allow_html=True)
    menu = st.radio("Menu:", ["🚀 Radar", "🏢 Lançar", "📊 Ganhos"])
    if st.button("Sair"):
        st.session_state.logado = False
        st.rerun()

# --- 5. TELAS ---

if menu == "🚀 Radar":
    if st.session_state.missao_ativa:
        m = st.session_state.missao_ativa
        st.subheader("🛠️ Missão Ativa")
        st.info(f"📍 Destino: {m['loc']}")
        
        # GPS Link
        maps_url = f"https://www.google.com/maps/search/?api=1&query={m['loc'].replace(' ', '+')}"
        st.link_button("🗺️ ABRIR GPS (INICIAR ROTA)", maps_url, type="primary")
        
        st.divider()
        with st.expander("Finalizar Serviço", expanded=True):
            st.file_uploader("Foto do trabalho", type=['jpg', 'png'])
            if st.button("CONCLUIR E RECEBER"):
                st.session_state.saldo += m['val']
                st.session_state.historico.append(m)
                st.session_state.missao_ativa = None
                st.success("Recebido!")
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
                    st.info("Buscando novas missões...")
                else:
                    for v in vagas:
                        # A MÁGICA PARA NÃO APARECER O CÓDIGO:
                        u_style = "urgent-card" if v['urgente'] else ""
                        
                        # Criamos o container visual PRIMEIRO
                        container = st.container()
                        with container:
                            # Renderizamos o HTML dentro do container
                            st.markdown(f"""
                            <div class="status-card {u_style}">
                                {f'<div class="urgent-label">⚡ URGENTE</div>' if v['urgente'] else ''}
                                <div style="display: flex; justify-content: space-between;">
                                    <b style="color: #1B5E20;">{v['empresa']}</b>
                                    <span class="distance-tag">📍 {v['km']} km</span>
                                </div>
                                <h2 style="margin: 5px 0; font-size: 20px;">{v['serv']}</h2>
                                <p style="color: #666; font-size: 14px;">{v['loc']}</p>
                                <div class="price-tag">R$ {v['val']:.2f}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # O botão fica logo abaixo, mas fora do bloco de texto HTML
                            if st.button(f"ACEITAR MISSÃO #{v['id']}", key=f"btn_{v['id']}"):
                                st.session_state.missao_ativa = v
                                st.session_state.missoes = [x for x in st.session_state.missoes if x['id'] != v['id']]
                                st.rerun()

elif menu == "🏢 Lançar":
    st.title("🏢 Lançar Serviço")
    with st.form("lancar"):
        emp = st.text_input("Empresa", "GS Consultoria")
        serv = st.text_input("Serviço")
        end = st.text_input("Endereço")
        cat = st.selectbox("Categoria", ["Zeladoria", "Encanador", "Montador", "Beleza"])
        val = st.number_input("Valor", value=100.0)
        urg = st.checkbox("Impulsionar")
        
        if st.form_submit_button("Publicar"):
            nova = {
                "id": random.randint(1000, 9999),
                "empresa": emp, "cat": cat, "serv": serv, 
                "loc": end, "val": val, "urgente": urg, "km": 5.0
            }
            st.session_state.missoes.append(nova)
            st.success("Publicado!")

elif menu == "📊 Ganhos":
    st.title("📊 Meus Ganhos")
    if st.session_state.historico:
        st.table(pd.DataFrame(st.session_state.historico)[['serv', 'val']])
        
