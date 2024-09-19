from telethon.sync import TelegramClient, events
from handlers.song_search_handler import song_search_handler
from handlers.ask_gpt_handler import ask_question_handler
from handlers.timer_handler import timer_handler
from handlers.translate_handler import translate_handler
from config import API_ID, API_HASH, SESSION_NAME

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

client.start()

client.add_event_handler(lambda event: song_search_handler(client, event), events.NewMessage(pattern=r'\?song(?: (.+))?'))
client.add_event_handler(ask_question_handler, events.NewMessage(pattern=r'\?ask (.+)'))
client.add_event_handler(translate_handler, events.NewMessage(pattern=r'\?tr(?: (.+))?'))
client.add_event_handler(timer_handler, events.NewMessage(pattern=r'\?timer (\d+)'))

client.run_until_disconnected()
