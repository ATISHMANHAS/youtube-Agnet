import json
import datetime
import random
from yt_dlp import YoutubeDL
from pathlib import Path

# Define search categories and queries
video_categories = {
    "mrbeast": "mrbeast shorts",
    "football": "football shorts",
    "cricket": "cricket insane catches",
    "anime_edits": "cool anime edits with quotes",
    "cat_shorts": "funny cute cat shorts",
    "ishowspeed": "ishowspeed funny livestream clips"
}

DATA_DIR = Path("Data")
DATA_DIR.mkdir(exist_ok=True)

VIDEO_DATA_PATH = DATA_DIR / "daily_video_list.json"
SEEN_IDS_PATH = DATA_DIR / "seen_ids.json"

YDL_OPTIONS = {
    'quiet': True,
    'extract_flat': 'in_playlist',
    'skip_download': True,
    'forcejson': True,
}

# Load seen video IDs
if SEEN_IDS_PATH.exists():
    with open(SEEN_IDS_PATH, "r") as f:
        seen_ids = set(json.load(f))
else:
    seen_ids = set()

print("🎯 Collecting 1 video from each category...\n")

selected_videos = []

# Loop through each category and search
for category, search_query in video_categories.items():
    query = f"ytsearch10:{search_query}"
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(query, download=False)
            entries = info.get("entries", [])
            for entry in entries:
                video_id = entry.get("id")
                if video_id not in seen_ids:
                    seen_ids.add(video_id)

                    # Set start and end intelligently (max 60s)
                    start = random.randint(5, 40)
                    max_duration = 60
                    min_clip = 20
                    clip_length = random.randint(min_clip, max_duration - start)
                    end = start + clip_length

                    selected_videos.append({
                        "title": entry.get("title", f"{category}_video"),
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "category": category,
                        "start": start,
                        "end": end,
                        "fetched_at": datetime.datetime.now().isoformat()
                    })
                    break
            else:
                print(f"⚠️ No new video found for: {category}")
    except Exception as e:
        print(f"❌ Error fetching for {category}: {e}")

# Save selected video data
with open(VIDEO_DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(selected_videos, f, indent=2, ensure_ascii=False)

# Save seen video IDs
with open(SEEN_IDS_PATH, "w", encoding="utf-8") as f:
    json.dump(list(seen_ids), f, indent=2)

print(f"\n✅ Saved {len(selected_videos)} videos to {VIDEO_DATA_PATH}")
