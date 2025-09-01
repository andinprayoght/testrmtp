import os
import time

# Default headers untuk rctiplus
DEFAULT_HEADERS = {
    "rctiplus.id": {
        "referer": "https://www.rctiplus.com",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
}

def main():
    print("=== Streamlink HLS → RTMP dengan Watermark ===")

    input_url = input("Masukkan URL master m3u8: ").strip()
    rtmp_url = input("Masukkan URL RTMP: ").strip()
    watermark_text = input("Text watermark (Enter = TipiStream): ").strip() or "TipiStream"

    # Set default headers jika rctiplus
    referer = user_agent = origin = None
    if "rctiplus.id" in input_url:
        referer = DEFAULT_HEADERS["rctiplus.id"]["referer"]
        user_agent = DEFAULT_HEADERS["rctiplus.id"]["user_agent"]
        print("⚡ Menambahkan default Referer dan User-Agent untuk rctiplus.id")

    # Opsi override manual
    use_referer = input("Override Referer? (y/n): ").strip().lower() == "y"
    if use_referer:
        referer = input("Referer: ").strip()

    use_agent = input("Override User-Agent? (y/n): ").strip().lower() == "y"
    if use_agent:
        user_agent = input("User-Agent: ").strip()

    use_origin = input("Tambahkan Origin? (y/n): ").strip().lower() == "y"
    if use_origin:
        origin = input("Origin: ").strip()

    # Bangun command Streamlink + FFmpeg
    streamlink_cmd = f'streamlink --stdout'
    if referer:
        streamlink_cmd += f' --http-header "Referer={referer}"'
    if user_agent:
        streamlink_cmd += f' --http-header "User-Agent={user_agent}"'
    if origin:
        streamlink_cmd += f' --http-header "Origin={origin}"'
    streamlink_cmd += f' "{input_url}" best'

    ffmpeg_cmd = f'ffmpeg -re -i - -vf "drawtext=text=\'{watermark_text}\':fontcolor=white:fontsize=14:x=10:y=10" ' \
                 f'-c:v libx264 -preset veryfast -c:a aac -b:a 64k -f flv "{rtmp_url}"'

    full_cmd = f'{streamlink_cmd} | {ffmpeg_cmd}'

    print("\nStreaming dimulai...\nTekan CTRL+C untuk berhenti.\n")

    # Loop auto-retry
    while True:
        exit_code = os.system(full_cmd)
        if exit_code == 0:
            print("✅ Streaming selesai tanpa error. Keluar.")
            break
        else:
            print("⚠️ Streaming terputus, mencoba ulang dalam 5 detik...")
            time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Dihentikan oleh user.")
