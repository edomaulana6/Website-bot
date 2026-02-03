import os
import yt_dlp
import logging
import sys
import random
from types import ModuleType

# BYPASS UNTUK PYTHON 3.12+
try:
    import imghdr
except ImportError:
    sys.modules['imghdr'] = ModuleType('imghdr')

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8521111355:AAFBex2-KpJ5M15X-QdX3qD9WU4tTr0WCiA"

# Kumpulan User-Agent agar terlihat seperti manusia asli
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

def start(update, context):
    update.message.reply_text("🔥 **Bot Downloader Anti-Blokir Aktif!**\n\nKetik judul lagu atau kirim link apa saja, saya akan sikat habis.", parse_mode='Markdown')

def handle_message(update, context):
    query = update.message.text
    if "http" in query:
        status = update.message.reply_text("🚀 Menembus server... Mohon tunggu.")
        download_and_send(update.message, query, type='video' if 'tiktok' in query or 'shorts' in query else 'audio')
        status.delete()
        return

    status_msg = update.message.reply_text(f"🔍 Mencari daftar: '{query}'...")
    # Opsi pencarian yang lebih kuat
    ydl_opts = {
        'quiet': True, 
        'default_search': 'ytsearch5', 
        'no_warnings': True,
        'user_agent': random.choice(USER_AGENTS)
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(query, download=False).get('entries', [])
            if not results:
                status_msg.edit_text("❌ Tidak ditemukan hasil.")
                return

            keyboard = [[InlineKeyboardButton(f"🎵 {v.get('title')[:40]}", callback_data=f"dl|{v.get('webpage_url')}")] for v in results]
            status_msg.edit_text("✨ Pilih lagu (Langsung Kirim):", reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            status_msg.edit_text("❌ Server sibuk, coba lagi sebentar.")

def button_callback(update, context):
    query = update.callback_query
    if query.data.startswith("dl|"):
        url = query.data.split("|")[1]
        query.edit_message_text("📥 Sedang memproses file (Anti-Limit)...")
        download_and_send(query.message, url, type='audio', is_callback=True)

def download_and_send(message_obj, url, type='audio', is_callback=False):
    # KONFIGURASI PALING BANDEL
    ydl_opts = {
        'format': 'bestaudio/best' if type == 'audio' else 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True, # Abaikan error SSL
        'source_address': '0.0.0.0', # Gunakan IP VPS secara stabil
        'user_agent': random.choice(USER_AGENTS), # Rotasi identitas
        'socket_timeout': 30, # Jangan mudah menyerah jika lemot
        'retries': 10, # Coba lagi 10 kali jika gagal
        'fragment_retries': 10,
        'extract_flat': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            file_url = info.get('url')
            title = info.get('title', 'file')

            if type == 'audio':
                message_obj.reply_audio(audio=file_url, title=title, performer=info.get('uploader'))
            else:
                message_obj.reply_video(video=file_url, caption=f"✅ {title}")
            
            if is_callback: message_obj.delete()
        except Exception as e:
            message_obj.reply_text(f"⚠️ Server sedang proteksi ketat. Gunakan link lain.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(button_callback))
    print("✅ Bot Paling Bandel Berhasil Dijalankan!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
                              
