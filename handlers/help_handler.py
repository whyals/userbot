async def help_handler(event):
    help_text = 
"""
**[als_userbot](https://github.com/whyals/userbot)**
Автор : @why_als
ТГ канал проекта : @als_userbot

**Доступные команды:**
• `?gpt` - Задать вопрос GPT
• `?song` - Поиск песни
• `?tr` - Перевести текст
• `?timer` - Установить таймер

**Недоступные команды:**
• `?ban` - Бан пользователя
• `?unban` - Разбанить пользователя
• `?mute` - Замутить пользователя
• `?unmute` - Размутить пользователя
• `?mem` - создать мем по шаблону
(что бы просмотреть список шаблонов введите `?mem_list`)
"""
    await event.edit(help_text, parse_mode='markdown')
