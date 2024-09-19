from telethon.sync import events
import asyncio

@events.register(events.NewMessage(pattern=r'\?timer (\d+)'))
async def timer_handler(event):
    try:
        seconds = int(event.pattern_match.group(1))

        if seconds <= 0:
            await event.reply("Укажите положительное количество секунд.")
            return

        for remaining in range(seconds, 0, -1):
            await event.edit(f'{remaining} ')
            await asyncio.sleep(1)

        await event.edit("Alert!")

    except ValueError:
        await event.reply("Пожалуйста, укажите корректное количество секунд.")
