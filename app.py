import os
import yt_dlp
import logging
# Menggunakan patch manual untuk imghdr agar stabil di Python 3.12+
import sys
try:
    import imghdr
except ImportError:
    # Solusi bypass untuk Python 3.12 yang menghapus imghdr
    from types import ModuleType
    sys.modules['imghdr'] = ModuleType('imghdr')

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CallbackQueryHandler

# Setup Log - Tetap dipertahankan untuk monitoring VPS
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# DATA TOKEN - Tetap tertanam sesuai permintaan Anda
TOKEN = "8521111355:AAFBex2-KpJ5M15X-QdX3qD9WU4tTr0WCiA"

def inline_query(update, context):
    query = update.inline_query.query
    if not query: return
    
    # Optimasi yt_dlp agar lebih cepat di VPS
    ydl_opts = {
        'quiet': True, 
        'default_search': 'ytsearch15', 
        'no_warnings': True,
        'source_address': '0.0.0.0' # Stabilizer untuk koneksi VPS
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(query, download=False).get('entries', [])
        except Exception as e:
            logging.error(f"Error fetching YouTube: {e}")
            results = []

    articles = []
    for i, video in enumerate(results):
        if not video: continue
        
        duration = video.get('duration', 0)
        # FITUR FILTER: Tetap dipertahankan (maksimal 10 menit)
        if 0 < duration <= 600:
            articles.append(
                InlineQueryResultArticle(
                    id=str(i),
                    title=video.get('title'),
                    description=f"⏱ {video.get('duration_string')} | {video.get('uploader')}",
                    thumb_url=video.get('thumbnail'),
                    input_message_content=InputTextMessageContent(video.get('webpage_url')),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🎥 Video HD", callback_data=f"v|{video.get('webpage_url')}")],
                        [InlineKeyboardButton("🎵 MP3 320kbps", callback_data=f"a|{video.get('webpage_url')}")]
                    ])
                )
            )
    update.inline_query.answer(articles)

def main():
    # Menggunakan use_context=True sesuai script asli Anda (v13.15)
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(InlineQueryHandler(inline_query))
    
    # Output keterangan lokasi diubah agar lebih umum untuk VPS
    print("✅ Bot Berhasil Dijalankan di VPS Alwaysdata!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
