from config import SYSTEM_PROMPT


chat_history = [
    {"role":"system", "content":SYSTEM_PROMPT}
]


def add_user(text):

    chat_history.append({
        "role":"user",
        "content":text
    })


def add_assistant(text):

    chat_history.append({
        "role":"assistant",
        "content":text
    })


def get_history():

    return chat_history


def reset_chat():

    global chat_history

    chat_history = [
        {"role":"system", "content":SYSTEM_PROMPT}
    ]
