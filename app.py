from flask import Flask, render_template, request
from instagram_module import get_instagram_data
from youtube_module import extract_username, get_channel_id, get_videos
from facebook_module import scrape_facebook
from linkedin_module import get_linkedin_data
import os 

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = []
    platform = ""

    if request.method == "POST":
        url = request.form["url"]
        print("USER INPUT URL:", url)

        # ✅ Basic validation
        if not url.startswith("http"):
            return render_template("index.html", result=[{"error": "Invalid URL"}])

        # 🎥 YOUTUBE
        if "youtube.com" in url or "youtu.be" in url:
            platform = "Youtube"
            try:
                username = extract_username(url)
                channel_id = get_channel_id(username)
                result = get_videos(channel_id)
            except Exception as e:
                print("YOUTUBE ERROR:", e)
                result = [{"error": "YouTube fetch failed"}]

        # 📸 INSTAGRAM
        elif "instagram.com" in url:
            platform = "Instagram"
            try:
                username = url.strip("/").split("/")[-1]
                print("USERNAME:", username)

                result = get_instagram_data(username)

            except Exception as e:
                print("INSTAGRAM ERROR:", e)
                result = [{"error": "Instagram fetch failed"}]

        # 📘 FACEBOOK
        elif "facebook.com" in url:
            platform = "Facebook"
            try:
                print("FACEBOOK URL:", url)
                result = scrape_facebook(url)

            except Exception as e:
                print("FACEBOOK ERROR:", e)
                result = [{"error": "Facebook fetch failed"}]


        #linkedin
        elif "linkedin.com" in url:
             platform = "Linkedin"
             print("LINKEDIN URL:", url)
             result = get_linkedin_data(url)

        # ❌ OTHER
        else:
            result = [{"error": "Platform not supported"}]

    print("FINAL RESULT:", result)

    return render_template("index.html", result=result, platform=platform)


    
port = int(os.environ.get("PORT", 10000))

app.run(host="0.0.0.0", port=port)