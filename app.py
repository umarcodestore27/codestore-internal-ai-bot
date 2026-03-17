import streamlit as st
import requests
from PyPDF2 import PdfReader

OLLAMA_URL = "http://localhost:11434/api/generate"

st.set_page_config(page_title="CodeStore Bot", page_icon="🤖")

# ---------------------------
# 🔥 Sticky Header
# ---------------------------
st.markdown("""
<style>
.block-container > div:first-child {
    position: sticky;
    top: 0;
    background: #0e1117;
    z-index: 999;
    padding: 15px 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.4);
    text-align: center; /* ✅ center align */
}

/* Add spacing below header */
.header-space {
    height: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h2 style='margin:0;'>🤖 CodeStore Internal Bot</h2>",
    unsafe_allow_html=True
)

# ✅ Add spacing below header
st.markdown("<div class='header-space'></div>", unsafe_allow_html=True)

# ---------------------------
# Session State
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stop" not in st.session_state:
    st.session_state.stop = False

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if "edit_text" not in st.session_state:
    st.session_state.edit_text = ""

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

if "input_value" not in st.session_state:
    st.session_state.input_value = ""

# ---------------------------
# PDF Extract
# ---------------------------
def extract_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text[:2000]

# ---------------------------
# Chat Function
# ---------------------------
def chat(prompt, history, file=None):

    system_prompt = "You are an expert AI coding assistant. Answer clearly and concisely.\n"

    if file:
        if file.type == "application/pdf":
            system_prompt += extract_pdf(file)
        else:
            system_prompt += "\nUser uploaded an image.\n"

    for msg in history:
        system_prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"

    system_prompt += f"User: {prompt}\nAssistant:"

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "deepseek-coder",
            "prompt": system_prompt,
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": 1024}
        }
    )

    return response.json().get("response", "⚠️ No response")

# ---------------------------
# 🔥 SEND CALLBACK (FIXES INPUT BUG)
# ---------------------------
def handle_send():
    user_text = st.session_state.input_value.strip()

    if user_text == "":
        return

    if st.session_state.stop:
        st.warning("⛔ Generation stopped")
        st.session_state.stop = False
        return

    st.session_state.messages.append({
        "role": "user",
        "content": user_text
    })

    response = chat(user_text, st.session_state.messages[:-1], uploaded_file)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    # ✅ SAFE CLEAR (NO ERROR)
    st.session_state.input_value = ""

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    uploaded_file = st.file_uploader("📎 Upload PDF/Image")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------
# Chat Display (WITH EDIT BUTTON)
# ---------------------------
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):

        col1, col2 = st.columns([10,1])

        with col1:
            st.markdown(msg["content"])

        if msg["role"] == "user":
            with col2:
                if st.button("✏️", key=f"edit_{i}"):
                    st.session_state.edit_mode = True
                    st.session_state.edit_text = msg["content"]
                    st.session_state.edit_index = i

# ---------------------------
# Edit Logic
# ---------------------------
if st.session_state.edit_mode:
    new_text = st.text_area("Edit your question:", st.session_state.edit_text)

    if st.button("🔄 Re-run"):
        i = st.session_state.edit_index

        st.session_state.messages = st.session_state.messages[:i]

        st.session_state.messages.append({
            "role": "user",
            "content": new_text
        })

        response = chat(new_text, st.session_state.messages[:-1], uploaded_file)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.session_state.edit_mode = False
        st.session_state.edit_index = None
        st.rerun()

# ---------------------------
# 🔥 INPUT ROW (FINAL)
# ---------------------------
col1, col2, col3 = st.columns([8,1,1])

with col1:
    st.text_input(
    "Message Input",  # ✅ non-empty label
    placeholder="Ask something...",
    label_visibility="collapsed",  # 👈 still hidden in UI
    key="input_value"
)

with col2:
    st.button("⬆️", on_click=handle_send)

with col3:
    if st.button("⛔"):
        st.session_state.stop = True