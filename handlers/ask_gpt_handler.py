import openai
from telethon.errors import MessageTooLongError

from userbot.config import OPENAI_API_KEY

from userbot.utils.chatGPT_func import ask_question
from userbot.utils.send_long_message_func import send_long_message


openai.api_key = OPENAI_API_KEY
role = "Ты помощник, отвечающий на вопросы."

async def ask_question_handler(client, event):
    question = event.pattern_match.group(1)
    await event.edit(f"Вопрос: {question}\nОбрабатывается...")

    answer = await ask_question(question, role)

    try:
        await event.edit(f"Вопрос: {question}\nОтвет: {answer}")
    except MessageTooLongError:
        await send_long_message(client, event.chat_id, f"Вопрос: {question}\nОтвет: {answer}")
