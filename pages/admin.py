"""
Módulos para atividades de admins, como alterar dados de usuários ou recuperar
suas conversas.
"""
import emoji

import streamlit as st
import api.user_requests as user_requests
import api.chat_requests as chat_requests
import api.admin_requests as admin_requests
import util.message_formatting as message_formatting

# -----set-up inicial-----


st.set_page_config(
    page_title="Admin - TC-chat",
    page_icon=emoji.emojize(":hammer_and_wrench:")
)

# esconde sidebar e toolbar geradas automaticamente
st.markdown(
    '<style>[data-testid="stSidebarNav"] { display: none; }</style>', unsafe_allow_html=True)
st.markdown(
    '<style>[data-testid="stToolbar"] { display: none; }</style>', unsafe_allow_html=True)

# impede o acesso de um usuário não autenticado
if not st.session_state.get("is_authenticated", False):
    st.error("Acesso negado. Por favor, faça o login primeiro.",
             icon=emoji.emojize(":warning:"))
    st.switch_page("app.py")
    st.stop()

if "active_user_id" not in st.session_state:
    st.session_state.active_user_id = None
if "active_user" not in st.session_state:
    st.session_state.active_user = None
if "active_user_chats" not in st.session_state:
    st.session_state.active_user_chats = None


# -----funções utilizadas neste módulo-----


def select_user(user_id: int):
    st.session_state.active_user_id = user_id
    st.session_state.active_user = user_requests.get_user(user_id,
                                                          token=st.session_state.token)["result"]
    st.session_state.active_user_chats = chat_requests.get_all_chats(user_id,
                                                                     token=st.session_state.token)["result"]


def create_data_payload(name: str,
                        email: str,
                        is_authorized: bool,
                        daily_quota: int,
                        is_admin: bool):
    data = {}
    if name:
        data.update({"name": name})
    if email:
        data.update({"email": email})
    if is_authorized is not None:
        data.update({"isAuthorized": is_authorized})
    if daily_quota is not None:
        data.update({"dailyQuota": daily_quota})
    if is_admin is not None:
        data.update({"isAdmin": is_admin})
    return data


# -----sidebar de users-----


with st.sidebar:
    st.header("Administração")
    st.markdown("---")
    st.subheader("Usuários")

    if st.session_state.get("user_list") is None:
        with st.spinner("Buscando usuários..."):
            st.session_state.user_list = user_requests.get_all_users(
                token=st.session_state.token)["result"]

    for user in st.session_state.user_list:
        button_type = "primary" if user["id"] == st.session_state.active_user_id else "secondary"
        st.button(
            label=user["name"],
            key=f"user_{user["id"]}",
            on_click=select_user,
            args=(user["id"],),
            use_container_width=True,
            type=button_type,
        )

    st.markdown("<div style='height: 40vh;'></div>",
                unsafe_allow_html=True)

    if st.button("Voltar para a tela principal",
                 use_container_width=True,
                 icon=emoji.emojize(":right_arrow_curving_left:")):
        st.switch_page("pages/chats.py")


# -----conteúdo principal da página-----


st.title(emoji.emojize("Administração :hammer_and_wrench:"))

if st.session_state.active_user_id is None:
    select_user(st.session_state.user.get("id"))

st.markdown("### Informações do usuário")

with st.form("update_user_form",
             clear_on_submit=True):
    name = st.text_input("Nome",
                         value=st.session_state.active_user.get("name"))
    email = st.text_input("Email",
                          value=st.session_state.active_user.get("email"))
    id = st.text_input("ID do Usuário",
                       value=st.session_state.active_user_id,
                       disabled=True)
    is_authorized = st.text_input("Autorizado(a)",
                                  value=st.session_state.active_user.get("isAuthorized"))
    daily_quota = st.text_input("Quota diária",
                                value=st.session_state.active_user.get("dailyQuota"))
    is_admin = st.text_input("Administrador(a)",
                             value=st.session_state.active_user.get("isAdmin"))

    data = create_data_payload(name,
                               email,
                               is_authorized,
                               daily_quota,
                               is_admin)

    submitted = st.form_submit_button("Alterar dados",
                                      use_container_width=True)
    if submitted:
        with st.spinner("Processando..."):
            success = user_requests.put_user(
                user_id=st.session_state.active_user_id,
                data=data,
                token=st.session_state.token
            )["success"]

            if success:
                st.success("Dados do usuário alterados com sucesso.",
                           icon=emoji.emojize(":check_mark_button:"))
            else:
                st.warning("Erro ao alterar dados do usuário.",
                           icon=emoji.emojize(":warning:"))

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
                    user_id=st.session_state.active_user_id,
                    data={
                        "password": new_password
                    },
                    token=st.session_state.token
                )["success"]

            if success:
                st.success("Senha alterada com sucesso.",
                           icon=emoji.emojize(":check_mark_button:"))
            else:
                st.warning("Erro ao alterar a senha.",
                           icon=emoji.emojize(":warning:"))

st.markdown("---")
st.markdown("### Chats do usuário")
with st.container():
    if st.session_state.active_user_chats == []:
        st.markdown("O usuário ainda não criou nenhum chat.")
    for chat in st.session_state.active_user_chats:
        with st.expander(chat["title"]):
            messages = message_formatting.format_messages(chat["messages"])
            for message in messages:
                with st.chat_message(message["role"]):
                    st.markdown(message_formatting.format_message(
                        message["content"]))

st.markdown("---")
st.markdown("### Todos os usuários")

with st.form("change_daily_quota_reset_value_form",
             clear_on_submit=True):
    reset_value = st.text_input("Novo valor de quota diária")
    submitted = st.form_submit_button("Alterar valor")
    if submitted:
        response = admin_requests.change_daily_quota_reset_value(reset_value,
                                                                 st.session_state.token)
        if response["success"]:
            st.success("Valor da quota diária alterado com sucesso",
                       icon=emoji.emojize(":check_mark_button:"))
        else:
            st.warning("Erro ao alterar o valor da quota diária.",
                       icon=emoji.emojize(":right_arrow_curving_left:"))

if st.button("Executar reset da quota diária agora",
             use_container_width=True):
    response = admin_requests.run_daily_quota_reset(st.session_state.token)
    if response["success"]:
        st.success("Reset de quota diária executado com sucesso",
                   icon=emoji.emojize(":check_mark_button:"))
    else:
        st.warning("Erro ao executar o reset de quota diária.",
                   icon=emoji.emojize(":right_arrow_curving_left:"))

with st.form("change_all_users_authorization"):
    is_authorized = st.text_input("Autorizações de todos os membros",
                                  value="False")
    submitted = st.form_submit_button("Alterar autorização")

    if submitted:
        is_authorized = True if is_authorized == "True" else False
        response = admin_requests.change_all_users_authorization(is_authorized,
                                                                 st.session_state.token)
        if response["success"]:
            st.success("Autorizações de todos os usuários alteradas com sucesso",
                       icon=emoji.emojize(":check_mark_button:"))
        else:
            st.warning("Erro ao alterar as autorizações de todos os usuários.",
                       icon=emoji.emojize(":right_arrow_curving_left:"))
