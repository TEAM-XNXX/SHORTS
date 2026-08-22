from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import string
import random

app = FastAPI()

# মেমোরি ডাটাবেজ
url_db = {}

class URLItem(BaseModel):
    longUrl: str

def generate_short_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8)) # ৮ অক্ষরের আইডি

@app.post("/api/index")
def shorten_url(item: URLItem):
    if not item.longUrl:
        raise HTTPException(status_code=400, detail="Invalid URL")
    
    short_id = generate_short_id()
    url_db[short_id] = item.longUrl
    
    return {"shortId": short_id}

# মূল ডোমেইনে হিট করলে এবং কুয়েরি প্যারামিটার 'q' থাকলে রিডাইরেক্ট হবে
@app.get("/")
def handle_root(q: str = None):
    if q and q in url_db:
        return RedirectResponse(url=url_db[q])
    elif q:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # কুয়েরি প্যারামিটার না থাকলে সাধারণ ইণ্ডেক্স বা মেসেজ দেখাবে
    return {"message": "Welcome to Shorts URL Shortener"}
