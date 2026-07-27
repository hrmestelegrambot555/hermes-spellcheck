#!/usr/bin/env python3
"""
Hermes Spell-Check Userbot - AI Powered (Fixed Version)
"""
import asyncio
import os
from telethon import TelegramClient, events
import requests

API_ID = 31844510
API_HASH = "b1722fa9a615a9cdf394ee3886765b97"
PHONE = "+19432518923"
SESSION_NAME = "hermes_spellcheck"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "sk-or-v1-75ed86c133ce74985444cd1dc2f08e45e511f64e3d3c241b86c5fc8d8752d1d49")

last_edited = {}

# Comprehensive Persian typos dictionary
LOCAL_FIXES = {
    # Greetings - all variations
    "صلام": "سلام", "سلاام": "سلام", "سللام": "سلام",
    "ثلام": "سلام", "ثلامل": "سلام", "سلامم": "سلام",
    "سلاممم": "سلام", "سلامممم": "سلام",
    
    # Common words with half-space issues
    "میخوام": "می‌خوام", "میخوای": "می‌خوای", "میخواد": "می‌خواد",
    "میشه": "می‌شه", "میکنه": "می‌کنه", "میکنم": "می‌کنم",
    "میتونم": "می‌تونم", "میتونه": "می‌تونه", "میتونیم": "می‌تونیم",
    "میتونی": "می‌تونی", "میبینم": "می‌بینم", "میبینه": "می‌بینه",
    "میخوایم": "می‌خوایم", "میخوانم": "می‌خوام",
    "نمیخوام": "نمی‌خوام", "نمیشه": "نمی‌شه", "نمیکنه": "نمی‌کنه",
    "نمیتونم": "نمی‌تونم", "نمیتونه": "نمی‌تونه",
    "خواهش میکنم": "خواهش می‌کنم", "عذر میخوام": "عذر می‌خوام",
    "باید برم": "باید برم", "دارم میام": "دارم میام",
    
    # Questions
    "چتوری": "چطوری", "چجوری": "چطوری", "چطوریی": "چطوری",
    "چطوره": "چطوره", "چطوریه": "چطوریه", "چطوریم": "چطوریم",
    "چرا": "چرا", "کی": "کی", "کجا": "کجا",
    
    # Common typos - S/Z variations
    "خبی": "خوبی", "خوبم": "خوبم", "خوبی": "خوبی",
    "ممنون": "ممنون", "ممنونم": "ممنونم",
    "باشه": "باشه", "اوکی": "اوکی",
    "پیشی": "پیشی", "میشه": "می‌شه",
    
    # Common letter substitutions
    "هستم": "هستم", "هستی": "هستی", "هسته": "هسته",
    "دارم": "دارم", "داری": "داری", "داره": "داره",
    "کردم": "کردم", "کردی": "کردی", "کرده": "کرده",
    "رفتم": "رفتم", "رفتی": "رفتی", "رفته": "رفته",
    "اومدم": "اومدم", "اومدی": "اومدی", "اومده": "اومده",
    
    # Common misspellings
    "میخام": "می‌خوام", "میخوام": "می‌خوام",
    "میشی": "می‌شی", "میشیم": "می‌شیم",
    "میکنی": "می‌کنی", "میکنیم": "می‌کنیم",
    "میتونی": "می‌تونی", "میتونیم": "می‌تونیم",
    
    # Other common words
    "خیلی": "خیلی", "خیلیی": "خیلی",
    "عالی": "عالی", "عالیی": "عالی",
    "بد": "بد", "خوب": "خوب",
    "بده": "بده", "خوبه": "خوبه",
}

PROTECTED_WORDS = [
    "کص", "کیر", "کون", "ننه", "جنده", "حروم",
    "خفه", "گمشو", "له", "عینی", "خفن", "سیکتیر",
    " Bastard", "fuck", "shit", "ass", "dick",
    "پسک", "لاشی", "عوضی", "بی‌ناموس", "بی‌شرف",
]

def has_elongation(word):
    """Check if word has repeated characters (like سلامممم)"""
    for i in range(len(word) - 2):
        if word[i] == word[i+1] == word[i+2]:
            return True
    return False

def is_protected(word):
    """Check if word is a swear word or protected"""
    word_lower = word.lower().strip('؟!.,؛')
    for protected in PROTECTED_WORDS:
        if protected in word_lower or word_lower in protected:
            return True
    return False

def local_fix(text):
    """Apply local fixes without AI"""
    words = text.split()
    fixed_words = []
    for word in words:
        if has_elongation(word) or is_protected(word):
            fixed_words.append(word)
        else:
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
    """Use AI to fix text (with rate limit handling)"""
    if not OPENROUTER_API_KEY:
        return None
    
    # Skip AI if rate limited (check every 5 minutes)
    import time
    if not hasattr(ai_fix, 'last_call'):
        ai_fix.last_call = 0
    if not hasattr(ai_fix, 'rate_limited_until'):
        ai_fix.rate_limited_until = 0
    
    if time.time() < ai_fix.rate_limited_until:
        return None
    
    if time.time() - ai_fix.last_call < 2:  # Min 2 seconds between calls
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
7. حروف اضافه مثل «از»، «به»، «در» را تغییر نده
8. اعداد فارسی را تغییر نده

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
            fixed = result["choices"][0]["message"]["content"].strip().strip('"\'')
            # Only return if it's actually different and seems reasonable
            if fixed and fixed != text and len(fixed) > len(text) * 0.5:
                return fixed
        elif response.status_code == 429:
            # Rate limited - disable AI for 5 minutes
            ai_fix.rate_limited_until = time.time() + 300
            print("⚠️ Rate limited - AI disabled for 5 minutes")
    except Exception as e:
        print(f"AI Error: {e}")
    
    return None

def fix_text(text):
    """Fix text using local + AI"""
    if not text or len(text) < 2:
        return text, False
    
    # First: local fixes
    local_fixed = local_fix(text)
    
    # Then: AI fixes on the locally fixed text
    ai_fixed = ai_fix(local_fixed)
    
    # Return the best result
    if ai_fixed and ai_fixed != text:
        return ai_fixed, True
    if local_fixed != text:
        return local_fixed, True
    
    return text, False

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    @client.on(events.NewMessage(outgoing=True))
    async def handler(event):
        global last_edited
        
        # Only check private messages
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
            
            # Keep memory small
            if len(last_edited) > 100:
                keys = list(last_edited.keys())[:50]
                for k in keys:
                    del last_edited[k]
    
    print("🔄 Hermes AI Spell-Check Userbot started!")
    print("📝 Monitoring your outgoing messages...")
    print("✨ Elongations preserved")
    print("🛡️ Protected words preserved")
    print(f"🤖 AI: {'Enabled' if OPENROUTER_API_KEY else 'Disabled'}")
    print("Press Ctrl+C to stop")
    
    await client.start(phone=PHONE)
    print("✅ Connected to Telegram!")
    
    me = await client.get_me()
    print(f"👤 Logged in as: {me.first_name} (@{me.username})")
    
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
