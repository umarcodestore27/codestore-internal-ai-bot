# import streamlit as st
# import requests
# from PyPDF2 import PdfReader

# OLLAMA_URL = "http://localhost:11434/api/generate"

# # ==============================
# # ⚙ Page Setup
# # ==============================
# st.set_page_config(page_title="CodeStore Coder Bot", page_icon="🤖")

# st.title("🤖 CodeStore Coder Bot")
# st.caption("Powered by Ollama (DeepSeek) • Built by CodeStore Team")
# st.markdown("""
# <style>
# .suggestion-box {
#     position: fixed;
#     bottom: 140px;
#     left: 50%;
#     transform: translateX(-50%);
#     width: 600px;
#     background: #0e1117;
#     padding: 12px;
#     border-radius: 12px;
#     border: 1px solid #333;
#     z-index: 999;
# }
# </style>
# """, unsafe_allow_html=True)
# # ==============================
# # 📂 Sidebar
# # ==============================
# with st.sidebar:
#     st.markdown("<h2 style='text-align:center;'>🤖 CodeStore Bot</h2>", unsafe_allow_html=True)
#     st.markdown("<br><br>", unsafe_allow_html=True)

#     st.header("📂 Upload")
#     uploaded_file = st.file_uploader(
#         "Upload",
#         type=["pdf", "png", "jpg", "jpeg"],
#         label_visibility="collapsed"
#     )

# # ==============================
# # 🧠 Session State
# # ==============================
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "followups" not in st.session_state:
#     st.session_state.followups = []

# if "edit_mode" not in st.session_state:
#     st.session_state.edit_mode = False

# if "edit_text" not in st.session_state:
#     st.session_state.edit_text = ""

# # ==============================
# # 🤖 Chat Function
# # ==============================
# def chat(msg, history):
#     prompt = "You are an expert coding assistant.\n"

#     for h in history:
#         prompt += f"{h['role']}: {h['content']}\n"

#     prompt += f"user: {msg}\nassistant:"

#     try:
#         res = requests.post(
#             OLLAMA_URL,
#             json={
#                 "model": "deepseek-coder",
#                 "prompt": prompt,
#                 "stream": False
#             },
#             timeout=60
#         )

#         # DEBUG
#         if res.status_code != 200:
#             return f"Error: {res.status_code} | {res.text}"

#         data = res.json()

#         # extra safety
#         if "response" not in data:
#             return f"⚠️ Invalid response: {data}"

#         return data["response"]

#     except Exception as e:
#         return f"⚠️ {str(e)}"
# # ==============================
# # 💬 Show Chat
# # ==============================
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # ==============================
# # ✏️ Edit Button
# # ==============================
# if st.session_state.messages:
#     if st.session_state.messages[-1]["role"] == "assistant":
#         if st.button("✏️ Edit last question"):
#             for m in reversed(st.session_state.messages):
#                 if m["role"] == "user":
#                     st.session_state.edit_text = m["content"]
#                     break
#             st.session_state.edit_mode = True
#             st.rerun()

# # ==============================
# # 💬 Followups
# # ==============================
# if st.session_state.followups:
#     st.markdown('<div class="suggestion-box">', unsafe_allow_html=True)
#     st.markdown('<div class="suggestion-title">💬 Suggestions</div>', unsafe_allow_html=True)

#     cols = st.columns(3)

#     for i, q in enumerate(st.session_state.followups):
#         if cols[i].button(q, key=f"f_{i}_{len(st.session_state.messages)}"):
#             st.session_state.followup = q
#             st.rerun()

#     st.markdown('</div>', unsafe_allow_html=True)

# # ==============================
# # 💬 PROCESS INPUT FIRST
# # ==============================
# user_input = None

# # followup click
# if "followup" in st.session_state:
#     user_input = st.session_state.followup
#     del st.session_state.followup

# # edit mode
# elif st.session_state.edit_mode:
#     edited = st.text_input("Edit your question", st.session_state.edit_text)
#     st.session_state.edit_text = edited

#     if st.button("🔁 Regenerate"):
#         st.session_state.messages = st.session_state.messages[:-2]
#         st.session_state.messages.append({"role": "user", "content": edited})
#         st.session_state.edit_mode = False
#         st.session_state.followup = edited
#         st.rerun()

# # normal input
# else:
#     new_input = st.chat_input("Ask coding questions...")
#     if new_input:
#         user_input = new_input


# # ==============================
# # 💬 PROCESS
# # ==============================
# if user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     with st.chat_message("assistant"):
#         response = chat(user_input, st.session_state.messages[:-1])
#         st.markdown(response)

#     st.session_state.messages.append({"role": "assistant", "content": response})

#     st.session_state.followups = [
#         "Explain more?",
#         "Show example?",
#         "Optimize solution?"
#     ]


# # ==============================
# # 💬 FOLLOWUPS (FIXED — AFTER PROCESS)
# # ==============================
# if st.session_state.followups:
#     st.markdown('<div class="suggestion-box">', unsafe_allow_html=True)
#     st.markdown('<div class="suggestion-title">💬 Suggestions</div>', unsafe_allow_html=True)

