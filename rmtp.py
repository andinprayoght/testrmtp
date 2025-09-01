import os

def build_ffmpeg_command(m3u8_url, rtmp_url, referer=None, origin=None, user_agent=None):
    # Header opsional
    headers = []
    if referer:
        headers.append(f"Referer: {referer}")
    if origin:
        headers.append(f"Origin: {origin}")
    if user_agent:
        headers.append(f"User-Agent: {user_agent}")

    # Satukan header jadi satu string untuk -headers
    headers_str = ""
    if headers:
        headers_str = ' -headers "' + "\\r\\n".join(headers) + '\\r\\n"'

    # Command ffmpeg
    cmd = f'ffmpeg -i "{m3u8_url}"{headers_str} ' \
          f'-c:v libx264 -preset veryfast -b:v 2500k ' \
          f'-c:a aac -b:a 128k -ac 2 -ar 44100 ' \
          f'-f flv "{rtmp_url}"'
    return cmd

def main():
    print("=== Restream m3u8 → RTMP ===")

    # Input URL
    m3u8_url = input("Masukkan URL m3u8: ").strip()
    rtmp_url = input("Masukkan URL RTMP: ").strip()

    # Pilihan opsional
    use_referer = input("Tambahkan Referer? (y/n): ").strip().lower() == "y"
    referer = input("Referer: ").strip() if use_referer else None

    use_origin = input("Tambahkan Origin? (y/n): ").strip().lower() == "y"
    origin = input("Origin: ").strip() if use_origin else None

    use_agent = input("Tambahkan User-Agent? (y/n): ").strip().lower() == "y"
    user_agent = input("User-Agent: ").strip() if use_agent else None

    # Bangun command
    command = build_ffmpeg_command(m3u8_url, rtmp_url, referer, origin, user_agent)

    print("\nCommand yang dijalankan:\n")
    print(command)
    print("\nStreaming dimulai...\n")

    # Eksekusi
    os.system(command)

if __name__ == "__main__":
    main()
