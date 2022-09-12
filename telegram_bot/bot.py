import telebot
from config.settings import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


from .models import BotUser, RegisteredUser
from . import step
from .commands import BotController

@bot.message_handler(commands=['start'])
def start_handler(message):
    controller = BotController(message)

    user = BotUser.objects.get(chat_id=message.from_user.id)

    if user.step == step.IS_ANONYM:
        controller.start()
    else:
        controller.generate_sertificate()

@bot.message_handler(content_types=['text'])
def message_handler(message):
    controller = BotController(message)

    user = BotUser.objects.get(chat_id=message.from_user.id)

    if user.step == step.ZERO:
        controller.generate_sertificate()