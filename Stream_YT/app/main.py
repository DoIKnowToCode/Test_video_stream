from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import subprocess

from yt_handler import get_m3u8_url

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Go to /stream to watch video"}

@app.get("/stream")
async def stream_video():
    """
    Streams YouTube video as MP4 using ffmpeg to make it compatible with
    Windows Media Player Legacy and iOS AVPlayer.
    """
    m3u8_url = get_m3u8_url()

    ffmpeg_cmd = [
        "ffmpeg",
        "-i", m3u8_url,
        "-c:v", "libx264",    # Re-encode to H.264
        "-c:a", "aac",        # Re-encode to AAC
        "-preset", "veryfast",
        "-movflags", "frag_keyframe+empty_moov+faststart",  # enable streaming
        "-f", "mp4",
        "pipe:1"
    ]

    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE)

    return StreamingResponse(process.stdout, media_type="video/mp4")
