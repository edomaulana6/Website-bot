#!/bin/bash

# --- CONFIGURATION ---
BOT_DIR=$(pwd)
DOWNLOAD_DIR="$BOT_DIR/downloads"

echo "------------------------------------------------"
echo "🛠️ SISTEM PERBAIKAN & OPTIMASI BOT SULTAN 🛠️"
echo "------------------------------------------------"

# 1. Update Core Components (Mencegah Error YouTube ganti algoritma)
echo "🚀 Memperbarui library (yt-dlp & telegram)..."
pip install -U pip yt-dlp python-telegram-bot --quiet

# 2. Membersihkan Proses Hantu (Ghost Processes)
echo "👻 Membersihkan proses gantung (yt-dlp)..."
pkill -f yt-dlp
pkill -f ffmpeg

# 3. Reset Storage (Mencegah Disk VPS Penuh)
echo "📂 Membersihkan sampah download..."
if [ -d "$DOWNLOAD_DIR" ]; then
    rm -rf "$DOWNLOAD_DIR"/*
else
    mkdir -p "$DOWNLOAD_DIR"
fi

# 4. Verifikasi FFmpeg (Jantungnya download video)
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️ FFmpeg tidak ditemukan! Menginstal sekarang..."
    sudo apt update && sudo apt install ffmpeg -y
else
    echo "✅ FFmpeg sudah siap."
fi

echo "------------------------------------------------"
echo "✅ SEMUA ERROR TERATASI! Silakan jalankan bot."
echo "------------------------------------------------"
