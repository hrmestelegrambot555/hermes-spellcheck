# Spellcheck Userbot for Railway

## مراحل استقرار:

1. **آپلود به GitHub:**
   - یه repo جدید بساز
   - فایل‌های `main.py`, `requirements.txt`, `railway.json` رو آپلود کن

2. **استقرار در Railway:**
   - برو به railway.app
   - با GitHub لاگین کن
   - روی "New Project" بزن
   - "Deploy from GitHub repo" رو انتخاب کن
   - repo رو انتخاب کن
   - Railway خودکار build و deploy می‌کنه

3. **متغیرهای محیطی (Variables):**
   - هیچ متغیری لازم نیست چون همه چیز توی کد هست

4. **فایل session:**
   - فایل `hermes_spellcheck.session` رو هم آپلود کن
   - یا دوباره authenticate کن

## نکات مهم:
- Railway رایگانه (۵۰۰ ساعت در ماه)
- اگه خاموش بشه، خودکار ری‌استارت می‌شه
- برای متوقف کردن: project رو pause کن
