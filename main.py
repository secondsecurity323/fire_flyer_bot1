import os
import telebot
from flask import Flask, request

TOKEN = '7330507162:AAGBzEhn-wwwdiGoHIflj1W47cTnbcrQL3c'
OWNER_ID =1656844563

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return ''

@bot.message_handler(func=lambda m: m.text and m.text.lower() in ['ایدی', '/ایدی'])
def send_id(message):
    user = message.from_user
    role = "سازنده ربات" if user.id == OWNER_ID else "ادمین" if get_chat_status(message.chat.id, user.id) in ['administrator', 'creator'] else "کاربر عادی"
    username = f"@{user.username}" if user.username else "ندارد"
    text = f"👤 نام: {user.first_name}\n🆔 آیدی عددی: {user.id}\n🔗 یوزرنیم: {username}\n👑 مقام: {role}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text and m.text.lower() == 'admin' and m.reply_to_message)
def reply_admin(message):
    target = message.reply_to_message.from_user
    role = "سازنده ربات" if target.id == OWNER_ID else "ادمین" if get_chat_status(message.chat.id, target.id) in ['administrator', 'creator'] else "کاربر عادی"
    username = f"@{target.username}" if target.username else "ندارد"
    text = f"👤 نام: {target.first_name}\n🆔 آیدی عددی: {target.id}\n🔗 یوزرنیم: {username}\n👑 مقام: {role}"
    bot.send_message(message.chat.id, text)

def get_chat_status(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status
    except:
        return None

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f'https://fire-flyer-bot1.onrender.com/{TOKEN}')

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
