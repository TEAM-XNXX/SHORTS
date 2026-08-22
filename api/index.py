import os
import secrets
import string
from urllib.parse import urlparse
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

LINKS = {}
ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 17

def valid_url(value):
    try:
        parsed = urlparse(value)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False

def make_code():
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))
        if code not in LINKS:
            return code

@app.post("/api/shorten")
def shorten():
    data = request.get_json(silent=True) or {}
    target = str(data.get("url", "")).strip()

    if not valid_url(target):
        return jsonify({"ok": False, "error": "Enter a valid http:// or https:// URL."}), 400

    code = make_code()
    LINKS[code] = {"url": target, "clicks": 0}
    google_fake_url = f"https://google.com{code}"

    return jsonify({"ok": True, "code": code, "url": target, "short_url": google_fake_url})

@app.get("/r/<code>")
def redirect_link(code):
    item = LINKS.get(code)
    if not item:
        return "Short link not found.", 404
    item["clicks"] += 1
    return redirect(item["url"], code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
