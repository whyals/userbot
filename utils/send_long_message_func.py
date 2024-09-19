async def send_long_message(client, chat_id, message):
    MAX_MESSAGE_LENGTH = 4096
    for i in range(0, len(message), MAX_MESSAGE_LENGTH):
        part = message[i:i+MAX_MESSAGE_LENGTH]
        await client.send_message(chat_id, part)
