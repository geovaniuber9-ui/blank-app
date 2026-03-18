import streamlit as st
import pandas as pd
import time

# CONFIGURAÇÃO DA PÁGINA GS CONSULTORIA
st.set_page_config(page_title="LuzSocial v3.0", page_icon="⚡", layout="centered")

# ESTILO PARA PARECER APLICATIVO
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .card { background-color: white; padding: 20px; border-radius: 15px; border-left: 8px solid #1A237E; margin-bottom: 15px; box-shadow: 0px 2px 10px rgba(0,0,0,0.05); }
    .stButton>button { border-radius: 20px; height: 3em; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if 'status' not in st.session_state: st.session_state.status = "login"
if 'saldo' not in st.session_state: st.session_state.saldo = 0.0

# --- TELA DE LOGIN ---
if st.session_state.status == "login":
    st.title("⚡ LuzSocial")
    st.write("### Trabalho e Dignidade Instantânea")
    user = st.text_input("CPF ou Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("ENTRAR NO PAINEL"):
        st.session_state.status = "menu"
        st.rerun()

# --- MENU DE CATEGORIAS ---
elif st.session_state.status == "menu":
    st.title("📂 Categorias de Serviço")
    
    escolha = st.radio("Selecione o tipo de trabalho:", 
                      ["Zeladoria Urbana (Limpeza de Praças/Ruas)", 
                       "Serviços Domésticos (Cozinheira/Diarista)", 
                       "Serviço Comunitário"])

    st.divider()

    if "Zeladoria" in escolha:
        st.markdown('<div class="card"><h3>Varrer Praça da Matriz</h3><p>Osasco - Centro</p><h2>R$ 25,00</h2></div>', unsafe_allow_html=True)
        if st.button("VER MAPA E INICIAR"):
            st.session_state.status = "mapa"
            st.rerun()
    else:
        st.info(f"Buscando vagas para {escolha}...")
        st.warning("Nenhuma vaga aberta nesta região no momento.")

# --- TELA DE MAPA (GPS) ---
elif st.session_state.status == "mapa":
    st.header("🗺️ GPS de Navegação")
    
    # Coordenadas de Osasco (Ponto de Apoio e Destino)
    dados_mapa = pd.DataFrame({
        'lat': [-23.5325, -23.5335],
        'lon': [-46.7915, -46.7925]
    })
    
    st.map(dados_mapa) # MAPA REAL
    
    st.markdown("""
    **📍 Roteiro da Missão:**
    1. **Ponto de Apoio:** Base GS - Rua 15 (Retirar Vassoura/Pá).
    2. **Destino Final:** Praça da Matriz (Executar limpeza).
    """)
    
    if st.button("CHEGUEI NO DESTINO"):
        st.session_state.status = "executando"
        st.rerun()

# --- FINALIZAÇÃO ---
elif st.session_state.status == "executando":
    st.header("📸 Finalização")
    st.camera_input("Tire foto do serviço pronto")
    if st.button("CONCLUIR E RECEBER"):
        st.session_state.saldo += 25.0
        st.session_state.status = "pago"
        st.rerun()

elif st.session_state.status == "pago":
    st.balloons()
    st.success(f"✅ SUCESSO! Saldo atual: R$ {st.session_state.saldo:.2f}")
    if st.button("VOLTAR AO MENU"):
        st.session_state.status = "menu"
        st.rerun()
