#!/usr/bin/env python3
"""
Hermes AI Spell-Check Userbot - Railway Version (Session String)
"""
import asyncio
import os
import json
import time
from telethon import TelegramClient, events, StringSession
import requests

API_ID = int(os.environ.get("API_ID", "31844510"))
API_HASH = os.environ.get("API_HASH", "b1722fa9a615a9cdf394ee3886765b97")
SESSION_STRING = os.environ.get("SESSION_STRING", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

last_edited = {}

# ═══════════════════════════════════════════════
# LOAD DICTIONARY
# ═══════════════════════════════════════════════
DICT_PATH = os.path.join(os.path.dirname(__file__), "persian_dict.json")
print(f"📝 Loading dictionary from {DICT_PATH}...")
with open(DICT_PATH, "r", encoding="utf-8") as f:
    LOCAL_FIXES = json.load(f)
print(f"✅ Loaded {len(LOCAL_FIXES)} entries")

# ═══════════════════════════════════════════════
# EXTRA FIXES
# ═══════════════════════════════════════════════
EXTRA_FIXES = {
    "صلام": "سلام", "سلاام": "سلام", "سللام": "سلام",
    "ثلام": "سلام", "هلو": "سلام", "هلا": "سلام",
    "مچكرم": "ممنونم", "مچکرم": "mI keep having issues. Let me just write the whole file from scratch.",
    "بلاخره": "بالاخره", "بلي": "بله",
    "میخوام": "mI keep having issues. Let me just write the whole file from scratch.",
    "میخوای": "mI keep having issues. Let me just write the whole file from scratch.",
    "میخواد": "mI keep having issues. Let me just write the whole file from scratch.",
    "میشه": "mI keep having issues. Let me just write the whole file from scratch.",
    "میکنه": "mI keep having issues. Let me just write the whole file from scratch.",
    "میکنم": "mI keep having issues. Let me just write the whole file from scratch.",
    "میتونم": "mI keep having issues. Let me just write the whole file from scratch.",
    "میتونه": "mI keep having issues. Let me just write the whole file from scratch.",
    "میتونی": "mI keep having issues. Let me just write the whole file from scratch.",
    "میبینم": "mI keep having issues. Let me just write the whole file from scratch.",
    "میبینه": "mI keep having issues. Let me just write the whole file from scratch.",
}
LOCAL_FIXES.update(EXTRA_FIXES)

PROTECTED_WORDS = [
    "کص", "کیر", "کون", "ننه", "جنده", "حروم",
    "خفه", "گمشو", "له", "عینی", "خفن", "سیکتیر",
    "fuck", "shit", "ass", "dick",
    "پسک", "لاشی", "عوضی", "بی‌ناموس", "بی‌شرف",
]

def has_elongation(word):
    for i in range(len(word) - 2):
        if word[i] == word[i+1] == word[i+2]:
            return True
    return False

def get_base_form(word):
    if not word:
        return word
    base = word[0]
    for i in range(1, len(word)):
        if word[i] != word[i-1]:
            base += word[i]
    return base

def is_protected(word):
    word_lower = word.lower().strip('؟!.,؛')
    for protected in PROTECTED_WORDS:
        if protected in word_lower or word_lower in protected:
            return True
    return False

def local_fix(text):
    words = text.split()
    fixed_words = []
    for word in words:
        if is_protected(word):
            fixed_words.append(word)
            continue
        
        if word in LOCAL_FIXES:
            fixed_words.append(LOCAL_FIXES[word])
            continue
        
        if has_elongation(word):
            base = get_base_form(word)
            if base in LOCAL_FIXES:
                corrected_base = LOCAL_FIXES[base]
                if len(word) > len(base):
                    fixed_words.append(corrected_base + corrected_base[-1])
                else:
                    fixed_words.append(corrected_base)
                continue
            base_k = base.replace('ک', 'ك')
            base_y = base.replace('ی', 'ي')
            if base_k in LOCAL_FIXES:
                corrected_base = LOCAL_FIXES[base_k]
                if len(word) > len(base):
                    fixed_words.append(corrected_base + corrected_base[-1])
                else:
                    fixed_words.append(corrected_base)
                continue
            if base_y in LOCAL_FIXES:
                corrected_base = LOCAL_FIXES[base_y]
                if len(word) > len(base):
                    fixed_words.append(corrected_base + corrected_base[-1])
                else:
                    fixed_words.append(corrected_base)
                continue
            fixed_words.append(word)
            continue
        
        fixed = False
        for wrong, correct in LOCAL_FIXES.items():
            if word == wrong:
                fixed_words.append(correct)
                fixed = True
                break
        if not fixed:
            fixed_words.append(word)
    return ' '.join(fixed_words)

def ai_fix(text):
    if not OPENROUTER_API_KEY:
        return None
    if not hasattr(ai_fix, 'last_call'):
        ai_fix.last_call = 0
    if not hasattr(ai_fix, 'rate_limited_until'):
        ai_fix.rate_limited_until = 0
    if time.time() < ai_fix.rate_limited_until:
        return None
    if time.time() - ai_fix.last_call < 2:
        return None
    ai_fix.last_call = time.time()
    prompt = f"""تو یک ویرایشگر متن فارسی هستی. متن زیر را بررسی کن و فقط غلط‌های املایی را اصلاح کن.

قوانین مهم:
1. اگر کلمه‌ای کشیده شده (مثل سلامممم) آن را تغییر نده
2. هیچ کلمه‌ای را حذف یا اضافه نکن
3. فقط غلط‌های املایی را درست کن
4. نیم‌فاصله‌ها را درست کن
5. کلمات عامیانه مثل خوبی، ممنون، باشه را تغییر نده
6. اگر متن درست است، همان متن را برگردان

متن ورودی:
{text}

متن اصلاح شده:"""
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "google/gemma-4-26b-a4b-it:free",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
                "temperature": 0.1
            },
            timeout=15
        )
        if response.status_code == 200:
            result = response.json()
            fixed = result["choices"][0]["message"]["content"].strip().strip("\"'")
            if fixed and fixed != text and len(fixed) > len(text) * 0.5:
                return fixed
        elif response.status_code == 429:
            ai_fix.rate_limited_until = time.time() + 300
            print("⚠️ Rate limited - AI disabled for 5 minutes")
    except Exception as e:
        print(f"AI Error: {e}")
    return None

