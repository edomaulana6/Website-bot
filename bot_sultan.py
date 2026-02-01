import telebot
import requests

# Masukkan Token asli Anda dari BotFather
API_TOKEN = '8521111355:AAEJ44UXZPE1rE3xK734pfTAOZHVNSaVNiw' # GANTI DENGAN TOKEN LENGKAP ANDA
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "✅ **Bot Sultan Aktif!**\n\nKirimkan link TikTok untuk mendownload video tanpa watermark secara gratis.")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text
    
    # Validasi jika link berasal dari TikTok
    if "tiktok.com" in url:
        bot.reply_to(message, "⏳ **Sedang memproses...** Tunggu sebentar ya Sultan.")
        
        try:
            # Menggunakan API TikWM yang stabil dan ringan
            api_url = f"https://www.tikwm.com/api/?url={url}"
            response = requests.get(api_url).json()
            
            if response.get('code') == 0:
                # Ambil URL video tanpa watermark
                video_url = "https://www.tikwm.com" + response['data']['play']
                caption = f"🎬 **Judul:** {response['data']['title']}\n👤 **User:** {response['data']['author']['nickname']}"
                
                # Kirim video langsung ke Telegram
                bot.send_video(message.chat.id, video_url, caption=caption)
            else:
                bot.reply_to(message, "❌ **Gagal!** Video tidak ditemukan atau link salah.")
        
        except Exception as e:
            bot.reply_to(message, f"❌ **Error:** Terjadi gangguan pada server API.")
    
    else:
        bot.reply_to(message, "⚠️ Sultan, tolong kirimkan link **TikTok** yang valid saja.")

# Memulai bot
print("Bot sedang berjalan...")
bot.infinity_polling()
