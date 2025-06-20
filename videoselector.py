import json
from yt_dlp import YoutubeDL
from pathlib import Path
import datetime

video_categories = {
    "mrbeast": "mrbeast shorts",
    "fun": "funny shorts for kids",
    "facts": "animated facts for kids"
}

output_dir = Path("Data")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / "daily_video_list.json"

# ✅ Correct yt-dlp options for search
YDL_OPTIONS = {
    'quiet': True,
    'extract_flat': 'in_playlist',
    'skip_download': True,
    'forcejson': True,
}

all_videos = []

print("🔍 Collecting trending videos per category...\n")

for category, search_query in video_categories.items():
    search_term = f"ytsearch5:{search_query}"
    print(f"📁 Category: {category} | Searching: {search_term}")
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(search_term, download=False)
            videos = info.get('entries', [])

            if not videos:
                print(f"⚠️ No videos found for '{category}', skipping.\n")
                continue

            for i, entry in enumerate(videos[:2]):
                all_videos.append({
                    "url": f"https://www.youtube.com/watch?v={entry['id']}",
                    "title": entry.get("title", f"{category}_{i}"),
                    "category": category,
                    "fetched_at": datetime.datetime.now().isoformat()
                })

    except Exception as e:
        print(f"❌ Error fetching for {category}: {e}\n")

# Save result
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_videos, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved {len(all_videos)} videos to {output_file}")
