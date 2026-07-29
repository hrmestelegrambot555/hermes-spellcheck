#!/usr/bin/env python3
"""
Generate Telethon Session String
Run this LOCALLY, then copy the output to Railway env var
"""
from telethon.sync import TelegramClient

API_ID = 31844510
API_HASH = "b1722fa9a615a9cdf394ee3886765b97"
PHONE = "+19432518923"

with TelegramClient('session_gen', API_ID, API_HASH) as client:
    client.start(phone=PHONE)
    string = client.session.save()
    print("\n" + "="*60)
    print("✅ SESSION STRING:")
    print("="*60)
    print(string)
    print("="*60)
    print("\nاین رشته رو کپی کن و به عنوان SESSION_STRING در Railway بذار")
