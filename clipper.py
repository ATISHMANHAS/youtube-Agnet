import os
import subprocess
import json
from pathlib import Path

# Path to your JSON video list
VIDEO_DATA_PATH = "daily_video_list.json"
# Output folder for shorts
OUTPUT_DIR = "shorts"

# Create output directory if not exists
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def clip_video(url, start_time, end_time, output_path):
    """
    Use ffmpeg to clip video with audio
    """
    command = [
        "yt-dlp",
        "--download-sections", f"*{start_time}-{end_time}",
        "-f", "bv*+ba/b",
        "-o", output_path,
        url
    ]

    print(f"🎬 Clipping {url} [{start_time}s - {end_time}s]")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"❌ Failed to clip {url}: {result.stderr.splitlines()[-1]}")
    else:
        print(f"✅ Saved: {output_path}\n")

def main():
    print("🎬 Starting clipping...\n")

    if not os.path.exists(VIDEO_DATA_PATH):
        print(f"❌ File not found: {VIDEO_DATA_PATH}")
        return

    with open(VIDEO_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for category in data:
        title = category.get("title", "untitled")
        url = category.get("url")
        start = category.get("start", 0)
        end = category.get("end", start + 20)

        # Create filename and check if already exists
        safe_title = "".join(c if c.isalnum() else "_" for c in title.lower())
        filename = f"{safe_title}_short.mp4"
        output_path = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(output_path):
            print(f"⏩ Skipping already downloaded: {filename}")
            continue

        clip_video(url, start, end, output_path)

    print("✅ All done. Check your 'shorts/' folder.")

if __name__ == "__main__":
    main()
