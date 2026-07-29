#!/usr/bin/env python3
"""
🌙 Modern Dark Translator - Web Version (FastAPI + HTMX)
Works on mobile, desktop, anywhere!
"""

import json
import time
import requests
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# ═══════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════

CONFIG_FILE = Path.home() / ".translator_config.json"
HISTORY_FILE = Path.home() / ".translator_history.json"
HISTORY_LIMIT = 100

LANGUAGES = {
    "auto": "🔍 تشخیص خودکار",
    "fa": "🇮🇷 فارسی",
    "en": "🇺🇸 English",
    "ar": "🇸🇦 العربية",
    "tr": "🇹🇷 Türkçe",
    "de": "🇩🇪 Deutsch",
    "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español",
    "ru": "🇷🇺 Русский",
    "zh": "🇨🇳 中文",
    "ja": "🇯🇵 日本語",
    "ko": "🇰🇷 한국어",
    "it": "🇮🇹 Italiano",
    "pt": "🇵🇹 Português",
    "hi": "🇮🇳 हिन्दी",
    "nl": "🇳🇱 Nederlands",
    "pl": "🇵🇱 Polski",
    "sv": "🇸🇪 Svenska",
}

# ═══════════════════════════════════════════════════════
# TRANSLATION BACKENDS
# ═══════════════════════════════════════════════════════

async def translate_libre(text: str, source: str, target: str) -> str:
    """LibreTranslate - free, open source"""
    try:
        url = "https://libretranslate.de/translate"
        data = {
            "q": text,
            "source": source if source != "auto" else "auto",
            "target": target,
            "format": "text"
        }
        r = requests.post(url, data=data, timeout=10)
        if r.status_code == 200:
            return r.json()["translatedText"]
    except:
        pass
    return None


async def translate_google(text: str, source: str, target: str) -> str:
    """Google Translate (free web endpoint)"""
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": source if source != "auto" else "auto",
            "tl": target,
            "dt": "t",
            "q": text
        }
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            result = r.json()
            # Google format: result[0][0][0] = translated text
            if (result and isinstance(result, list) and len(result) > 0 and
                result[0] and isinstance(result[0], list) and len(result[0]) > 0 and
                result[0][0] and isinstance(result[0][0], list) and len(result[0][0]) > 0):
                return result[0][0][0]
    except Exception as e:
        print(f"Google translate error: {e}")
    return None


async def translate_mymemory(text: str, source: str, target: str) -> str:
    """MyMemory Translation API"""
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"{source if source != 'auto' else 'auto'}|{target}"
        }
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            return r.json()["responseData"]["translatedText"]
    except:
        pass
    return None


TRANSLATORS = [
    ("Google", translate_google),
    ("LibreTranslate", translate_libre),
    ("MyMemory", translate_mymemory),
]


async def translate(text: str, source: str, target: str) -> tuple[str, str]:
    """Try multiple translators until one works"""
    if source == target:
        return text, "Same Language"
    
    for name, func in TRANSLATORS:
        try:
            result = await func(text, source, target)
            if result and result != text:
                return result, name
        except:
            continue
    
    return text, "Failed"


# ═══════════════════════════════════════════════════════
# HISTORY MANAGEMENT
# ═══════════════════════════════════════════════════════

def load_history():
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return []


def save_history(history):
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history[-HISTORY_LIMIT:], f, ensure_ascii=False, indent=2)
    except:
        pass


