import os
import requests
import re
import time

def get_sub_playlists(master_url):
    """
    Ambil semua sub-playlist dari master m3u8.
    Mengembalikan list tuple: (bitrate_kbps, sub_playlist_url)
    """
    try:
        r = requests.get(master_url, timeout=10)
        r.raise_for_status()
        content = r.text
    except Exception as e:
        print("Gagal ambil master playlist:", e)
        return []

    # Cari URL sub-playlist dan bitrate
    pattern = re.compile(r'#EXT-X-STREAM-INF:.*BANDWIDTH=(\d+).*?\n(.*\.m3u8)')
    matches = pattern.findall(content)
    playlists = []
    for bw, url in matches:
        if not url.startswith("http"):
            # Buat URL absolute jika relative
            url = os.path.join(os.path.dirname(master_url), url)
        playlists.append((int(bw)//1000, url))  # bitrate dalam kbps
    return playlists

def build_ffmpeg_command(sub_url, rtmp_url, referer=None, origin=None, user_agent=None, v_bitrate="2500k"):
    headers = []
    if referer:
        headers.append(f"Referer: {referer}")
    if origin:
        headers.append(f"Origin: {origin}")
    if user_agent:
        headers.append(f"User-Agent: {user_agent}")

    headers_str = ""
    if headers:
        headers_str = ' -headers "' + "\\r\\n".join(headers) + '\\r\\n"'

    cmd = f'ffmpeg -re -i "{sub_url}"{headers_str} ' \
          f'-c:v libx264 -preset veryfast -b:v {v_bitrate} ' \
          f'-c:a aac -b:a 128k -ac 2 -ar 44100 ' \
          f'-f flv "{rtmp_url}"'
    return cmd

def main():
    print("=== Restream m3u8 → RTMP (Pilih Sub-Playlist) ===")

    master_url = input("Masukkan URL master m3u8: ").strip()
    rtmp_url = input("Masukkan URL RTMP: ").strip()

    playlists = get_sub_playlists(master_url)
    if playlists:
        print("\nDaftar bitrate tersedia:")
        for idx, (bw, url) in enumerate(playlists, start=1):
            print(f"{idx}. {bw} kbps → {url}")

        pilih = input("Pilih nomor playlist (Enter = default 1): ").strip()
        if pilih.isdigit() and 1 <= int(pilih) <= len(playlists):
            sub_url = playlists[int(pilih)-1][1]
        else:
            sub_url = playlists[0][1]
    else:
        print("Tidak ditemukan sub-playlist, pakai master URL.")
        sub_url = master_url

    # Opsional headers
    use_referer = input("Tambahkan Referer? (y/n): ").strip().lower() == "y"
    referer = input("Referer: ").strip() if use_referer else None

    use_origin = input("Tambahkan Origin? (y/n): ").strip().lower() == "y"
    origin = input("Origin: ").strip() if use_origin else None

    use_agent = input("Tambahkan User-Agent? (y/n): ").strip().lower() == "y"
    user_agent = input("User-Agent: ").strip() if use_agent else None

    # Optional video bitrate custom
    v_bitrate = input("Bitrate video (contoh 2500k) [Enter = 2500k]: ").strip() or "2500k"

    command = build_ffmpeg_command(sub_url, rtmp_url, referer, origin, user_agent, v_bitrate)

    print("\nStreaming dimulai...\nTekan CTRL+C untuk berhenti.\n")

    # Loop auto-retry
    while True:
        exit_code = os.system(command)
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
