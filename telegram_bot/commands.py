import telebot
from config.settings import BOT_TOKEN
from PIL import Image, ImageDraw, ImageFont
import qrcode

from django.core.exceptions import ObjectDoesNotExist

from .models import BotUser, RegisteredUser
from telegram_bot import step, excel_reader
import os

from pathlib import Path

bot = telebot.TeleBot(BOT_TOKEN)

class BotController:
    def __init__(self, message):
        self.message = message
        self.chat_id = message.from_user.id
        self.user, _ = BotUser.objects.get_or_create(chat_id=self.chat_id)
        self.message_id = message.message_id if hasattr(message, "message_id") else message.message.message_id

    def start(self):
        bot.send_message(self.chat_id, "Assalomu alaykum! Sertifikatni olish uchun, <b>EMAIL</b> ingizni yuboring", parse_mode='html')
        self.set_step(step.ZERO)

    def send_existing_sertificate(self):
        bot.send_photo(self.chat_id, self.user.file_id)

    def generate_sertificate(self):
        bot.send_message(self.chat_id, "Foyalanuvchi tekshirilmoqda...")
        if self.user.file_id != None and self.user.file_id != "":
            bot.send_message(self.chat_id, "Tayyorlanmoqda...")
            return self.send_existing_sertificate()

        try:
            user = RegisteredUser.objects.filter(email=self.message.text).first()
            
            if user is None:
                return self.email_not_registered()

            bot.send_message(self.chat_id, "Tayyorlanmoqda...")

            path = user.name

            self.save_image(path)

            file = bot.send_photo(chat_id=self.chat_id, photo=open(f'{path}.png', 'rb'))

            os.remove(f'{path}.png')

            self.user.file_id = file.photo[0].file_id
            
            self.user.save()
        
        except ObjectDoesNotExist:
            self.email_not_registered()

    def save_image(self, name):
        image = Image.open('rasm.png')

        draw = ImageDraw.Draw(image)
        
        font = ImageFont.truetype('Merienda-Bold.ttf', 130)
        
        draw.text(((220, 1800)), name, (0, 0, 0), font=font)

        qr_code = qrcode.QRCode(box_size=20)
        
        qr_code.add_data('https://t.me/Dg2022_bot')
        
        qr_code.make()   
        
        img_qr = qr_code.make_image()

        pos = (image.size[0] - img_qr.size[0], image.size[1] - img_qr.size[1])

        image.paste(img_qr, pos)

        image.save("{}.png".format(name))        

    def email_not_registered(self):
        bot.send_message(self.chat_id, "Ro'yxatdan o'tmagan foydalanuvchi")

    def change_database(self):
        excel_reader.locate_users()
        bot.send_message(self.chat_id, "Changed")

    def set_step(self, step):
        self.user.step = step
        self.user.save()   

    