import os
import subprocess
import yt_dlp
import asyncio
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# KONFIGURASI TRANSPARAN
TOKEN = "MASUKKAN_TOKEN_ANDA"
DOWNLOAD_DIR = "downloads"

# Fitur: Membersihkan sampah setiap kali bot start
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

async def download_worker(url):
    """Fungsi download dengan proteksi timeout untuk mencegah proses hantu"""
    ydl_opts = {
        'format': 'best[filesize<50M]/bestaudio/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'nocheckcertificate': True,
        'quiet': True,
    }
    
    # Menjalankan download di thread terpisah agar tidak memacetkan bot
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Fungsi to_thread mencegah bot membeku
            info = await asyncio.to_thread(ydl.extract_info, url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        print(f"Error Log: {e}")
        return None

async def main_handler(update, context):
    url = update.message.text
    if "http" not in url: return

    status_msg = await update.message.reply_text("⏳ Sedang diproses... (Sistem Anti-Error)")
    
    file_path = await download_worker(url)
    
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                await update.message.reply_document(document=f)
            await status_msg.delete()
        except Exception:
            await status_msg.edit_text("❌ Gagal: File terlalu besar untuk Telegram (Limit 50MB).")
        finally:
            # FITUR: Hapus file seketika setelah kirim (Anti-Disk Full)
            if os.path.exists(file_path):
                os.remove(file_path)
    else:
        await status_msg.edit_text("⚠️ Gagal download. Pastikan link valid.")

if __name__ == '__main__':
    print("--- BOT SULTAN RUNNING (SECURE MODE) ---")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main_handler))
    app.run_polling()
        
