"""
Ponto de partida da aplicação, faz login e salva as informações de user
e seus chats no st.session_state, além de definir quais são as páginas
para ambos usuários autenticado e não autenticado.
"""
import emoji

import streamlit as st
import api.login_requests as login_requests


# -----set-up inicial-----


st.set_page_config(
    page_title="Login - TC-chat",
    page_icon=emoji.emojize(":books:")
)

# esconde sidebar e toolbar geradas automaticamente
st.markdown(
    '<style>[data-testid="stSidebar"] { display: none; }</style>', unsafe_allow_html=True)
st.markdown(
    '<style>[data-testid="stToolbar"] { display: none; }</style>', unsafe_allow_html=True)


# -----funções utilizadas neste módulo-----


def initialize_session_state():
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False
        st.session_state.user = None
        st.session_state.token = None
        st.session_state.active_chat_id = None
        st.session_state.active_chat_messages = []
        st.session_state.chat_history = []


def handle_login(email: str, password: str):
    with st.spinner("Fazendo login..."):
        login_response = login_requests.post_login(email, password)
        try:
            if login_response["success"]:
                st.session_state.is_authenticated = True
                st.session_state.token = login_response["result"]["token"]
                st.session_state.user = login_response["result"]["user"]
                st.switch_page("pages/chats.py")
            else:
                st.error("E-mail ou senha incorretos.",
                         icon=emoji.emojize(":warning:"))
        except KeyError:
            st.error("E-mail ou senha incorretos.",
                     icon=emoji.emojize(":warning:"))
            

# -----conteúdo principal da página-----


initialize_session_state()

if st.session_state.is_authenticated:
    st.switch_page("pages/chats.py")

st.title("Faça login no TC-chat")

with st.form("login_form"):
    email = st.text_input("Email",
                          placeholder="alfabeto.estrela@ccc.ufcg.edu.br"
                          )
    password = st.text_input("Senha",
                             type="password"
                             )
    submitted = st.form_submit_button("Entrar",
                                      use_container_width=True,
                                      type="primary"
                                      )

if submitted:
    if not email or not password:
        st.warning("Por favor, preencha todos os campos.",
                   icon=emoji.emojize(":warning:"))
    else:
        handle_login(email, password)

button = st.button("Registre-se no TC-chat",
                   use_container_width=True,
                   icon=emoji.emojize(":bust_in_silhouette:"))
if button:
    st.switch_page("pages/register.py")
