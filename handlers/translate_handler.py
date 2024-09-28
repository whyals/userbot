from telethon.sync import events

from userbot.utils.translate_func import translate_text


@events.register(events.NewMessage(pattern=r'\?tr(?: (.+))?'))
async def translate_handler(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        original_text = reply_message.text
        translated_text = translate_text(original_text)

        await event.edit(f"Перевод: {translated_text}")

    elif event.pattern_match.group(1):
        original_text = event.pattern_match.group(1)
        translated_text = await translate_text(original_text)

        await event.edit(f"Оригинал: {original_text}\nПеревод: {translated_text}")

    else:
        await event.edit("Пожалуйста, ответьте на сообщение или введите текст для перевода.")
        return
