import os
import yt_dlp
import logging
import sys
import random
import time
import hashlib
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

TOKEN = "masukan token tele"

# Database sementara untuk URL
url_storage = {}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

def start(update, context):
    update.message.reply_text("👑 **Bot Sultan Aktif!**\n\nKetik judul lagu atau kirim link. Saya download dulu ke VPS baru saya kirim ke kamu.", parse_mode='Markdown')

def handle_message(update, context):
    query = update.message.text
    if "http" in query:
        status_msg = update.message.reply_text("⌛ Menyiapkan pratinjau...")
        
        ydl_opts = {'quiet': True, 'no_warnings': True, 'user_agent': random.choice(USER_AGENTS)}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Ambil data thumbnail & judul tanpa download filenya
                info = ydl.extract_info(query, download=False)
                title = info.get('title', 'Video/Audio')
                thumbnail = info.get('thumbnail')
                
                url_id = hashlib.md5(query.encode()).hexdigest()[:8]
                url_storage[url_id] = query
                
                keyboard = [
                    [
                        InlineKeyboardButton("📹 Unduh Video", callback_data=f"choice|video|{url_id}"),
                        InlineKeyboardButton("🎧 Unduh Audio", callback_data=f"choice|audio|{url_id}")
                    ]
                ]
                
                # Kirim Thumbnail sebagai foto dengan caption dan tombol
                if thumbnail:
                    update.message.reply_photo(
                        photo=thumbnail,
                        caption=f"🎬 **{title}**\n\nSilakan pilih format unduhan:",
                        reply_markup=InlineKeyboardMarkup(keyboard),
                        parse_mode='Markdown'
                    )
                else:
                    update.message.reply_text(
                        f"🎬 **{title}**\n\nSilakan pilih format unduhan:",
                        reply_markup=InlineKeyboardMarkup(keyboard),
                        parse_mode='Markdown'
                    )
                
                status_msg.delete() # Hapus pesan loading
                return
            except Exception as e:
                status_msg.edit_text(f"❌ Gagal mengambil info: {str(e)[:50]}")
                return

    # Logika pencarian judul (Tetap sama)
    status_msg = update.message.reply_text(f"🔍 Mencari: '{query}'...")
    ydl_opts = {'quiet': True, 'default_search': 'ytsearch5', 'no_warnings': True, 'user_agent': random.choice(USER_AGENTS)}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(query, download=False).get('entries', [])
            if not results:
                status_msg.edit_text("❌ Tidak ditemukan.")
                return

            keyboard = [[InlineKeyboardButton(f"🎵 {v.get('title')[:40]}", callback_data=f"dl|{v.get('webpage_url')}")] for v in results]
            status_msg.edit_text("✨ Pilih lagu untuk didownload (Otomatis Audio):", reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            status_msg.edit_text("❌ Terjadi kesalahan.")

def button_callback(update, context):
    query = update.callback_query
    if query.data.startswith("choice|"):
        _, fmt, url_id = query.data.split("|")
        url = url_storage.get(url_id)
        if url:
            # Mengubah caption foto agar user tahu proses sedang berjalan
            query.edit_message_caption(caption=f"📥 Sedang memproses {fmt.upper()}... Mohon tunggu.")
            download_and_send(query.message, url, type=fmt, is_callback=True)
        else:
            query.answer("⚠️ Link kadaluwarsa. Kirim ulang linknya.", show_alert=True)
            
    elif query.data.startswith("dl|"):
        url = query.data.split("|")[1]
        query.edit_message_text("📥 Sedang mendownload ke VPS... Mohon tunggu.")
        download_and_send(query.message, url, type='audio', is_callback=True)

def download_and_send(message_obj, url, type='audio', is_callback=False):
    if not os.path.exists('downloads'): os.makedirs('downloads')
    filename = f"downloads/file_{int(time.time())}"
    
    ydl_opts = {
        'format': 'bestaudio/best' if type == 'audio' else 'bestvideo+bestaudio/best',
        'outtmpl': f'{filename}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'user_agent': random.choice(USER_AGENTS),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            actual_file = f"{filename}.{info.get('ext')}"
            
            if not os.path.exists(actual_file):
                import glob
                files = glob.glob(f"{filename}.*")
                if files: actual_file = files[0]

            with open(actual_file, 'rb') as f:
                if type == 'audio':
                    message_obj.reply_audio(audio=f, title=info.get('title'), performer=info.get('uploader'))
                else:
                    message_obj.reply_video(video=f, caption=f"✅ {info.get('title')}")

            if os.path.exists(actual_file):
                os.remove(actual_file)
            
            # Hapus pesan tombol setelah file dikirim
            if is_callback: 
                try: message_obj.delete()
                except: pass
        except Exception as e:
            message_obj.reply_text(f"⚠️ Gagal: {str(e)[:50]}")

def main():
    print("--- BOT SULTAN RUNNING ---")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(button_callback))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
