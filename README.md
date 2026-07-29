# Hermes Spell-Check Userbot - Railway Deploy

## راهنمای استقرار

### ۱. تولید Session String
ابتدا فایل `gen_session_string.py` رو لوکال اجرا کن:
```bash
pip install telethon==1.44.0
python3 gen_session_string.py
```
یه رشته بلند می‌ده — کپیش کن.

### ۲. آپلود به GitHub
```bash
git init
git add .
git commit -m "spellcheck bot"
git remote add origin https://github.com/YOUR_USER/spellcheck-bot.git
git push -u origin main
```

### ۳. استقرار در Railway
1. به [railway.app](https://railway.app) برو
2. `New Project` → `Deploy from GitHub`
3. ریپو رو انتخاب کن

### ۴. تنظیم Environment Variables
| Variable | Value |
|----------|-------|
| `API_ID` | `31844510` |
| `API_HASH` | `b1722fa9a615a9cdf394ee3886765b97` |
| `SESSION_STRING` | `1BVbu...` (رشته‌ای که کپی کردی) |
| `OPENROUTER_API_KEY` | `sk-or-v1-...` |

### ۵. آپدیت دیکشنری
دیکشنری `persian_dict.json` حدود ۴۴MB است.
برای آپدیت، فایل جدید رو جایگزین کن و دوباره deploy کن.

### ⚠️ نکات مهم
- فایل `.session` در GitHub آپلود نمی‌شه (در .gitignore هست)
- Session String امن‌تر از فایل session است
- اگر Session منقضی شد، دوباره `gen_session_string.py` رو اجرا کن
