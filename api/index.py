import os
import secrets
import string
from urllib.parse import urlparse

from flask import Flask, jsonify, request, redirect, render_template
from flask_cors import CORS

# Vercel এর জন্য নিখুঁত টেমপ্লেট পাথ কনফিগারেশন
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, '..', 'templates')
app = Flask(__name__, template_folder=template_dir)
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


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({
        "ok": True
    })


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
        if code not in LINKS:
            return code


# এখন কেউ আপনার মেইন সাইটে (/) ভিজিট করলে সরাসরি সুন্দর ডিজাইন বা index.html দেখতে পাবে
@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({
        "ok": True
    })


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


@app.get("/")
def home():

    return jsonify({
        "ok": True,
        "service": "URL Shortener API",
        "version": "1.0"
    })


@app.get("/health")
def health():

    return jsonify({
        "ok": True
    })


@app.post("/api/shorten")
def shorten():

    data = request.get_json(
        silent=True
    ) or {}

    target = str(
        data.get("url", "")
    ).strip()


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

    short_url = (
        f"{base}/r/{code}"
    )


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

        return (
            "Short link not found.",
            404
        )


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

        port=int(
            os.environ.get(
                "PORT",
                "5000"
            )
        )

    )
