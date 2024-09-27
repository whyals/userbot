import asyncio
import logging
from functools import partial
from telethon import events, TelegramClient

from userbot_handlers.search_song_handler import song_search_handler
from userbot_handlers.ask_gpt_handler import ask_question_handler
from userbot_handlers.timer_handler import timer_handler
from userbot_handlers.translate_handler import translate_handler
from userbot_handlers.help_handler import help_handler

from userbot_handlers.user_moderation_handler import ban_user, unban_user, mute_user, unmute_user

from config import API_ID, API_HASH, SESSION_NAME

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def main():
    await client.start()
    logger.info("Userbot запущен.")

    client.add_event_handler(
        partial(song_search_handler, client),
        events.NewMessage(pattern=r'\?song(?: (.+))?')
    )
    client.add_event_handler(
        partial(ask_question_handler, client),
        events.NewMessage(pattern=r'\?gpt (.+)')
    )
    client.add_event_handler(translate_handler,
        events.NewMessage(pattern=r'\?tr(?: (.+))?')
    )
    client.add_event_handler(
        timer_handler,
        events.NewMessage(pattern=r'\?timer (\d+)')
    )
    client.add_event_handler(
        help_handler,
        events.NewMessage(pattern=r'\?help')
    )


    client.add_event_handler(
        partial(ban_user, client),
        events.NewMessage(pattern=r'^\.?ban$')
    )
    client.add_event_handler(
        partial(unban_user, client),
        events.NewMessage(pattern=r'^\.?unban$')
    )
    client.add_event_handler(
        partial(mute_user, client),
        events.NewMessage(pattern=r'\?mute(?: (\d+))?')
    )
    client.add_event_handler(
        partial(unmute_user, client),
        events.NewMessage(pattern=r'\?unmute')
    )

    logger.info("Обработчики зарегистрированы.")

    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Userbot остановлен.")
