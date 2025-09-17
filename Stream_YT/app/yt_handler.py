import yt_dlp
import os
from config import YOUTUBE_URL, COOKIES_FILE

def get_m3u8_url():
    """
    Get the best m3u8 (HLS) URL for the given YouTube video.
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'cookiefile': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
        'format': 'bestaudio+bestvideo/best',
        'force_generic_extractor': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(YOUTUBE_URL, download=False)
        # Try to find an m3u8 URL in formats
        for f in info.get('formats', []):
            if f.get('protocol') == 'm3u8_native' or f.get('protocol') == 'm3u8':
                return f['url']

        # fallback: just return the video URL
        return info['url']
