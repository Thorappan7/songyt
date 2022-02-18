from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

import youtube_dl,time, ffmpeg
from youtube_search import YoutubeSearch
import requests
import yt_dlp
from yt_dlp import YoutubeDL
from text import Text

import os
from Config import Config

bot = Client(
    'song_bot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))



@bot.on_message(filters.command("start"))
def start(client, message):
    Ytdl_Bot = f"👋 𝗛𝗲𝗹𝗹𝗼 @{message.from_user.username}\n\nI'm an advanced Song Finder Bot\nCheck my buttons below to know more..\n"
    client.send_photo(message.chat.id,
        photo="https://telegra.ph/file/c91e170af27dead097415.jpg",
        caption=Ytdl_Bot,  
        parse_mode='html',
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton("Help", callback_data="help"),
            InlineKeyboardButton("About", callback_data="about")
            ],[
            InlineKeyboardButton("Channel", url="https://t.me/Malayalam_music),
            InlineKeyboardButton("Close", callback_data="close_data")
            ]]
        )
    )
@bot.on_message(filters.command(['song']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply("Searching..🧐")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            #UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            if time_to_seconds(duration) >= 1800:  # duration limit
                m.edit("Exceeded 30mins cap")
                return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('Try with correct Song name')
            return
    except Exception as e:
        m.edit(
            "✖️ Check spelling bro try again\n\n"
        )
        print(str(e))
        return
    m.edit("Processing 📥")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"☼ Title : {title[:35]}\n☼ Duration : {duration} \n☼ Upload By : @Malayalam_Music"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("Uploading..📤")
        message.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            parse_mode="md",
            title=title,
            duration=dur,
        )
        m.delete()
    except Exception as e:
        m.edit("❌ Error Contact Admin") 
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

@bot.on_callback_query()
async def cb_handler(client, query):
    if query.data == "close_data":
        await query.message.delete()

    elif query.data == "start":
        button = [[
            InlineKeyboardButton("Help", callback_data="help"),
            InlineKeyboardButton("About", callback_data="about")
        ],[
            InlineKeyboardButton("Channel", url="https://t.me/Malayalam_music),
            InlineKeyboardButton("Close", callback_data="close_data")
        ]]
        await query.message.edit_text(Text.START_TXT.format(query.from_user.mention), reply_markup=InlineKeyboardMarkup(button))
    
    elif query.data == "help":
        button = [[
            InlineKeyboardButton("Home", callback_data="start"),
            InlineKeyboardButton("About", callback_data="about")
        ]]
        await query.message.edit_text(Text.HELP_TXT.format(query.from_user.mention), reply_markup=InlineKeyboardMarkup(button))

    elif query.data == "about":
        button = [[
            InlineKeyboardButton("Home", callback_data="start"),
            InlineKeyboardButton("Back", callback_data="help")
        ]]
        await query.message.edit_text(Text.ABOUT_TXT.format(query.from_user.mention), reply_markup=InlineKeyboardMarkup(button))


bot.run()
