api_id = input("Введите telegram ID (ClientTelegram API): ")
api_hash = input("Введите telegram HASH: ")
session_name = input("Введите название сессии: ")

openai_api_key = input("Введите ключ OpenAI: ")
gpt_model = input("Введите название модели GPT (например, gpt-4o-mini-2024-07-18): ")

sp_client_id = input("Введите Spotify Client ID: ")
sp_client_secret = input("Введите Spotify Client Secret: ")

ym_token = input("Введите токен Yandex Music: ")

with open('config.py', 'w') as configfile:
    configfile.write(f"API_ID = '{api_id}'\n")
    configfile.write(f"API_HASH = '{api_hash}'\n")
    configfile.write(f"SESSION_NAME = '{session_name}'\n\n")

    configfile.write(f"OPENAI_API_KEY = '{openai_api_key}'\n")
    configfile.write(f"GPT_MODEL = '{gpt_model}'\n\n")

    configfile.write(f"SP_CLIENT_ID = '{sp_client_id}'\n")
    configfile.write(f"SP_CLIENT_SECRET = '{sp_client_secret}'\n\n")

    configfile.write(f"YM_TOKEN = '{ym_token}'\n")

print("Конфигурационный файл config.py успешно создан.")
