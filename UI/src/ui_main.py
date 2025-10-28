import os
import time
import uuid

import gradio as gr
import requests
from dotenv import load_dotenv

load_dotenv()


AGENT_URL_BASE = os.environ.get("AGENT_URL_BASE")

if not AGENT_URL_BASE:
    raise ValueError("The AGENT_URL_BASE environment variable is not set.")


user_id = None
session_id = None
last_user_message = None


def init_session():
    global user_id
    global session_id
    print("Starting session...")

    user_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())

    r = requests.post(
        f"{AGENT_URL_BASE}/apps/barista_agent/users/{user_id}/sessions/{session_id}"
    )

    r.raise_for_status()

    print("Session started!")


def run():
    request_json = {
        "appName": "barista_agent",
        "userId": user_id,
        "sessionId": session_id,
        "newMessage": {"role": "user", "parts": [{"text": last_user_message}]},
    }

    text = ""

    try:
        response_service = requests.post(f"{AGENT_URL_BASE}/run", json=request_json)

        response_service.raise_for_status()
        print(response_service.json())
        num_responses = len(response_service.json())

        if num_responses > 0:
            for content in response_service.json():
                if "text" in content["content"]["parts"][0]:
                    text = text + " " + content["content"]["parts"][0]["text"]
    except Exception as e:
        return "Error => " + str(e) + "\n\n Try again!"

    return text


with gr.Blocks(gr.themes.Soft()) as demo:
    chatbot = gr.Chatbot(type="messages", height="70vh")
    msg = gr.Textbox(label="What do you need?")
    clear = gr.Button("Clear Messages")
    new_session = gr.Button("Create new session (when you have a problem)")

    def user(user_message, history: list):
        global last_user_message
        last_user_message = user_message
        return "", history + [{"role": "user", "content": user_message}]

    def bot(history: list):
        bot_message = run()
        history.append({"role": "assistant", "content": ""})
        for character in bot_message:
            history[-1]["content"] += character
            time.sleep(0.003)
            yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)
    new_session.click(init_session, None, chatbot, queue=False)


if __name__ == "__main__":
    init_session()
    demo.launch(server_name="0.0.0.0", server_port=8080)
    # demo.launch()
