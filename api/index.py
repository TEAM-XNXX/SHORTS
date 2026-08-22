import os
import secrets
import string
from urllib.parse import urlparse

from flask import Flask, jsonify, request, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# টেস্ট করার জন্য স্ক্রিনশটের মতো ১টি লিঙ্ক আগে থেকেই মেমোরিতে রাখা হলো
LINKS = {
    "qLf0aM3hhImkBEBfG": {
        "url": "https://derisivepageant.com...",
        "clicks": 5901,
        "date": "Aug 20, 2026",
        "title": "XYZ FF"
    }
}

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 17  # স্ক্রিনশট অনুযায়ী কোড একটু বড় করা হয়েছে


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


# নতুন প্রিমিয়াম অ্যাডভান্সড ড্যাশবোর্ড UI
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gshort · Simple Link Workspace</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { background-color: #f4f6fa; color: #333; padding-bottom: 40px; }
        
        /* নেভিগেশন বার */
        .navbar { display: flex; justify-content: space-between; align-items: center; background: white; padding: 12px 6%; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .nav-left { display: flex; align-items: center; gap: 20px; }
        .menu-btn { background: none; border: none; font-size: 20px; cursor: pointer; color: #666; }
        .logo { display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 22px; color: #1a1a1a; text-decoration: none; }
        .logo-icon { background: #0066cc; color: white; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; border-radius: 10px; font-size: 18px; }
        .logo span { color: #8a2be2; }
        .nav-tabs { display: flex; gap: 10px; }
        .tab-btn { background: #eef2ff; border: 1px solid #e0e7ff; padding: 8px 16px; border-radius: 20px; font-weight: 600; color: #312e81; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 6px; }
        .nav-right { display: flex; align-items: center; gap: 15px; color: #666; }
        .nav-right-btn { background: none; border: 1px solid #e5e7eb; width: 38px; height: 38px; border-radius: 10px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 16px; color: #4b5563; }

        /* মেইন কন্টেন্ট */
        .workspace-container { max-width: 800px; margin: 50px auto 0; padding: 0 20px; }
        .hero-section { text-align: center; margin-bottom: 35px; }
        .hero-tag { font-size: 12px; font-weight: 700; color: #0066cc; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 10px; }
        .hero-title { font-size: 32px; font-weight: 700; color: #111827; margin-bottom: 12px; }
        .hero-subtitle { font-size: 15px; color: #6b7280; }

        /* ইনপুট বক্স */
        .search-box-wrapper { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); margin-bottom: 30px; }
        .input-group { display: flex; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 16px; padding: 6px 10px; align-items: center; }
        .input-group input { flex: 1; border: none; background: transparent; padding: 14px 10px; font-size: 15px; outline: none; color: #374151; }
        .btn-shorten { background: #0066cc; color: white; border: none; width: 44px; height: 44px; border-radius: 12px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 18px; transition: background 0.2s; }
        .btn-shorten:hover { background: #0052a3; }
        .advanced-opt { margin-top: 15px; display: flex; align-items: center; gap: 8px; font-size: 14px; color: #4b5563; font-weight: 500; cursor: pointer; width: max-content; }
        .advanced-opt input { cursor: pointer; width: 16px; height: 16px; }

        /* লিঙ্ক ম্যানেজমেন্ট ড্যাশবোর্ড */
        .management-box { background: white; border-radius: 20px; padding: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); }
        .manage-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f3f4f6; padding-bottom: 15px; margin-bottom: 20px; }
        .manage-title { font-size: 12px; font-weight: 700; color: #0066cc; letter-spacing: 1px; text-transform: uppercase; }
        .total-stats { font-size: 15px; font-weight: 500; color: #4b5563; }
        .total-stats span { font-weight: 700; font-size: 24px; color: #111827; margin-right: 4px; }

        /* স্ট্যাটাস বার */
        .status-bar { display: flex; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 12px; padding: 15px 20px; margin-bottom: 25px; }
        .status-item { flex: 1; }
        .status-title { font-size: 14px; font-weight: 600; color: #0066cc; margin-bottom: 6px; }
        .status-sub { font-size: 13px; color: #6b7280; font-weight: 500; }
        .progress-line { height: 4px; background: #e5e7eb; border-radius: 2px; margin-top: 10px; position: relative; overflow: hidden; }
        .progress-fill { position: absolute; left: 0; top: 0; height: 100%; width: 10%; background: #0066cc; border-radius: 2px; }

        /* লিঙ্ক লিস্ট আইটেম */
        .link-list { display: flex; flex-direction: column; gap: 20px; }
        .link-card { background: white; border: 1px solid #f0f2f5; border-radius: 14px; padding: 5px 0; }
        .card-row-top { display: flex; align-items: flex-start; gap: 15px; margin-bottom: 15px; position: relative; }
        .card-icon { width: 36px; height: 36px; background: #f3f4f6; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 16px; color: #4b5563; margin-top: 2px; }
        .card-details { flex: 1; overflow: hidden; }
        .card-url-original { font-size: 15px; color: #0066cc; font-weight: 600; text-decoration: none; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 4px; }
        .card-meta { font-size: 12px; color: #9ca3af; font-weight: 500; }
        .card-meta span { margin-right: 10px; }
        
        .card-row-bottom { display: flex; justify-content: space-between; align-items: center; background: #fafbfc; border-top: 1px solid #f3f4f6; padding: 12px 15px; border-radius: 0 0 14px 14px; }
        .google-link-wrapper { display: flex; align-items: center; gap: 8px; flex: 1; overflow: hidden; }
        .g-logo { color: #ea4335; font-size: 16px; font-weight: 700; }
        .card-url-short { font-size: 14px; color: #111827; font-weight: 600; text-decoration: none; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .btn-copy-card { background: none; border: none; font-size: 13px; font-weight: 600; color: #4b5563; cursor: pointer; padding: 4px 8px; border-radius: 6px; }
        .btn-copy-card:hover { background: #f3f4f6; }
        
        .card-stats-views { text-align: right; min-width: 80px; }
        .views-count { font-size: 18px; font-weight: 700; color: #111827; }
        .views-label { font-size: 11px; color: #9ca3af; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }

        /* কার্ড অ্যাকশন বাটনসমূহ */
        .card-actions { display: flex; gap: 8px; margin-top: 10px; padding: 0 15px 10px; }
        .action-btn { background: none; border: 1px solid #e5e7eb; width: 32px; height: 32px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 13px; color: #6b7280; transition: all 0.2s; }
        .action-btn:hover { background: #f9fafb; color: #111827; }
        .action-btn.delete:hover { background: #fef2f2; color: #ef4444; border-color: #fca5a5; }

        .hidden { display: none !important; }
    </style>
</head>
<body>

    <!-- টপ নেভিগেশন বার -->
    <div class="navbar">
        <div class="nav-left">
            <button class="menu-btn"><i class="fa-solid fa-bars"></i></button>
            <a href="#" class="logo"><div class="logo-icon">G</div>Gshort<span>.net</span></a>
            <div class="nav-tabs">
                <button class="tab-btn"><i class="fa-solid fa-link"></i> My links</button>
            </div>
        </div>
        <div class="nav-right">
            <button class="nav-right-btn"><i class="fa-regular fa-credit-card"></i></button>
            <button class="nav-right-btn"><i class="fa-solid fa-arrow-rotate-left"></i></button>
            <button class="nav-right-btn"><i class="fa-solid fa-gear"></i></button>
            <button class="nav-right-btn"><i class="fa-regular fa-circle-question"></i></button>
            <button class="nav-right-btn"><i class="fa-solid fa-arrow-right-from-bracket"></i></button>
            <button class="nav-right-btn"><i class="fa-regular fa-sun"></i></button>
        </div>
    </div>

    <!-- ওয়ার্কস্পেস কন্টেইনার -->
    <div class="workspace-container">
        <div class="hero-section">
            <p class="hero-tag">Gshort · Simple Link Workspace</p>
            <h1 class="hero-title">Create your short link</h1>
            <p class="hero-subtitle">Paste a destination, shorten it and manage everything below.</p>
        </div>

        <!-- শর্টনার ইনপুট বক্স -->
        <div class="search-box-wrapper">
            <div class="input-group">
                <input type="url" id="long-url" placeholder="https://example.com" required>
                <button id="shorten-btn" class="btn-shorten"><i class="fa-solid fa-scissors"></i></button>
            </div>
            <label class="advanced-opt">
