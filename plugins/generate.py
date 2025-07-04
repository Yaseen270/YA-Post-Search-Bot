# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import traceback
from pyrogram.types import Message
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from info import API_ID, API_HASH, DATABASE_URI, ADMIN
from pymongo import MongoClient

mongo_client = MongoClient(DATABASE_URI)
database = mongo_client.userdb.sessions

strings = {
    'need_login': "U have to /login before using then bot can download restricted content ❕",
    'already_logged_in': "You are already logged in.\nIf you want to login again, /logout to proceed.",
}
SESSION_STRING_SIZE = 351

def get(obj, key, default=None):
    try:
        return obj[key]
    except:
        return default

@Client.on_message(filters.private & filters.command(["logout"]) & filters.user(ADMIN))
async def logout(_, msg):
    user_data = database.find_one({"chat_id": msg.chat.id})
    if user_data is None or not user_data.get('session'):
        return 
    data = {
        'session': None,
        'logged_in': False
    }
    database.update_one({'_id': user_data['_id']}, {'$set': data})
    await msg.reply("**Logout Successfully** ♦")

@Client.on_message(filters.private & filters.command(["login"]) & filters.user(ADMIN))
async def main(bot: Client, message: Message):
    user_data = database.find_one({"chat_id": message.from_user.id})
    if get(user_data, 'logged_in', False):
        await message.reply(strings['already_logged_in'])
        return 
    user_id = int(message.from_user.id)
    phone_number_msg = await bot.ask(chat_id=user_id, text="<b>আপনার ফোন নম্বরটি পাঠান যাতে দেশের কোড অন্তর্ভুক্ত থাকে।</b>\n<b>Example:</b> <code>+13124562345, +9171828181889</code>")
    if phone_number_msg.text=='/cancel':
        return await phone_number_msg.reply('<b>process cancelled !</b>')
    phone_number = phone_number_msg.text
    client = Client(":memory:", API_ID, API_HASH)
    await client.connect()
    await phone_number_msg.reply("Sending OTP...")
    try:
        code = await client.send_code(phone_number)
        phone_code_msg = await bot.ask(user_id, "অফিসিয়াল টেলিগ্রাম অ্যাকাউন্টে একটি OTP আছে কিনা তা পরীক্ষা করে দেখুন। যদি আপনি এটি পেয়ে থাকেন, তাহলে নীচের ফর্ম্যাটটি পড়ার পরে এখানে OTP পাঠান. \n\nIf OTP is `12345`, **please send it as** `1 2 3 4 5`.\n\n**Enter /cancel to cancel The Procces**", filters=filters.text, timeout=600)
    except PhoneNumberInvalid:
        await phone_number_msg.reply('`PHONE_NUMBER` **is invalid.**')
        return
    if phone_code_msg.text=='/cancel':
        return await phone_code_msg.reply('<b>process cancelled !</b>')
    try:
        phone_code = phone_code_msg.text.replace(" ", "")
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except PhoneCodeInvalid:
        await phone_code_msg.reply('**OTP is invalid.**')
        return
    except PhoneCodeExpired:
        await phone_code_msg.reply('**OTP is expired.**')
        return
    except SessionPasswordNeeded:
        two_step_msg = await bot.ask(user_id, '**আপনার অ্যাকাউন্টে দুই-পদক্ষেপ যাচাইকরণ সক্ষম করা হয়েছে। দয়া করে পাসওয়ার্ডটি প্রদান করুন।.\n\nEnter /cancel to cancel The Procces**', filters=filters.text, timeout=300)
        if two_step_msg.text=='/cancel':
            return await two_step_msg.reply('<b>process cancelled !</b>')
        try:
            password = two_step_msg.text
            await client.check_password(password=password)
        except PasswordHashInvalid:
            await two_step_msg.reply('**Invalid Password Provided**')
            return
    string_session = await client.export_session_string()
    await client.disconnect()
    if len(string_session) < SESSION_STRING_SIZE:
        return await message.reply('<b>invalid session sring</b>')
    try:
        user_data = database.find_one({"chat_id": message.from_user.id})
        if user_data is not None:
            data = {
                'session': string_session,
                'logged_in': True
            }

            uclient = Client(":memory:", session_string=data['session'], api_id=API_ID, api_hash=API_HASH)
            await uclient.connect()

            database.update_one({'_id': user_data['_id']}, {'$set': data})
    except Exception as e:
        return await message.reply_text(f"<b>ERROR IN LOGIN:</b> `{e}`")
    await bot.send_message(message.from_user.id, "<b>অ্যাকাউন্ট লগইন সফলভাবে.\n\nIf আপনি AUTH KEY সম্পর্কিত যেকোনো ত্রুটি পাবেন তাহলে /logout and /login again</b>")


# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
