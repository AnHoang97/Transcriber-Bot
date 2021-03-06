import json
import os
import uuid
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from src.transcribe import transcribe_file


def start(update: Update, context: CallbackContext) -> None:
    message = ("Hi! I'm the Transcribe Bot. "
               "I will transcribe all voice messages sent in this chat."
               "You can find the code for me at https://github.com/AnHoang97/Transcriber-Bot")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message)


def audio2text(update: Update, context: CallbackContext) -> None:
    # download the voice file from the message
    logging.info(
        f"Download voice file trom message {update.message.message_id}.")
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
        logging.error("Voice message can't be transcribed")


# create updater
if __name__ == "__main__":
    if not os.path.exists('log'):
        os.makedirs('log')
    logging.basicConfig(level=logging.DEBUG,
                        format="[%(levelname)s] %(asctime)s - %(name)s : %(message)s",
                        handlers=[
                            logging.handlers.TimedRotatingFileHandler(
                                "log/" + "debug.log", 
                                encoding="utf-8",
                                when="midnight",
                            ),
                            logging.StreamHandler()
                        ]
                        )

    updater = Updater(token=os.environ['TRANSCRIBEBOT_TELEGRAM_TOKEN'], use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.bot_data.update({
        "s3-bucket": os.environ['TRANSCRIBEBOT_AWS_S3_BUCKET'],
        "language": os.environ['TRANSCRIBEBOT_LANGUAGE'],
    })

    dispatcher.add_handler(MessageHandler(Filters.voice, audio2text))
    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
