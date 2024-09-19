from deep_translator import GoogleTranslator
from langdetect import detect


async def translate_text(text):
    try:
        original_lang = detect(text)

        if original_lang == 'ru':
            target_lang = 'en'
        else:
            target_lang = 'ru'
        print(original_lang, target_lang)
        translated = GoogleTranslator(source = original_lang, target = target_lang).translate(text)

        return translated

    except Exception as e:
        return f"Ошибка при определении языка или переводе: {e}"
