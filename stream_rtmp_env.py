import os
import time

# Ambil environment variables
INPUT_URL = os.getenv("INPUT_URL")
RTMP_URL = os.getenv("RTMP_URL")
WATERMARK_TEXT = os.getenv("WATERMARK_TEXT", "TipiStream")
REFERER = os.getenv("REFERER")
USER_AGENT = os.getenv("USER_AGENT")
ORIGIN = os.getenv("ORIGIN")

# Bangun command Streamlink + FFmpeg
streamlink_cmd = f'streamlink --stdout'
if REFERER:
    streamlink_cmd += f' --http-header "Referer={REFERER}"'
if USER_AGENT:
    streamlink_cmd += f' --http-header "User-Agent={USER_AGENT}"'
if ORIGIN:
    streamlink_cmd += f' --http-header "Origin={ORIGIN}"'
streamlink_cmd += f' "{INPUT_URL}" best'

ffmpeg_cmd = f'ffmpeg -re -i - -vf "drawtext=text=\'{WATERMARK_TEXT}\':fontcolor=white:fontsize=14:x=10:y=10" ' \
             f'-c:v libx264 -preset veryfast -c:a aac -b:a 64k -f flv "{RTMP_URL}"'

full_cmd = f'{streamlink_cmd} | {ffmpeg_cmd}'

print(f"Streaming {INPUT_URL} → {RTMP_URL} dengan watermark '{WATERMARK_TEXT}'")

# Loop auto-retry
while True:
    exit_code = os.system(full_cmd)
    if exit_code == 0:
        print("✅ Streaming selesai tanpa error. Keluar.")
        break
    else:
        print("⚠️ Streaming terputus, mencoba ulang dalam 5 detik...")
        time.sleep(5)
