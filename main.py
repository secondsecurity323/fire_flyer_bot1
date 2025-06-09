from flask import Flask, request
import telegram
import os

TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    msg = update.message

    if not msg:
        return 'ok'

    chat_id = msg.chat.id
    user = msg.from_user
    text = msg.text.lower() if msg.text else ""

    if text in ["ایدی", "/ایدی"]:
        role = "سازنده ربات" if user.id == OWNER_ID else "ادمین" if msg.chat.get_member(user.id).status in ["administrator", "creator"] else "کاربر عادی"
        username = f"@{user.username}" if user.username else "ندارد"
        reply = f"👤 نام: {user.first_name}\n🆔 آیدی عددی: {user.id}\n🔗 یوزرنیم: {username}\n👑 مقام: {role}"
        bot.send_message(chat_id=chat_id, text=reply)

    elif text == "admin" and msg.reply_to_message and msg.chat.type in ["group", "supergroup"]:
        target = msg.reply_to_message.from_user
        role = "سازنده ربات" if target.id == OWNER_ID else "ادمین" if msg.chat.get_member(target.id).status in ["administrator", "creator"] else "کاربر عادی"
        username = f"@{target.username}" if target.username else "ندارد"
        reply = f"👤 نام: {target.first_name}\n🆔 آیدی عددی: {target.id}\n🔗 یوزرنیم: {username}\n👑 مقام: {role}"
        bot.send_message(chat_id=chat_id, text=reply)

    return 'ok'
