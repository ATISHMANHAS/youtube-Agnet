import os
import json
import subprocess
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

UPLOAD_FOLDER = "shorts"
UPLOADED_LOG = "uploaded_videos.json"
MAX_UPLOADS = 6
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Trending hashtags to append
TRENDING_HASHTAGS = "#shorts #trending #viral #funny #catshorts #football #cricket #mrbeast #gaming"

# Long description for each short
LONG_DESCRIPTION = (
    "🎬 Enjoy daily viral shorts from the world of ⚽ football, 🏏 cricket, 🎮 gaming, 😺 cat moments, and more!\n"
    "🔥 Don’t forget to like, share & subscribe for your daily dose of fun!\n\n"
    "#Shorts #Viral #Trending #FootballShorts #CricketShorts #MrBeastShorts "
    "#GamingShorts #CatShorts #AnimeEdits #FunnyReels #FYP #ExplorePage #DailyShorts"
)

def generate_title_from_filename(filename):
    base = os.path.splitext(filename)[0].lstrip("_").replace("_", " ").strip().capitalize()
    if not base:
        base = "Amazing Short"
    full_title = f"{base} {TRENDING_HASHTAGS}"
    return full_title[:95]  # Safe within YouTube's limit

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

def load_uploaded_videos():
    if not os.path.exists(UPLOADED_LOG):
        return []
    with open(UPLOADED_LOG, 'r') as f:
        return json.load(f)

def save_uploaded_videos(uploaded):
    with open(UPLOADED_LOG, 'w') as f:
        json.dump(uploaded, f, indent=2)

def upload_video(youtube, filepath, title, description, tags):
    print(f"🚀 Uploading: {title}")
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22',
        },
        'status': {
            'privacyStatus': 'public',
            'madeForKids': False,
        }
    }
    media = MediaFileUpload(filepath, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    response = request.execute()
    print(f"✅ Uploaded: https://www.youtube.com/watch?v={response['id']}")
    return response['id']

def main():
    creds = authenticate()
    youtube = build("youtube", "v3", credentials=creds)

    uploaded = load_uploaded_videos()
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".mp4")]
    files_to_upload = [f for f in files if f not in uploaded and "_720p" not in f][:MAX_UPLOADS]

    if not files_to_upload:
        print("📭 No new videos to upload.")
        return

    for filename in files_to_upload:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        try:
            title = generate_title_from_filename(filename)
            tags = ["shorts", "fun", "trending", "football", "mrbeast", "cricket", "youtube", "catshorts", "ai", "gaming"]

            video_id = upload_video(youtube, filepath, title, LONG_DESCRIPTION, tags)
            uploaded.append(filename)
            save_uploaded_videos(uploaded)
        except Exception as e:
            print(f"❌ Failed to upload {filename}: {e}")

if __name__ == "__main__":
    main()
