from telethon import events
import openai
from telethon.errors import MessageTooLongError

from utils.chatGPT_func import ask_question
from config import OPENAI_API_KEY, client
from utils.send_long_message_func import send_long_message


openai.api_key = OPENAI_API_KEY
role = "Ты помощник, отвечающий на вопросы."

@events.register(events.NewMessage(pattern=r'\?ask (.+)'))
async def ask_question_handler(event):
    question = event.pattern_match.group(1)
    await event.edit(f"Вопрос: {question}\nОбрабатывается...")

    answer = await ask_question(question, role)

    try:
        await event.edit(f"Вопрос: {question}\nОтвет: {answer}")
    except MessageTooLongError:
        await send_long_message(client, event.chat_id, f"Вопрос: {question}\nОтвет: {answer}")
