from telethon.sync import TelegramClient
from telethon.sessions import StringSession


api_id = int(input("API_ID: "))
api_hash = input("API_HASH: ")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    client.start()
    session_string = client.session.save()

    print("\n--- ВАША СТРОКА СЕССИИ ---")
    print(session_string)
    print("--------------------------\n")
