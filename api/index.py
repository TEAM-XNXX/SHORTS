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
CODE_LENGTH = 7


def valid_url(value):
    try:
        parsed = urlparse(value)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )
    except Exception:
        return False


def make_code():
    while True:
        code = "".join(
            secrets.choice(ALPHABET)
            for _ in range(CODE_LENGTH)
        )
        if code not in LINKS:
            return code


# সরাসরি পাইথনের ভেতরেই সম্পূর্ণ HTML ডিজাইন কোডটি ঢুকিয়ে দেওয়া হলো
HTML_PAGE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gshort.net · Free URL Shortener</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Roboto, sans-serif; }
        body { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .shortener-container { background: #ffffff; padding: 50px 40px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); width: 100%; max-width: 650px; text-align: center; }
        .brand-title { font-size: 36px; color: #1e293b; font-weight: 800; margin-bottom: 8px; letter-spacing: -1px; }
        .brand-title span { color: #2563eb; }
        .brand-subtitle { font-size: 15px; color: #64748b; margin-bottom: 35px; }
        .input-group { display: flex; gap: 10px; background: #f8fafc; padding: 8px; border-radius: 12px; border: 2px solid #e2e8f0; transition: border-color 0.2s; }
        .input-group:focus-within { border-color: #2563eb; background: #fff; }
        .input-group input { flex: 1; border: none; background: transparent; padding: 12px 15px; font-size: 16px; outline: none; color: #334155; }
        .btn-shorten { background: #2563eb; color: white; border: none; padding: 0 24px; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; transition: background 0.2s; white-space: nowrap; }
        .btn-shorten:hover { background: #1d4ed8; }
        .btn-shorten:disabled { background: #94a3b8; cursor: not-allowed; }
        .result-container { margin-top: 30px; padding: 20px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; text-align: left; }
        .result-label { font-size: 14px; color: #166534; font-weight: 600; margin-bottom: 8px; }
        .result-field { display: flex; gap: 10px; }
        .result-field input { flex: 1; padding: 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 15px; background: #fff; color: #1e293b; font-weight: 500; }
        .btn-copy { background: #10b981; color: white; border: none; padding: 0 20px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
        .btn-copy:hover { background: #059669; }
        .success-text { font-size: 13px; color: #15803d; margin-top: 6px; font-weight: 500; }
        .hidden { display: none !important; }
        .footer-links { margin-top: 40px; font-size: 13px; color: #94a3b8; }
        .footer-links a { color: #64748b; text-decoration: none; margin: 0 5px; }
        .copyright { margin-top: 15px; font-size: 12px; }
        @media (max-width: 500px) {
            .input-group { flex-direction: column; background: transparent; border: none; padding: 0; }
            .input-group input { background: #fff; border: 2px solid #e2e8f0; border-radius: 12px; margin-bottom: 10px; }
            .btn-shorten { padding: 14px; border-radius: 12px; }
        }
    </style>
</head>
<body>
    <div class="shortener-container">
        <h1 class="brand-title">Gshort<span>.net</span></h1>
        <p class="brand-subtitle">আপনার বড় লিঙ্কগুলোকে মুহূর্তেই ছোট এবং সচল করুন।</p>
        <div class="shortener-form">
            <div class="input-group">
                <input type="url" id="long-url" placeholder="এখানে আপনার বড় লিঙ্কটি পেস্ট করুন..." required>
                <button id="shorten-btn" class="btn-shorten">Shorten URL</button>
            </div>
        </div>
        <div id="result-box" class="result-container hidden">
            <p class="result-label">আপনার সচল শর্ট লিঙ্ক তৈরি হয়েছে:</p>
            <div class="result-field">
                <input type="text" id="shortened-url" readonly value="">
                <button id="copy-btn" class="btn-copy">Copy</button>
            </div>
            <p id="copy-success" class="success-text hidden">✓ লিঙ্কটি কপি হয়েছে!</p>
        </div>
        <div class="footer-links">
            <a href="#">Privacy</a> • <a href="#">Terms</a> • <a href="#">Report Abuse</a>
            <p class="copyright">© 2026 Gshort.net</p>
        </div>
    </div>
    <script>
        const API = window.location.origin;
        document.getElementById('shorten-btn').addEventListener('click', function() {
            const longUrl = document.getElementById('long-url').value.trim();
            const shortenBtn = document.getElementById('shorten-btn');
            const resultBox = document.getElementById('result-box');
            const shortenedUrlField = document.getElementById('shortened-url');
            const copySuccess = document.getElementById('copy-success');

            if (longUrl === "") { alert("দয়া করে একটি সঠিক লিঙ্ক প্রদান করুন।"); return; }
            shortenBtn.innerText = "Shortening...";
            shortenBtn.disabled = true;
            copySuccess.classList.add('hidden');

            fetch(API + "/api/shorten", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: longUrl })
            })
            .then(response => {
                if (!response.ok) { return response.json().then(err => { throw new Error(err.error || 'Error'); }); }
                return response.json();
            })
            .then(data => {
                if (data.ok && data.short_url) {
                    resultBox.classList.remove('hidden');
                    shortenedUrlField.value = data.short_url;
                } else { throw new Error('Invalid response'); }
            })
            .catch(error => { console.error("Error:", error); alert(error.message || "লিঙ্কটি তৈরি করতে সমস্যা হয়েছে।"); })
            .finally(() => { shortenBtn.innerText = "Shorten URL"; shortenBtn.disabled = false; });
        });

        document.getElementById('copy-btn').addEventListener('click', function() {
            const shortenedUrlField = document.getElementById('shortened-url');
            const copySuccess = document.getElementById('copy-success');
            if (shortenedUrlField.value !== "") {
                navigator.clipboard.writeText(shortenedUrlField.value)
                    .then(() => { copySuccess.classList.remove('hidden'); })
                    .catch(err => { console.error("Copy failed: ", err); });
            }
        });
    </script>
</body>
</html>
"""


@app.get("/")
def home():
    # সরাসরি এইচটিএমএল স্ট্রিং রেসপন্স হিসেবে পাঠানো হচ্ছে
    return HTML_PAGE


@app.get("/health")
def health():
    return jsonify({"ok": True})


@app.post("/api/shorten")
def shorten():
    data = request.get_json(silent=True) or {}
    target = str(data.get("url", "")).strip()

    if not valid_url(target):
        return jsonify({
            "ok": False,
            "error": "Enter a valid http:// or https:// URL."
        }), 400

    code = make_code()

    LINKS[code] = {
        "url": target,
        "clicks": 0
    }

    base = request.host_url.rstrip("/")
    short_url = f"{base}/r/{code}"

    return jsonify({
        "ok": True,
        "code": code,
        "url": target,
        "short_url": short_url
    })


@app.get("/r/<code>")
def redirect_link(code):
    item = LINKS.get(code)

    if not item:
        return "Short link not found.", 404

    item["clicks"] += 1

    return redirect(
        item["url"],
        code=302
    )


@app.get("/api/link/<code>")
def link_info(code):
    item = LINKS.get(code)

    if not item:
        return jsonify({
            "ok": False,
            "error": "Short link not found."
        }), 404

    return jsonify({
        "ok": True,
        "code": code,
        "url": item["url"],
        "clicks": item["clicks"]
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000"))
    )
