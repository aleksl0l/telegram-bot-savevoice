from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import redis
import io
import os

r = redis.StrictRedis(host='localhost', port=6379, db=1)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Я бот сохраняющий голосовые сообщения!")


def save_audio(bot, update):
    voice_id = update.message.voice.file_id
    user_id = update.message.from_user.id
    file = bot.get_file(voice_id)
    bot.send_message(chat_id=update.message.chat_id, text="Сохраняю...")
    with io.BytesIO() as buf:
        file.download(out=buf, timeout=10)
        r.rpush(str(user_id), buf.getbuffer().tobytes())


token = os.environ['token']
updater = Updater(token=token)

dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
img_handler = MessageHandler(Filters.voice, save_audio)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(img_handler)

updater.start_polling()

