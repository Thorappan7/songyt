from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

import youtube_dl
from youtube_search import YoutubeSearch
import requests
import yt_dlp
from yt_dlp import YoutubeDL

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
    Ytdl_Bot = f"👋 𝗛𝗲𝗹𝗹𝗼 @{message.from_user.username}\n\nI'm Song Finder[🎶](https://telegra.ph/file/34e13355f6753772d4e3f.mp4)\n\nSend the name of the song you want... 😍🥰🤗\n\nType /song song name\n\n𝐄𝐠. `/song Faded`"
    message.reply_text(
        text=Ytdl_Bot, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [[
              InlineKeyboardButton('Channel 👬', url='https://t.me/Malayalam_Music'),
              InlineKeyboardButton('Group 🤗', url='https://t.me/Malayalam_Musics')
            ]]
        )
    )
@bot.on_message(filters.command(['song']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🔎 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 𝐭𝐡𝐞 𝐬𝐨𝐧𝐠...')
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

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

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
    m.edit("Processing")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"🎵 Sᴏɴɢ Uᴘʟᴏᴀᴅᴇᴅ ғʀᴏᴍ YᴏᴜTᴜʙᴇ Mᴜsɪᴄ..!.\n\nPᴏᴡᴇʀᴇᴅ ʙʏ [{bat}](https://t.me/{Config.bn})"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("📤 υρℓσα∂ιиg fιℓє тσ тєℓєgяαм...")
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
        m.edit("❌ Error Contact support Group") 
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


bot.run()
