"""
Módulo de visualização das informações do perfil e alteração de senha de
usuário "aluno".
"""
import sys
import emoji

import api.user_requests as user_requests
import streamlit as st

# -----set-up inicial-----

sys.path.append('..')
st.set_page_config(
    page_title="Perfil - TC-chat",
    page_icon=emoji.emojize(":bust_in_silhouette:")
)

# esconde sidebar e toolbar geradas automaticamente
st.markdown(
    '<style>[data-testid="stSidebarNav"] { display: none; }</style>', unsafe_allow_html=True)
st.markdown(
    '<style>[data-testid="stToolbar"] { display: none; }</style>', unsafe_allow_html=True)

st.set_page_config(
    layout="centered",
    page_title="Meu Perfil",
    page_icon=emoji.emojize(":bust_in_silhouette:")
)

# impede o acesso de um usuário não autenticado
if not st.session_state.get("is_authenticated", False):
    st.error("Acesso negado. Por favor, faça o login primeiro.")
    st.switch_page("app.py")
    st.stop()

# -----conteúdo principal da página-----

st.title(emoji.emojize("Meu Perfil :bust_in_silhouette:"))
st.divider()
st.subheader("Informações do Usuário")

st.text_input("Nome",
              value=st.session_state.user.get('name', ''),
              disabled=True)
st.text_input("Email",
              value=st.session_state.user.get('email', ''),
              disabled=True)
st.text_input("ID do Usuário",
              value=st.session_state.user.get('id', ''),
              disabled=True)
st.text_input("Autorizado(a)",
              value=st.session_state.user.get('isAuthorized', ''),
              disabled=True)
st.text_input("Quota diária",
              value=st.session_state.user.get('dailyQuota', ''),
              disabled=True)

st.divider()
st.subheader("Alterar Senha")

# -----alteração de senha-----

with st.form("change_password_form",
             clear_on_submit=True):
    new_password = st.text_input("Nova Senha",
                                 type="password")
    confirm_password = st.text_input("Confirme a Nova Senha",
                                     type="password")

    submitted = st.form_submit_button("Alterar Senha",
                                      use_container_width=True)

    if submitted:
        if new_password != confirm_password:
            st.warning("As senhas não coincidem",
                       icon=emoji.emojize(":warning:"))
        elif len(new_password) < 8:
            st.warning("A senha deve ter no mínimo 8 caracteres",
                       icon=emoji.emojize(":warning:"))
        else:
            with st.spinner("Processando..."):
                success = user_requests.put_user(
                    user_id=st.session_state.user["id"],
                    password=new_password,
                    token=st.session_state.token
                )["success"]

            if success:
                st.success("Senha alterada com sucesso.",
                           icon=emoji.emojize(":check_mark_button:"))
            else:
                st.warning("Erro ao alterar a senha.",
                           icon=emoji.emojize(":warning:"))

with st.sidebar:
    if st.button("Voltar para a tela principal",
                 use_container_width=True,
                 icon=emoji.emojize(":right_arrow_curving_left:")):
        st.switch_page("pages/chats.py")
