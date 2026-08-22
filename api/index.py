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


# আপনার স্ক্রিনশটের সাথে মিলিয়ে ১০০% নিখুঁত ডিজাইন এবং ইন্টিগ্রেটেড শর্টনার রেজাল্ট বক্স
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gshort · Fast URL Shortener</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { background-color: #f4f6fa; color: #333; padding-bottom: 60px; }
        
        /* নেভিগেশন বার */
        .navbar { display: flex; justify-content: space-between; align-items: center; background: white; padding: 15px 6%; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }
        .logo { display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 24px; color: #111827; text-decoration: none; }
        .logo-icon { background: #0066cc; color: white; width: 38px; height: 38px; display: flex; align-items: center; justify-content: center; border-radius: 12px; font-size: 20px; font-weight: 800; }
        .logo span { color: #8a2be2; }
        
        .nav-right { display: flex; align-items: center; gap: 20px; }
        .nav-link { color: #4b5563; text-decoration: none; font-size: 14px; font-weight: 600; }
        .btn-login { background: #0066cc; color: white; border: none; padding: 10px 20px; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; }
        .btn-register { color: #0066cc; text-decoration: none; font-size: 14px; font-weight: 600; }
        .theme-btn { background: none; border: none; font-size: 16px; color: #6b7280; cursor: pointer; }

        /* মেইন কন্টেন্ট */
        .workspace-container { max-width: 800px; margin: 60px auto 0; padding: 0 20px; text-align: center; }
        .hero-tag { font-size: 12px; font-weight: 700; color: #0066cc; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 15px; }
        .hero-title { font-size: 40px; font-weight: 800; color: #0f172a; margin-bottom: 16px; letter-spacing: -1px; }
        .hero-subtitle { font-size: 16px; color: #64748b; max-width: 600px; margin: 0 auto 35px; line-height: 1.6; }

        /* ইনপুট বক্স */
        .search-box-wrapper { background: white; padding: 25px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.02); margin-bottom: 40px; text-align: left; border: 1px solid #f1f5f9; }
        .input-group { display: flex; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 6px 10px; align-items: center; }
        .input-group input { flex: 1; border: none; background: transparent; padding: 14px 10px; font-size: 16px; outline: none; color: #334155; }
        .btn-shorten { background: #0066cc; color: white; border: none; width: 46px; height: 46px; border-radius: 12px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 20px; transition: background 0.2s; }
        .btn-shorten:hover { background: #0052a3; }
        .advanced-opt { margin-top: 15px; display: flex; align-items: center; gap: 8px; font-size: 14px; color: #64748b; font-weight: 500; cursor: pointer; width: max-content; }
        .advanced-opt input { cursor: pointer; width: 16px; height: 16px; }

        /* ৪টি স্ট্যাটাস্টিকস কার্ড গ্রিড */
        .stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 35px; }
        .stats-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.01); border: 1px solid #f1f5f9; }
        .stats-number { font-size: 32px; font-weight: 800; color: #0066cc; margin-bottom: 6px; letter-spacing: -0.5px; }
        .stats-label { font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }

        /* ফিচার ইন্ডিকেটর ডট */
        .feature-indicators { display: flex; justify-content: center; gap: 20px; margin-bottom: 50px; flex-wrap: wrap; }
        .indicator-item { display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 600; color: #4b5563; }
        .dot { width: 8px; height: 8px; background-color: #10b981; border-radius: 50%; display: inline-block; }

        /* লিঙ্ক লিস্ট কন্টেইনার (লুকানো থাকবে, লিঙ্ক তৈরি হলে ভেসে উঠবে) */
        .management-box { background: white; border-radius: 24px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.02); text-align: left; border: 1px solid #f1f5f9; margin-top: 20px; animation: fadeIn 0.4s ease-out; }
        .manage-title { font-size: 14px; font-weight: 700; color: #0066cc; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 20px; }
        .link-list { display: flex; flex-direction: column; gap: 20px; }
        
        /* লিঙ্ক কার্ড ডিজাইন */
        .link-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; overflow: hidden; }
        .card-top { padding: 20px; display: flex; align-items: flex-start; gap: 15px; }
        .card-icon { width: 38px; height: 38px; background: #f1f5f9; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 16px; color: #4b5563; }
        .card-details { flex: 1; overflow: hidden; }
        .card-url-original { font-size: 15px; color: #0066cc; font-weight: 600; text-decoration: none; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 4px; }
        .card-meta { font-size: 12px; color: #94a3b8; font-weight: 500; }
        
        .card-actions { display: flex; gap: 8px; padding: 0 20px 15px; }
        .action-btn { background: none; border: 1px solid #e2e8f0; width: 32px; height: 32px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 13px; color: #64748b; }
        .action-btn:hover { background: #f8fafc; color: #111827; }
        .action-btn.delete:hover { background: #fef2f2; color: #ef4444; border-color: #fca5a5; }
        
        .card-bottom { display: flex; justify-content: space-between; align-items: center; background: #f8fafc; border-top: 1px solid #e2e8f0; padding: 15px 20px; }
        .google-link-wrapper { display: flex; align-items: center; gap: 8px; flex: 1; overflow: hidden; }
        .g-logo { color: #ea4335; font-size: 15px; }
        .card-url-short { font-size: 14px; color: #1e293b; font-weight: 600; text-decoration: none; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .btn-copy-card { background: white; border: 1px solid #cbd5e1; font-size: 12px; font-weight: 600; color: #475569; cursor: pointer; padding: 5px 10px; border-radius: 6px; margin-left: 5px; }
        .btn-copy-card:hover { background: #f1f5f9; }
        
        .card-stats-views { text-align: right; min-width: 80px; }
        .views-count { font-size: 20px; font-weight: 800; color: #0f172a; line-height: 1.2; }
        .views-label { font-size: 10px; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }

        /* ফুটার লিঙ্ক */
        .footer-links { margin-top: 60px; font-size: 13px; color: #94a3b8; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; border-top: 1px solid #e2e8f0; padding-top: 20px; }
        .footer-links a { color: #0066cc; text-decoration: none; }

        .hidden { display: none !important; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        @media (max-width: 600px) { .stats-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>

    <!-- টপ নেভিগেশন বার -->
    <div class="navbar">
        <a href="#" class="logo"><div class="logo-icon">G</div>Gshort<span>.net</span></a>
        <div class="nav-right">
            <a href="#" class="nav-link" style="margin-right: 10px;">Pricing</a>
            <button class="btn-login" style="margin-right: 10px;">Log in</button>
            <a href="#" class="btn-register" style="margin-right: 15px;">Register</a>
            <button class="theme-btn"><i class="fa-regular fa-sun"></i></button>
        </div>
    </div>

    <!-- মূল ল্যান্ডিং কন্টেইনার -->
    <div class="workspace-container">
        <p class="hero-tag">Gshort · Fast URL Shortener</p>
        <h1 class="hero-title">Shorten links. Share smarter.</h1>
        <p class="hero-subtitle">Create fast, reliable short URLs, manage every destination and track lifetime clicks from one simple dashboard.</p>

        <!-- শর্টনার ইনপুট বক্স -->
        <div class="search-box-wrapper">
            <div class="input-group">
                <input type="url" id="long-url" placeholder="https://example.com" required>
                <button id="shorten-btn" class="btn-shorten"><i class="fa-solid fa-scissors"></i></button>
            </div>
            <label class="advanced-opt">
                <input type="checkbox"> Advanced options
            </label>
        </div>

        <!-- ৪টি স্ট্যাটাস্টিকস কার্ড গ্রিড -->
        <div class="stats-grid">
            <div class="stats-card">
                <p class="stats-number">131.8M</p>
                <p class="stats-label">Links</p>
            </div>
            <div class="stats-card">
                <p class="stats-number">1.6B</p>
                <p class="stats-label">Clicks</p>
