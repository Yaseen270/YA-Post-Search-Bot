# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

from info import *
from utils import *
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

@Client.on_message(filters.group & filters.command("fsub"))
async def f_sub_cmd(bot, message):
    m=await message.reply("Please wait..")
    try:
       group     = await get_group(message.chat.id)
       user_id   = group["user_id"] 
       user_name = group["user_name"]
       verified  = group["verified"]
    except :
       return await bot.leave_chat(message.chat.id)  
    if message.from_user.id!=user_id:
       return await m.edit(f"<b>Only {user_name} can use this command</b> 😁")
    if bool(verified)==False:
       return await m.edit("<b>This chat is not verified!\nuse /verify</b>")    
    try:
       f_sub = int(message.command[-1])
    except:
       return await m.edit("❌ <b>Incorrect format!\nUse</b> `/fsub ChannelID`")       
    try:
       chat   = await bot.get_chat(f_sub)
       group  = await bot.get_chat(message.chat.id)
       c_link = chat.invite_link
       g_link = group.invite_link       
    except Exception as e:
       text = f"❌ <b>Error:</b> `{str(e)}`\n\n<b>নিশ্চিত করুন যে আমি সেই চ্যানেল এবং এই গ্রুপের সমস্ত অনুমতি সহ অ্যাডমিন।</b>"
       return await m.edit(text)
    await update_group(message.chat.id, {"f_sub":f_sub})
    await m.edit(f"✅ <b>সফলভাবে ForceSub সংযুক্ত করা হয়েছে [{chat.title}]({c_link})!</b>", disable_web_page_preview=True)
    text = f"#NewFsub\n\nUser: {message.from_user.mention}\nGroup: [{group.title}]({g_link})\nChannel: [{chat.title}]({c_link})"
    await bot.send_message(chat_id=LOG_CHANNEL, text=text)

@Client.on_message(filters.group & filters.command("nofsub"))
async def nf_sub_cmd(bot, message):
    m=await message.reply("Disattaching..")
    try:
       group     = await get_group(message.chat.id)
       user_id   = group["user_id"] 
       user_name = group["user_name"]
       verified  = group["verified"]
       f_sub     = group["f_sub"]
    except :
       return await bot.leave_chat(message.chat.id)  
    if message.from_user.id!=user_id:
       return await m.edit(f"Only {user_name} can use this command 😁")
    if bool(verified)==False:
       return await m.edit("<b>This chat is not verified!\nuse /verify</b>")        
    if bool(f_sub)==False:
       return await m.edit("<b>এই চ্যাটে বর্তমানে কোনও FSub নেই।\nuse /fsub</b>")        
    try:
       chat   = await bot.get_chat(f_sub)
       group  = await bot.get_chat(message.chat.id)
       c_link = chat.invite_link
       g_link = group.invite_link       
    except Exception as e:
       text = f"❌ <b>Error:</b> `{str(e)}`\n\n<b>নিশ্চিত করুন যে আমি সেই চ্যানেল এবং এই গ্রুপের সমস্ত অনুমতি সহ অ্যাডমিন।</b>"
       return await m.edit(text)
    await update_group(message.chat.id, {"f_sub":False})
    await m.edit(f"✅ <b>থেকে FSub সফলভাবে সরানো হয়েছে [{chat.title}]({c_link})!</b>", disable_web_page_preview=True)
    text = f"#RemoveFsub\n\nUser: {message.from_user.mention}\nGroup: [{group.title}]({g_link})\nChannel: [{chat.title}]({c_link})"
    await bot.send_message(chat_id=LOG_CHANNEL, text=text)

       
@Client.on_callback_query(filters.regex(r"^checksub"))
async def f_sub_callback(bot, update):
    user_id = int(update.data.split("_")[-1])
    group   = await get_group(update.message.chat.id)
    f_sub   = group["f_sub"]
    admin   = group["user_id"]

    if update.from_user.id!=user_id:
       return await update.answer("<b>That's not for you</b> 😂", show_alert=True)
    try:
       await bot.get_chat_member(f_sub, user_id)          
    except UserNotParticipant:
       await update.answer("<b>I like your smartness..\nBut don't be over smart</b> 🤭", show_alert=True) # @kingvj01 😁
    except:       
       await bot.restrict_chat_member(chat_id=update.message.chat.id, 
                                      user_id=user_id,
                                      permissions=ChatPermissions(can_send_messages=True,
                                                                  can_send_media_messages=True,
                                                                  can_send_other_messages=True))
       await update.message.delete()
    else:
       await bot.restrict_chat_member(chat_id=update.message.chat.id, 
                                      user_id=user_id,
                                      permissions=ChatPermissions(can_send_messages=True,
                                                                  can_send_media_messages=True,
                                                                  can_send_other_messages=True))
       await update.message.delete()
