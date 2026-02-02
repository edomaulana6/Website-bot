import os
import yt_dlp
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CallbackQueryHandler

# Setup Log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# DATA TOKEN 100% AKURAT
TOKEN = "8521111355:AAFBex2-KpJ5M15X-QdX3qD9WU4tTr0WCiA"

def inline_query(update, context):
    query = update.inline_query.query
    if not query: return
    
    # Cari 15 hasil dari YouTube
    ydl_opts = {'quiet': True, 'default_search': 'ytsearch15', 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(query, download=False).get('entries', [])
        except:
            results = []

    articles = []
    for i, video in enumerate(results):
        duration = video.get('duration', 0)
        # LOGIKA FILTER: Hanya durasi di bawah atau sama dengan 600 detik (10 menit)
        if 0 < duration <= 600:
            articles.append(
                InlineQueryResultArticle(
                    id=str(i),
                    title=video.get('title'),
                    description=f"⏱ {video.get('duration_string')} | {video.get('uploader')}",
                    thumb_url=video.get('thumbnail'), # Munculkan Thumbnail (Garis Merah)
                    input_message_content=InputTextMessageContent(video.get('webpage_url')),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🎥 Video HD", callback_data=f"v|{video.get('webpage_url')}")],
                        [InlineKeyboardButton("🎵 MP3 320kbps", callback_data=f"a|{video.get('webpage_url')}")]
                    ])
                )
            )
    update.inline_query.answer(articles)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(InlineQueryHandler(inline_query))
    
    print("✅ Bot Berhasil Dijalankan di Koyeb!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
