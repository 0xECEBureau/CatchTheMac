"""Flask app for the XSS challenge.
A background thread (bot) checks the latest message every 15 s and, if it
was not written by the bot, replies with "yes you are". Messages are stored
as a list of dicts with `author` and `text` keys so they can be rendered
with attribution in the UI.
"""
import base64
import threading
import time
from flask import Flask, request, make_response, render_template, jsonify

app = Flask(__name__)

# Message store: list of {author,text}
messages: list[dict] = []
lock = threading.Lock()

# ── Background bot that replies ------------------------------------------------

def bot_loop():
    while True:
        time.sleep(15)
        with lock:
            if messages and messages[-1]["author"] != "bot":
                messages.append({"author": "bot", "text": "yes you are"})

threading.Thread(target=bot_loop, daemon=True).start()

# ── Routes ---------------------------------------------------------------------

@app.route("/")
def index():
    role_cookie = request.cookies.get("role", "ZHVtYg==")  # "dumb" par défaut
    resp = make_response(render_template("index.html"))
    resp.set_cookie("role", role_cookie, httponly=False, samesite="Lax")
    return resp

@app.route("/post", methods=["POST"])
def post():
    role_cookie = request.cookies.get("role", "ZHVtYg==")
    try:
        role = base64.b64decode(role_cookie).decode(errors="ignore")
    except Exception:
        role = "dumb"
    with lock:
        messages.append({"author": "user", "text": f"I am {role}"})
    return jsonify(ok=True)

@app.route("/chat")
def chat():
    with lock:
        return jsonify(messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)