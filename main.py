
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
from config import Config

bot = Client(
    'YouTubeSongDownloader',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))



@bot.on_message(filters.command & filters.private(['start']))
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
    m.edit("Processing [🚀](https://telegra.ph/file/60b0489093120e762861f.mp4)")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎧 𝐓𝐢𝐭𝐥𝐞 : [{title[:35]}]({link})\n⏳ 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧 : `{duration}`\n🎬 𝐒𝐨𝐮𝐫𝐜𝐞 : [Youtube](https://youtu.be/3pN0W4KzzNY)\n👁‍🗨 𝐕𝐢𝐞𝐰𝐬 : `{views}`\n\n💌 @Malayalam_Music'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('❌ 𝐄𝐫𝐫𝐨𝐫')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
