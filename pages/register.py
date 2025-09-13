"""
Módulo de criação de novos usuários.
"""
import emoji

import streamlit as st
import api.user_requests as user_requests

# -----set-up inicial-----

# esconde sidebar criada automaticamente
st.markdown(
    '<style>[data-testid="stSidebar"] { display: none; }</style>', unsafe_allow_html=True)

# -----funções utilizadas neste módulo-----

def handle_register(name: str, email: str, password: str):
    with st.spinner("Registrando..."):
        response = user_requests.post_user(name, email, password)
        if response["success"]:
            st.success("Usuário registrado com sucesso")
        else:
            st.error("Erro ao registrar usuário.")

# -----conteúdo principal da página-----

st.title("Registre-se no TC-chat")
with st.form("register_form",
             clear_on_submit=True):
    name = st.text_input("Nome",
                         placeholder="Alfabeto Estrela")
    email = st.text_input("E-mail @ccc",
                          placeholder="alfabeto.estrela@ccc.ufcg.edu.br")
    password = st.text_input("Senha (min. 8 caracteres)",
                             type="password")
    if password and len(password) < 8:
        st.warning("A senha deve ter no mínimo 8 caracteres",
                   icon=emoji.emojize(":warning:"))
    submitted = st.form_submit_button("Registrar",
                                      use_container_width=True,
                                      type="primary",
                                      icon=emoji.emojize(":up_arrow:"))
    if submitted and len(password)>=8:
        handle_register(name,
                        email,
                        password)
        
button = st.button("Voltar à página de login",
                   use_container_width=True,
                   icon=emoji.emojize(":right_arrow_curving_left:"))
if button:
    st.switch_page("app.py")