def add_history(text, translated, source, target, backend):
    history = load_history()
    history.insert(0, {
        "id": int(time.time() * 1000),
        "text": text[:500],
        "translated": translated[:500],
        "source": source,
        "target": target,
        "backend": backend,
        "time": datetime.now().strftime("%H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    save_history(history)


# ═══════════════════════════════════════════════════════
# FASTAPI APP
# ═══════════════════════════════════════════════════════

app = FastAPI(title="🌙 Dark Translator")

# ═══════════════════════════════════════════════════════
# FASTAPI APP
# ═══════════════════════════════════════════════════════

app = FastAPI(title="🌙 Dark Translator")

# Read HTML template at startup
with open("templates/index.html", "r") as f:
    HTML_TEMPLATE = f.read()

def render_template():
    """Simple template rendering - replace placeholders"""
    lang_options = ""
    for code, name in LANGUAGES.items():
        sel_src = ' selected' if code == 'auto' else ''
        sel_tgt = ' selected' if code == 'fa' else ''
        lang_options += f'<option value="{code}"{sel_src}>{name}</option>'
        lang_options += f'<option value="{code}"{sel_tgt}>{name}</option>'
    
    # This is a simple approach - we'll use string replacement
    return HTML_TEMPLATE.replace(
        '{% for code, name in LANGUAGES.items() %}<option value="{{ code }}" {% if code == \'auto\' %}selected{% endif %}>{{ name }}</option>{% endfor %}',
        ''.join([f'<option value="{code}"{" selected" if code=="auto" else ""}>{name}</option>' for code, name in LANGUAGES.items()])
    ).replace(
        '{% for code, name in LANGUAGES.items() %}<option value="{{ code }}" {% if code == \'fa\' %}selected{% endif %}>{{ name }}</option>{% endfor %}',
        ''.join([f'<option value="{code}"{" selected" if code=="fa" else ""}>{name}</option>' for code, name in LANGUAGES.items()])
    )

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    html = HTML_TEMPLATE
    # Replace source language options
    src_options = ''.join([f'<option value="{code}"{" selected" if code=="auto" else ""}>{name}</option>' for code, name in LANGUAGES.items()])
    tgt_options = ''.join([f'<option value="{code}"{" selected" if code=="fa" else ""}>{name}</option>' for code, name in LANGUAGES.items()])
    html = html.replace("{{SOURCE_OPTIONS}}", src_options)
    html = html.replace("{{TARGET_OPTIONS}}", tgt_options)
    return HTMLResponse(html)

@app.post("/translate")
async def translate_endpoint(
    text: str = Form(...),
    source: str = Form("auto"),
    target: str = Form("fa")
):
    # Fix encoding issue - decode from latin1 to utf-8 if needed
    try:
        text = text.encode('latin1').decode('utf-8')
        source = source.encode('latin1').decode('utf-8')
        target = target.encode('latin1').decode('utf-8')
    except:
        pass
    
    if not text.strip():
        return JSONResponse({"error": "Empty text"}, status_code=400)
    
    print(f"DEBUG: Translating '{text.strip()}' from {source} to {target}")
    translated, backend = await translate(text.strip(), source, target)
    print(f"DEBUG: Got '{translated}' from {backend}")
    
    if translated == text.strip() and backend != "Same Language":
        return JSONResponse({
            "error": "Translation failed",
            "original": text
        }, status_code=500)
    
    add_history(text.strip(), translated, source, target, backend)
    
    return JSONResponse({
        "translated": translated,
        "backend": backend,
        "source": source,
        "target": target
    })


@app.post("/swap")
async def swap_languages(source: str = Form(...), target: str = Form(...)):
    if source == "auto":
        return JSONResponse({"source": target, "target": "en"})
    return JSONResponse({"source": target, "target": source})


@app.get("/history")
async def get_history():
    return JSONResponse(load_history())


@app.delete("/history/{item_id}")
async def delete_history(item_id: int):
    history = load_history()
    history = [h for h in history if h["id"] != item_id]
    save_history(history)
    return JSONResponse({"ok": True})


@app.delete("/history")
async def clear_history():
    save_history([])
    return JSONResponse({"ok": True})


@app.post("/copy")
async def copy_text(text: str = Form(...)):
    # Client handles clipboard
    return JSONResponse({"ok": True})


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    # Create templates dir
    Path("templates").mkdir(exist_ok=True)
    Path("static").mkdir(exist_ok=True)
    
    # Railway sets PORT env var, default to 8080
    port = int(os.environ.get("PORT", 8080))
    
    print(f"""
    🌙 Dark Translator Web Server
    ==============================
    Starting on http://0.0.0.0:{port}
    
    Press Ctrl+C to stop
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=port)