#     cols = st.columns(3)

#     for i, q in enumerate(st.session_state.followups):
#         if cols[i].button(q, key=f"f_{i}_{len(st.session_state.messages)}"):
#             st.session_state.followup = q
#             st.rerun()

#     st.markdown('</div>', unsafe_allow_html=True)

# Above this code the code was built on DeepSeek(Ollama)
###################################################################################################################################
#import streamlit as st
#import requests
#from PyPDF2 import PdfReader

#OLLAMA_URL = "http://localhost:11434/api/generate"

# ==============================
# ⚙ Page Setup
# ==============================
#st.set_page_config(
#    page_title="CodeStore Coder Bot",
#    page_icon="🤖",
#    layout="centered"
#)

#st.title("🤖 CodeStore Coder Bot")
#st.caption("Powered by Ollama (DeepSeek) • Built by CodeStore Team")

# ==============================
# 🎨 Floating Follow-up CSS
# ==============================
#st.markdown("""
#<style>
#.followup-container {
#    position: fixed;
#   bottom: 120px;
#    right: 25px;
#    width: 260px;
#    background: #1e1e1e;
#    border: 1px solid #333;
#    border-radius: 14px;
#    padding: 12px;
#    z-index: 999;
#    box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
#}
#.followup-title {
#    font-size: 14px;
#    margin-bottom: 8px;
#    color: #ccc;
#}
#</style>
#""", unsafe_allow_html=True)

# ==============================
# 📂 Sidebar
# ==============================
#with st.sidebar:
#    st.header("📂 Upload")

#    uploaded_file = st.file_uploader(
#        "Upload",
#        type=["pdf", "png", "jpg", "jpeg"],
#        label_visibility="collapsed"
#    )

#    st.markdown("---")

#    st.markdown(
#        """
#        <div style='text-align:center; font-size:14px; color:gray;'>
#            Made with ❤️<br>
#            <b>CodeStore Coder</b><br>
#            <span style='font-size:12px;'>Developed by CodeStore Team</span>
#        </div>
#        """,
#        unsafe_allow_html=True
#    )

# ==============================
## 🧠 Session State
# ==============================
#if "messages" not in st.session_state:
#    st.session_state.messages = []

#if "followups" not in st.session_state:
#    st.session_state.followups = []

#if "show_followup" not in st.session_state:
#    st.session_state.show_followup = False

# ==============================
# 📄 PDF Extract
# ==============================
#def extract_pdf_text(file):
#    reader = PdfReader(file)
#    text = ""
#    for page in reader.pages:
#        text += page.extract_text() or ""
#    return text[:2000]

# ==============================
# 🤖 Chat Function
# ==============================
#def chat(message, history, file):
#    system_prompt = """You are a strict coding assistant.

#Rules:
#- No unnecessary greetings
#- Give direct technical answers
#- Use bullet points
#- Use proper code blocks (```language)
#"""

#    prompt = system_prompt

#    if file:
#        try:
#            if file.name.endswith(".pdf"):
#                prompt += extract_pdf_text(file)
#        except:
#            pass

#    for msg in history:
#        prompt += f"{msg['role']}: {msg['content']}\n"

#    prompt += f"user: {message}\nassistant:"

#    try:
#        res = requests.post(
#            OLLAMA_URL,
#            json={
#                "model": "deepseek-coder",
#                "prompt": prompt,
#                "stream": False
#            },
#            timeout=60
#        )
#        return res.json().get("response", "No response")
#    except:
#        return "⚠️ Error connecting to model. Try again."

# ==============================
# 🧠 Follow-up Generator
# ==============================
#def generate_followups(question, answer):
#    prompt = f"""
#Generate EXACTLY 3 short follow-up questions.

#Question: {question}
#Answer: {answer}

#Rules:
#- Max 10 words each
#- No explanations
#- One per line
#"""

#    try:
#        res = requests.post(
#            OLLAMA_URL,
#            json={
#                "model": "deepseek-coder",
 #               "prompt": prompt,
#                "stream": False
#            },
#            timeout=60
#        )

#        text = res.json().get("response", "")

#        lines = [
#            line.strip("- ").strip()
#            for line in text.split("\n")
#            if line.strip() and len(line.strip()) < 80
#        ]

#        return lines[:3]

#    except:
#        return ["Explain more?", "Show example?", "Optimize code?"]

# ==============================
# 💬 Display Chat
# ==============================
#for msg in st.session_state.messages:
#    with st.chat_message(msg["role"]):
#        st.markdown(msg["content"])

# ==============================
# 💬 Input Handling
# ==============================
#if "followup" in st.session_state:
#    user_input = st.session_state.followup
#    del st.session_state.followup
#else:
#    user_input = st.chat_input("Ask coding questions...")

# ==============================
# 💬 Handle Query
# ==============================
#if user_input:
#    st.session_state.messages.append({"role": "user", "content": user_input})

