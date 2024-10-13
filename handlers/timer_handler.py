import asyncio
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

timer_running = False


async def timer_handler(event):
    global timer_running
    try:
        message = event.pattern_match.group(1)
        logger.info(f"Запрос таймера на {message}")

        if message.lower() == "stop":
            await event.delete()
            timer_running = False
            logger.info("Таймер остановлен")
            return

        hms_match = re.match(r'(\d+):(\d+):(\d+)', message)
        hm_match = re.match(r'(\d+):(\d+)', message)
        sec_match = re.match(r'(\d+)', message)
        logger.info(f"Результат: {hms_match} {hm_match} {sec_match}")

        if hms_match:
            hours = int(hms_match.group(1))
            minutes = int(hms_match.group(2))
            seconds = int(hms_match.group(3))
            total_seconds = hours * 3600 + minutes * 60 + seconds
        elif hm_match:
            hours = int(hm_match.group(1))
            minutes = int(hm_match.group(2))
            total_seconds = hours * 3600 + minutes * 60
        elif sec_match:
            total_seconds = int(sec_match.group(1))
        else:
            await event.edit("Пожалуйста, укажите время в формате hh:mm:ss, hh:mm или в секундах")
            return

        if total_seconds <= 0:
            await event.edit("Укажите положительное количество времени")
            return

        timer_running = True
        for remaining in range(total_seconds, 0, -1):
            if not timer_running:
                await event.reply("Таймер остановлен")
                logger.info("Таймер остановлен")
                return

            hours, remainder = divmod(remaining, 3600)
            minutes, seconds = divmod(remainder, 60)
            await event.edit(f'{hours:02}:{minutes:02}:{seconds:02}')
            await asyncio.sleep(1)

        await event.reply("АЛЕРТ")
        logger.info("Таймер закончился")

    except ValueError:
        await event.edit("Пожалуйста, укажите корректное количество времени")
