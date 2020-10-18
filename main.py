from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
import time
import os
import uuid
import json

from src.transcribe import transcribe_file

def start(update, context):
    message = ("Hi! I'm the Transcribe Bot. "
               "I will transcribe all voice messages sent in this chat."
               "You can find the code for me at https://github.com/AnHoang97/Transcriber-Bot")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message)

def audio2text(update, context):
    # download the voice file from the message
    print(
        f"[BACKEND] Download voice file trom the message {update.message.message_id}")
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    voice_path = os.path.join(".", "tmp", str(uuid.uuid4()) + ".ogg")
    file_id = update.message.voice.file_id
    voice_file = context.bot.get_file(file_id)
    voice_file.download(voice_path)

    # transcribe the voice message
    transcript = transcribe_file(
        voice_path, context.bot_data["s3-bucket"], context.bot_data["language"])

    # remove local voice file
    os.remove(voice_path)

    # send message
    if transcript:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text=transcript,
                                reply_to_message_id=update.message.message_id)
    else:
        print("[ERROR] Voice message can't be transcribed")


# create updater
if __name__ == "__main__":
    # read config file form ".token"
    with open("config.json", "rb") as f:
        config = json.load(f)

    updater = Updater(token=config["bot-token"], use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.bot_data.update(config)

    dispatcher.add_handler(MessageHandler(Filters.voice, audio2text))
    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
