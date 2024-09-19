# ВАЖНО!

Запускайте бота **ТОЛЬКО** на своем пк или личном сервере. Бот использует данные telegram client api, которе дают практически полный доступ к вашему телеграмму. Не сообщайте никому эти данные и не хостите бота на облачных серверах

# GPT_USERBOT

Этот мини проект представляет собой бота для Telegram, реализованного на Python который призван чуть-чуть упростить жизнь, не тратия время на переключение на другие приложения
## Функциональность

- **Ассистент GPT**: Быстрый поиск информации с помощью chatGPT от openai
- **Поиск песен**: Бот ищет песни по их названию или исполнителю и присылает ссылки на spotify, yandex и songlink
- **Преревод текста**: Бот автоматически определяет текст и перевод на русский/анлийский по необхоимости
- **Таймер**: утсановка таймера на n секунд
- **СЕКРЕТНО**: секрнтно



## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/whyals/userbot.git
   
2. Перейдите в дирректорию:
   ```bash
   cd userbot

3. Установить библиотеки:
   !!!перед установкой библиотеки shazamio необхожимо скачать rust
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```
   ```bash
   pip install -r requirements.txt

4. Пропишите все необхожимые ключи и параметры в config.py

5. Запустите:
   ```bash
   python bot.py

## Полезные ссылки

**[GPT models](https://platform.openai.com/docs/models/gpt-4o)** здесь вы найдете все варианты моделей openai и их цены

**[Telegram ID + Hash](https://my.telegram.org/apps)** cоздайте свое приложение и получите id и hash для использования бота

**[Spotify Token](https://developer.spotify.com/dashboard/152cff3c42a44766bbe1fdf5a3185cdc/settings)** получение id и токена для spotify

**[Yandex Token](https://yandex-music.readthedocs.io/en/main/token.html)** получение токена для Yandec Music



**[Spotify API](https://spotipy.readthedocs.io/en/2.24.0)**

**[Shazam API](https://github.com/shazamio/ShazamIO)**

**[Songlink API](https://linktree.notion.site/API-d0ebe08a5e304a55928405eb682f6741)**

**[Yandex Music API](https://yandex-music.readthedocs.io/en/main/index.html)** з

**[Translate API](https://github.com/nidhaloff/deep-translator)** 



