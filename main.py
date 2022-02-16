
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
    Ytdl bot = f'👋 𝗛𝗲𝗹𝗹𝗼 @{message.from_user.username}\n\n𝗜 𝗔𝗺 🎸𓂀 𝕐συ𝕋υႦҽ 𝕊σɳɠ 𝔻σɯɳʅσαԃҽɾ[🎶](https://telegra.ph/file/34e13355f6753772d4e3f.mp4)\n\n𝗦𝗲𝗻𝗱 𝗧𝗵𝗲 𝗡𝗮𝗺𝗲 𝗢𝗳 𝗧𝗵𝗲 𝗦𝗼𝗻𝗴 𝗬𝗼𝘂 𝗪𝗮𝗻𝘁... 😍🥰🤗\n\n𝗧𝘆𝗽𝗲 /s 𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲\n\n𝐄𝐠. `/s Faded`'
    message.reply_text(
        text=Ytdl bot, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [[
              InlineKeyboardButton('Channel 👬', url='https://t.me/Malayalam_Music'),
              InlineKeyboardButton('Group 🤗', url='https://t.me/Malayalam_Musics')
            ]]
        )
    )