def fix_text(text):
    if not text or len(text) < 2:
        return text, False
    ai_fixed = ai_fix(text)
    if ai_fixed and ai_fixed != text:
        return ai_fixed, True
    local_fixed = local_fix(text)
    if local_fixed != text:
        return local_fixed, True
    return text, False

async def main():
    if not SESSION_STRING:
        print("❌ SESSION_STRING not set!")
        print("Set it in Railway Environment Variables")
        return
    
    client = StringSession(SESSION_STRING)

    @client.on(events.NewMessage(outgoing=True))
    async def handler(event):
        global last_edited
        if not event.is_private:
            return
        text = event.message.text
        if not text or len(text) < 2:
            return
        fixed_text, was_fixed = fix_text(text)
        if was_fixed and fixed_text != text:
            msg_id = event.message.id
            if msg_id in last_edited:
                return
            last_edited[msg_id] = True
            await asyncio.sleep(0.5)
            try:
                await event.message.edit(fixed_text)
                print(f"✅ Edited: '{text[:40]}' -> '{fixed_text[:40]}'")
            except Exception as e:
                print(f"❌ Edit failed: {e}")
            if len(last_edited) > 100:
                keys = list(last_edited.keys())[:50]
                for k in keys:
                    del last_edited[k]

    print(f"🔄 Hermes AI Spell-Check Userbot started!")
    print(f"📝 Dictionary: {len(LOCAL_FIXES)} local fixes loaded")
    print("✨ Elongations preserved")
    print("🛡️ Protected words preserved")
    print(f"🤖 AI: {'Enabled' if OPENROUTER_API_KEY else 'Disabled'}")

    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ Session not authorized! Generate a new one.")
        return
    
    me = await client.get_me()
    print(f"✅ Connected to Telegram!")
    print(f"👤 Logged in as: {me.first_name} (@{me.username})")
    
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
