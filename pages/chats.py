"""
Módulo de chats para conversas entre o usuário e a LLM.
"""
import sys
import emoji

import api.chat_requests as chat_requests
import streamlit as st

# -----set-up inicial-----

sys.path.append('..')

# esconde sidebar gerada automaticamente
st.markdown(
    '<style>[data-testid="stSidebarNav"] { display: none; }</style>', unsafe_allow_html=True)

st.session_state.chat_history = None

# impede acesso de usuário não autenticado
if not st.session_state.get("is_authenticated", False):
    st.error("Acesso negado. Por favor, faça o login primeiro.",
             icon=emoji.emojize(":warning:")
             )
    st.switch_page("app.py")
    st.stop()

# -----funções utilizadas neste módulo-----


def select_chat(chat_id):
    """
    Carrega as mensagens de um chat específico para o st.session_state, a fim
    de serem exibidas no conteúdo principal da tela.

    Args:
        chat_id: identificador único do chat.
    """
    st.session_state.active_chat_id = chat_id
    with st.spinner("Carregando conversa..."):
        chat = chat_requests.get_chat(user_id=st.session_state.user["id"],
                                      chat_id=chat_id,
                                      token=st.session_state.token
                                      )["result"]
        st.session_state.active_chat_messages = chat_requests.format_messages(
            chat["messages"]
        )


def new_chat():
    """
    Prepara o st.session_state para uma nova conversa, assim deixando o
    conteúdo principal da tela sem mensagens em exibição.
    """
    st.session_state.active_chat_id = None
    st.session_state.active_chat_messages = []


def logout():
    """
    Realiza logout ao remover todos os elementos do st.session_state e troca a
    página para a de login.
    """
    keys_to_delete = [
        "is_authenticated",
        "user",
        "token",
        "active_chat_id",
        "active_chat_messages",
        "chat_history"
    ]
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.chat_history = None
    st.switch_page("app.py")

# -----sidebar-----


with st.sidebar:
    # título da sidebar e botão de criar nova conversa
    st.header(f"Bem-vindo, {st.session_state["user"]["name"]}!")

    if st.button("Nova Conversa",
                 use_container_width=True,
                 on_click=new_chat,
                 icon=emoji.emojize(":plus:")
                 ):
        pass

    st.markdown("---")
    st.subheader("Histórico de chats")

    # carrega o histórico de chats do usuário para o st.session_state
    if st.session_state.get("chat_history") is None:
        with st.spinner('Buscando histórico...'):
            st.session_state.chat_history = chat_requests.get_all_chats(
                user_id=st.session_state.user['id'],
                token=st.session_state.token
            )["result"]

    # criação de botões na sidebar para cada chat do usuário
    for chat in st.session_state.chat_history:
        button_type = "primary" if chat['id'] == st.session_state.active_chat_id else "secondary"
        st.button(
            chat['title'],
            key=f"chat_{chat['id']}",
            on_click=select_chat,
            args=(chat['id'],),
            use_container_width=True,
            type=button_type
        )

    st.markdown("<div style='height: 40vh;'></div>",
                unsafe_allow_html=True)

    # demais botões da sidebar
    if st.button("Ver Perfil",
                 use_container_width=True):
        st.switch_page("pages/profile.py")

    if st.button("Logout",
                 use_container_width=True,
                 type="secondary",
                 on_click=logout):
        pass

# -----conteúdo principal da página-----

st.title(emoji.emojize("TC chat :books::robot:"))

# exibe as mensagens do chat atual
for message in st.session_state.get('active_chat_messages', []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# envio de novas mensagens no chat atual
if prompt := st.chat_input("Digite sua mensagem aqui..."):
    st.session_state.active_chat_messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Pensando..."):
        chat = None
        is_new_chat = False

        # se é a continuação de uma conversa já existente
        if st.session_state.active_chat_id:
            chat = chat_requests.put_chat(
                user_id=st.session_state.user['id'],
                chat_id=st.session_state.active_chat_id,
                prompt=prompt,
                token=st.session_state.token
            )["result"]
        # se é uma nova conversa
        else:
            is_new_chat = True
            chat = chat_requests.post_chat(
                user_id=st.session_state.user['id'],
                prompt=prompt,
                token=st.session_state.token
            )["result"]

        if chat:
            st.session_state.active_chat_id = chat['id']
            st.session_state.active_chat_messages = chat_requests.format_messages(
                chat['messages']
            )["result"]
            if is_new_chat:
                st.session_state.chat_history = None

    st.rerun()
