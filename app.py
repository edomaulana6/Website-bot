import os
import time

def download_and_send(message_obj, url, type='audio', is_callback=False):
    # Buat folder download jika belum ada
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    # NAMA FILE UNIK AGAR TIDAK BENTROK
    filename = f"downloads/file_{int(time.time())}"
    
    ydl_opts = {
        'format': 'bestaudio/best' if type == 'audio' else 'best',
        'outtmpl': f'{filename}.%(ext)s', # DOWNLOAD FILENYA KE VPS
        'quiet': False, # Kita nyalakan log biar kelihatan di terminal
        'no_warnings': False,
        'nocheckcertificate': True,
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        'user_agent': random.choice(USER_AGENTS),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # PROSES DOWNLOAD NYATA
            info = ydl.extract_info(url, download=True)
            # Ambil path file yang baru didownload
            ext = info.get('ext')
            actual_file = f"{filename}.{ext}"
            title = info.get('title', 'Sultan_Music')

            # KIRIM FILENYA SEBAGAI DOKUMEN/AUDIO ASLI
            with open(actual_file, 'rb') as f:
                if type == 'audio':
                    message_obj.reply_audio(audio=f, title=title, performer=info.get('uploader'))
                else:
                    message_obj.reply_video(video=f, caption=f"✅ {title}")

            # HAPUS FILE DI VPS SETELAH TERKIRIM (BIAR GAK PENUH)
            os.remove(actual_file)
            
            if is_callback: message_obj.delete()

        except Exception as e:
            message_obj.reply_text(f"❌ Bot gagal narik file. Masalah: {str(e)[:100]}")
            # Bersihkan file sampah jika gagal
            if 'actual_file' in locals() and os.path.exists(actual_file):
                os.remove(actual_file)
    
