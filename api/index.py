from fastapi import FastAPI, HTTPException
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
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@app.post("/api/index")
def shorten_url(item: URLItem):
    if not item.longUrl:
        raise HTTPException(status_code=400, detail="Invalid URL")
    
    short_id = generate_short_id()
    url_db[short_id] = item.longUrl
    return {"shortId": short_id}

@app.get("/api/index")
def handle_redirect(q: str = None):
    if q and q in url_db:
        return RedirectResponse(url=url_db[q])
    elif q:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"message": "API status: Active"}
