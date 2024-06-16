import streamlit as st
from streamlit_chat import message
from rag import ChatRAG

st.set_page_config(page_title="RAG_LINK")

def display_messages(chat_id):
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["chats"][chat_id]["messages"]):
        message(msg, is_user=is_user, key=f"{chat_id}_{i}")
    st.session_state["thinking_spinner"] = st.empty()

def process_input(chat_id):
    if len(st.session_state["chats"][chat_id]["link"]) > 0:
        user_text = st.session_state["user_input"].strip()
        if user_text:
            with st.session_state["thinking_spinner"], st.spinner("Thinking"):
                agent_text = st.session_state["chats"][chat_id]["assistant"].ask(user_text)

            st.session_state["chats"][chat_id]["messages"].append((user_text, True))
            st.session_state["chats"][chat_id]["messages"].append((agent_text, False))

            st.session_state["user_input"] = ""

def load_and_process_link(chat_id):
    link = st.session_state["chats"][chat_id]["link"]
    st.session_state["chats"][chat_id]["assistant"].ingest(link_user=link)

def set_api_key():
    api_key = st.session_state["input_api_key"]
    if api_key.startswith("sk-") or api_key == "":
        st.session_state["api_key"] = api_key
        st.session_state["api_key_error"] = ""

        # Aggiorna l'API key per ogni assistente esistente
        for chat in st.session_state["chats"]:
            if chat["assistant"] is not None:
                chat["assistant"].change_apikey(api_key)
    else:
        st.session_state["api_key_error"] = "API Key non valida. Deve iniziare con 'sk-'."

def set_link(chat_id):
    link = st.session_state["input_link"]
    if link.startswith("https"):
        st.session_state["chats"][chat_id]["link"] = link
        st.session_state["link_error"] = ""

        chat_name = link.replace("https://", "")
        st.session_state["chat_names"][chat_id] = chat_name
    else:
        st.session_state["link_error"] = "Link non valido. Deve iniziare con 'https'."

def create_new_chat():
    new_chat_id = len(st.session_state["chats"])
    st.session_state["chats"].append({
        "messages": [],
        "api_key": "",
        "link": "",
        "assistant": None
    })
    st.session_state["chat_names"].append(f"Chat {new_chat_id + 1}")
    st.session_state["current_chat"] = new_chat_id
    st.session_state["input_link"] = ""

def select_chat():
    chat_name = st.session_state["selected_chat"]
    st.session_state["current_chat"] = st.session_state["chat_names"].index(chat_name)

def page():
    st.sidebar.header("Configurazione API")
    
    if "api_key" not in st.session_state:
        st.session_state["api_key"] = ""
    
    if "chats" not in st.session_state:
        st.session_state["chats"] = []
    
    if "current_chat" not in st.session_state:
        st.session_state["current_chat"] = None
    
    if "chat_names" not in st.session_state:
        st.session_state["chat_names"] = []

    st.sidebar.text_input("API Key", key="input_api_key", type="password", on_change=set_api_key)
    
    if "api_key_error" not in st.session_state:
        st.session_state["api_key_error"] = ""
    if st.session_state["api_key_error"]:
        st.sidebar.error(st.session_state["api_key_error"])

    st.sidebar.button("Crea Nuova Chat", on_click=create_new_chat)
    
    if st.session_state["chats"]:
        _ = st.sidebar.selectbox("Seleziona una chat", options=st.session_state["chat_names"], 
                                             index=st.session_state["current_chat"] if st.session_state["current_chat"] is not None else 0, 
                                             on_change=select_chat, key="selected_chat")
    
    chat_id = st.session_state["current_chat"]

    if chat_id is not None:
        st.header("Inserisci Link Esterno")
        
        if "link_error" not in st.session_state:
            st.session_state["link_error"] = ""

        st.text_input("Link Esterno", key="input_link", on_change=set_link, args=(chat_id,))
        if st.session_state["link_error"]:
            st.error(st.session_state["link_error"])

        if st.session_state["api_key"] and st.session_state["chats"][chat_id]["link"] and not st.session_state["link_error"]:
            if st.session_state["chats"][chat_id]["assistant"] is None:
                st.session_state["chats"][chat_id]["assistant"] = ChatRAG(apikey=st.session_state["api_key"]) if st.session_state["api_key"] else ChatRAG()
                load_and_process_link(chat_id)

            display_messages(chat_id)
            st.text_input("Message", key="user_input", on_change=process_input, args=(chat_id,))

if __name__ == "__main__":
    page()