#    with st.chat_message("user"):
 #       st.markdown(user_input)

 #   with st.chat_message("assistant"):
 #       with st.spinner("Thinking..."):
 #           response = chat(
#                user_input,
#                st.session_state.messages[:-1],
#                uploaded_file
#            )
#            st.markdown(response)

#    st.session_state.messages.append({"role": "assistant", "content": response})

    # Generate followups
#    followups = generate_followups(user_input, response)
#    st.session_state.followups = followups
#    st.session_state.last_query = user_input   # 🔥 IMPORTANT
#    st.session_state.show_followup = True
   
#    st.session_state.last_query = user_input

# ==============================
# 💬 Follow-up Suggestions (RIGHT SIDE + FLOATING)
# ==============================
#if st.session_state.show_followup and st.session_state.followups:

#    st.markdown('<div class="followup-container">', unsafe_allow_html=True)
#    st.markdown('<div class="followup-title">💬 Suggestions</div>', unsafe_allow_html=True)

#    for i, q in enumerate(st.session_state.followups[:3]):
#        unique_key = f"followup_{i}_{st.session_state.get('last_query','')}_{len(st.session_state.messages)}"

#    if st.button(q, key=unique_key):
#        st.session_state.followup = q
#        st.session_state.show_followup = False  # hide old suggestions
#        st.rerun()
#    st.markdown('</div>', unsafe_allow_html=True)

# Above this code is by Deep-Seek Coder
############################################################################################################################################
# Below this code is by Groq

import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

# ==============================
# 🔐 Load API Key
# ==============================
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ==============================
# ⚙ Page Setup
# ==============================
st.set_page_config(
    page_title="CodeStore Coder Bot",
    page_icon="🤖",
    layout="centered"
)

# ==============================
# 🎨 FIXED HEADER (LIKE KIMI)
# ==============================
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center;">
    <h1>🤖 CodeStore Coder Bot</h1>
    <p style="color: gray;">
        CodeStore AI Assistant • Built by CodeStore Team
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================
# 🧠 Session State
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "followups" not in st.session_state:
    st.session_state.followups = []

if "show_followup" not in st.session_state:
    st.session_state.show_followup = False

# ==============================
# 📂 Sidebar (UPGRADED)
# ==============================
with st.sidebar:

    # 🔥 Fixed Heading
    st.markdown(
        "<h2 style='font-weight:700;'>🤖 CodeStore Bot</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # 🔥 Controls
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.session_state.followups = []
        st.session_state.show_followup = False
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.followups = []
        st.session_state.show_followup = False
        st.rerun()

    st.markdown("---")

    # 🔥 Upload
    st.header("📂 Upload")

    uploaded_file = st.file_uploader(
        "Upload",
        type=["pdf", "png", "jpg", "jpeg"],
        label_visibility="collapsed",
        key="file_upload"
    )

# ==============================
# 📄 PDF Extract
# ==============================
def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text[:2000]

# ==============================
# 🤖 Greeting Detection
# ==============================
def is_greeting(text):
    greetings = ["hi", "hello", "hey"]
    words = text.lower().split()
    return any(word in greetings for word in words[:2])
# ==============================
# 🤖 Chat Function
# ==============================
def chat(messages):

    system_prompt = """You are a professional coding assistant developed by CodeStore.

- Greet the user if they greet you.
- Help with coding, debugging, and development.
- Provide clean answers with code blocks.
"""

    msgs = [{"role": "system", "content": system_prompt}]

    if uploaded_file and uploaded_file.name.endswith(".pdf"):
        try:
            msgs.append({"role": "system", "content": extract_pdf_text(uploaded_file)})
        except:
            pass

    msgs.extend(messages)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=msgs,
        temperature=0.7
    )

    return response.choices[0].message.content

# ==============================
# 🧠 Follow-ups
# ==============================
def generate_followups(question, answer):

    prompt = f"""
Generate EXACTLY 3 short follow-up questions.

Question: {question}
Answer: {answer}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        text = response.choices[0].message.content

        return [
            line.strip("- ").strip()
            for line in text.split("\n")
            if line.strip()
        ][:3]

    except:
        return ["Explain more?", "Show example?", "Optimize code?"]

# ==============================
# 💬 Display Chat
# ==============================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================
# 💬 Input (Clean like yours)
# ==============================
user_input = st.chat_input("Ask coding questions...")

if "followup" in st.session_state:
    user_input = st.session_state.followup
    del st.session_state.followup

# ==============================
# 💬 Handle Query
# ==============================
if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    if is_greeting(user_input):
        response = """👋 Hello!

I'm your technical assistant developed by CodeStore.

Ask me anything about coding 🚀
"""
        with st.chat_message("assistant"):
            st.markdown(response)
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
                st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.session_state.followups = generate_followups(user_input, response)
    st.session_state.show_followup = True

# ==============================
# 💬 Follow-ups
# ==============================
if st.session_state.show_followup and st.session_state.followups:

    st.markdown("💬 Suggestions")

    for q in st.session_state.followups:
        if st.button(q):
            st.session_state.followup = q
            st.session_state.show_followup = False
            st.rerun()
