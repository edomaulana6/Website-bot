import os
import yt_dlp
import logging
import sys
import random
import time
from types import ModuleType

# BYPASS UNTUK PYTHON 3.12+
try:
    import imghdr
except ImportError:
    sys.modules['imghdr'] = ModuleType('imghdr')

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# Setup Log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8521111355:AAFBex2-KpJ5M15X-QdX3qD9WU4tTr0WCiA"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

def start(update, context):
    update.message.reply_text("👑 **Bot Sultan Aktif!**\n\nKetik judul lagu atau kirim link. Saya download dulu ke VPS baru saya kirim ke kamu.", parse_mode='Markdown')

def handle_message(update, context):
    query = update.message.text
    if "http" in query:
        download_and_send(update.message, query, type='video' if 'tiktok' in query or 'shorts' in query else 'audio')
        return

    status_msg = update.message.reply_text(f"🔍 Mencari: '{query}'...")
    ydl_opts = {'quiet': True, 'default_search': 'ytsearch5', 'no_warnings': True, 'user_agent': random.choice(USER_AGENTS)}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(query, download=False).get('entries', [])
            if not results:
                status_msg.edit_text("❌ Tidak ditemukan.")
                return

            keyboard = [[InlineKeyboardButton(f"🎵 {v.get('title')[:40]}", callback_data=f"dl|{v.get('webpage_url')}")] for v in results]
            status_msg.edit_text("✨ Pilih lagu untuk didownload:", reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            status_msg.edit_text("❌ Terjadi kesalahan.")

def button_callback(update, context):
    query = update.callback_query
    if query.data.startswith("dl|"):
        url = query.data.split("|")[1]
        query.edit_message_text("📥 Sedang mendownload ke VPS... Mohon tunggu.")
        download_and_send(query.message, url, type='audio', is_callback=True)

def download_and_send(message_obj, url, type='audio', is_callback=False):
    if not os.path.exists('downloads'): os.makedirs('downloads')
    filename = f"downloads/file_{int(time.time())}"
    
    ydl_opts = {
        'format': 'bestaudio/best' if type == 'audio' else 'best',
        'outtmpl': f'{filename}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        'user_agent': random.choice(USER_AGENTS),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            actual_file = f"{filename}.{info.get('ext')}"
            
            with open(actual_file, 'rb') as f:
                if type == 'audio':
                    message_obj.reply_audio(audio=f, title=info.get('title'), performer=info.get('uploader'))
                else:
                    message_obj.reply_video(video=f, caption=f"✅ {info.get('title')}")

            if os.path.exists(actual_file):
                os.remove(actual_file)
            if is_callback: message_obj.delete()
        except Exception as e:
            message_obj.reply_text(f"⚠️ Gagal: {str(e)[:50]}")

def main():
    print("--- MEMULAI BOT ---")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(button_callback))
    print("✅ Bot Sultan Berhasil Jalan!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
