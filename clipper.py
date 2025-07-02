import os
import json
import random
import subprocess
from yt_dlp import YoutubeDL

# Constants
JSON_FILE = "Data/daily_video_list.json"
OUTPUT_FOLDER = "shorts"
MAX_CLIPS = 6
MAX_SHORT_LENGTH = 60  # seconds

# Create output folder if not exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load video list from JSON
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Process up to MAX_CLIPS
for idx, short in enumerate(data[:MAX_CLIPS]):
    title = short["title"]
    url = short["url"]

    print(f"\n🎬 Short #{idx + 1}: {title}")
    print(f"🔗 {url}")

    # Generate safe filenames
    safe_title = "".join(c if c.isalnum() else "_" for c in title.lower())
    output_final = os.path.join(OUTPUT_FOLDER, f"{safe_title}_short.mp4")

    try:
        # Get full video metadata
        ydl_opts_meta = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True
        }

        with YoutubeDL(ydl_opts_meta) as ydl:
            info = ydl.extract_info(url, download=False)
            full_duration = info.get('duration', 120)

        # Auto decide best cut point under 60s
        if full_duration <= MAX_SHORT_LENGTH:
            start = 0
            duration = full_duration
        elif full_duration <= 120:
            start = random.randint(5, 20)
            duration = min(MAX_SHORT_LENGTH, full_duration - start)
        else:
            start = random.randint(20, full_duration - MAX_SHORT_LENGTH)
            duration = MAX_SHORT_LENGTH

        print(f"⏱️ Cutting from {start}s for {duration}s")

        # Download full video
        ydl_opts_download = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': os.path.join(OUTPUT_FOLDER, f"{safe_title}_full.%(ext)s"),
            'quiet': True
        }

        with YoutubeDL(ydl_opts_download) as ydl:
            result = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(result)

        # Trim and resize to 1080x1920
        temp_trimmed = os.path.join(OUTPUT_FOLDER, f"{safe_title}_trimmed.mp4")
        subprocess.run([
            'ffmpeg', '-y',
            '-ss', str(start),
            '-i', filename,
            '-t', str(duration),
            '-vf', "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-c:a', 'aac', '-b:a', '128k',
            temp_trimmed
        ], check=True)

        os.rename(temp_trimmed, output_final)
        os.remove(filename)
        print(f"✅ Saved: {output_final}")

    except Exception as e:
        print(f"❌ Failed: {title} - {e}")
