import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="CodeStore Technologies Internal Bot",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------
# Custom Styling
# ---------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center;">
    <h1>CodeStore Technologies Internal Bot 🤖</h1>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------
# Session Memory
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# ---------------------------
# Display Chat History
# ---------------------------
for i, msg in enumerate(st.session_state.messages):

    with st.chat_message(msg["role"]):

        if st.session_state.edit_index == i and msg["role"] == "user":

            edited_text = st.text_area(
                "Edit your question",
                value=msg["content"],
                key=f"text_edit_{i}"
            )

            col1, col2 = st.columns(2)

            if col1.button("🔄 Re-search", key=f"research_{i}"):

                st.session_state.messages[i]["content"] = edited_text

                if i + 1 < len(st.session_state.messages):
                    if st.session_state.messages[i+1]["role"] == "assistant":
                        st.session_state.messages.pop(i+1)

                st.session_state.edit_index = None

                full_response = ""

                with st.chat_message("assistant"):
                    placeholder = st.empty()

                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=st.session_state.messages[:i+1],
                        stream=True
                    )

                    for chunk in response:
                        if chunk.choices[0].delta.content:
                            token = chunk.choices[0].delta.content
                            full_response += token
                            placeholder.markdown(full_response)

                st.session_state.messages.insert(
                    i+1,
                    {"role": "assistant", "content": full_response}
                )

                st.rerun()

            if col2.button("Cancel", key=f"cancel_{i}"):
                st.session_state.edit_index = None
                st.rerun()

        else:

            col_msg, col_edit = st.columns([8,1])

            with col_msg:
                st.markdown(msg["content"])

            if msg["role"] == "user":
                with col_edit:
                    if st.button("✏️", key=f"edit_{i}"):
                        st.session_state.edit_index = i
                        st.rerun()

# ---------------------------
# Chat Input
# ---------------------------

with st.form("chat_form", clear_on_submit=True):

    col_plus, col_input, col_send = st.columns([1,8,1])

    with col_plus:
        with st.popover("➕"):
            uploaded_doc = st.file_uploader(
                "Upload document",
                type=["pdf", "docx", "txt"]
            )

            uploaded_img = st.file_uploader(
                "Upload image",
                type=["png", "jpg", "jpeg"]
            )

    with col_input:
        prompt = st.text_input(
            "Prompt",
            placeholder="Ask me anything...",
            label_visibility="collapsed"
        )

    with col_send:
        send = st.form_submit_button("⬆️")

# ---------------------------
# Send message
# ---------------------------
if send and prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    full_response = ""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=st.session_state.messages,
        stream=True
    )

    with st.chat_message("assistant"):
        placeholder = st.empty()

        for chunk in response:
            if chunk.choices[0].delta.content:
                token = chunk.choices[0].delta.content
                full_response += token
                placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

    st.rerun()