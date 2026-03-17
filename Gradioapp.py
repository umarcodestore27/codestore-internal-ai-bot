import gradio as gr
import requests
from PyPDF2 import PdfReader
import json  

OLLAMA_URL = "http://localhost:11434/api/generate"

# ---------------------------
# Extract PDF Text
# ---------------------------
def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text[:2000]


# ---------------------------
# Model Function
# ---------------------------
def chat(message, history, file):

    prompt = """You are an expert AI coding assistant.

Rules:
- Answer ONLY what the user asks
- Do NOT assume extra context
- Do NOT repeat previous answers
- If coding is required, give clean code only
"""

    # File context
    if file is not None:
        try:
            if file.name.endswith(".pdf"):
                prompt += extract_pdf_text(file)
            else:
                prompt += "\nUser uploaded an image.\n"
        except:
            pass

    # History
    for msg in history:
        if not msg.get("content"):
            continue

        if msg["role"] == "user":
            prompt += f"User: {msg['content']}\n"
        else:
            prompt += f"Assistant: {msg['content']}\n"

    prompt += f"User: {message}\nAssistant:"

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "deepseek-coder",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        data = response.json()

        return data.get("response", "⚠️ No valid response")

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


# ---------------------------
# UI
# ---------------------------
with gr.Blocks(css="""
#chat-container {height: 75vh; overflow-y: auto;}
#input-row {position: sticky; bottom: 0; background: #0b0f19; padding: 10px;}
button {height: 40px !important;}
""") as demo:

    gr.Markdown("# 🤖 CodeStore Internal Bot")

    chatbot = gr.Chatbot(elem_id="chat-container")

    with gr.Row(elem_id="input-row"):
        file = gr.File(scale=2, label="📎")

        msg = gr.Textbox(
            placeholder="Ask coding questions...",
            show_label=False,
            lines=1,
            scale=8
        )

        send = gr.Button("➤", scale=1)

    clear = gr.Button("🗑️ Clear Chat")

    # ---------------------------
    # Logic
    # ---------------------------
    def user_input(message, history):
        history = history or []
        history.append((message, ""))
        return "", history


    def bot_reply(history, file):
        try:
            if not history:
                return []

            user_message = history[-1][0]

            formatted_history = []
            for user, bot in history[:-1]:
                if user:
                    formatted_history.append({"role": "user", "content": user})
                if bot:
                    formatted_history.append({"role": "assistant", "content": bot})

            response = chat(user_message, formatted_history, file)

            if not isinstance(response, str):
                response = str(response)

            if not response.strip():
                response = "⚠️ Empty response"

            history[-1] = (user_message, response)

            return history

        except Exception as e:
            print("🔥 ERROR:", e)
            history[-1] = (history[-1][0], f"❌ ERROR: {str(e)}")
            return history


    # ---------------------------
    # Actions (✅ INSIDE BLOCK)
    # ---------------------------
    send.click(user_input, [msg, chatbot], [msg, chatbot]).then(
        bot_reply, [chatbot, file], chatbot
    )

    msg.submit(user_input, [msg, chatbot], [msg, chatbot]).then(
        bot_reply, [chatbot, file], chatbot
    )

    clear.click(lambda: [], None, chatbot)


# ---------------------------
# Launch
# ---------------------------
demo.launch(debug=True)