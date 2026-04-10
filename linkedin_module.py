import requests
from urllib.parse import urlparse
import os

API_KEY = os.getenv("RAPID_API_KEY") 


def extract_company_name(url):
    path = urlparse(url).path
    parts = path.split("/")

    if "company" in parts:
        idx = parts.index("company")
        return parts[idx + 1]

    return None


def get_linkedin_data(url):
    try:
        # 🔍 Extract company name
        company = extract_company_name(url)

        if not company:
            return [{"error": "Invalid LinkedIn URL"}]

        print("COMPANY:", company)

        # 🔥 API endpoint (from your snippet)
        api_url = "https://linkedin-jobs-data-api.p.rapidapi.com/company/posts"

        querystring = {
            "company_name": company
        }

        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": "linkedin-jobs-data-api.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        # 📡 API call
        response = requests.get(api_url, headers=headers, params=querystring)

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            print("ERROR:", response.text)
            return [{"error": "LinkedIn API failed"}]

        data = response.json()
        print("FULL JSON:", data)

        # 🔥 CORRECT PATH (MAIN FIX)
        posts = data.get("data", {}).get("posts", [])

        result = []

        # ✅ Get latest 5 posts
        for post in posts[:10]:
            caption = post.get("text", "No caption")
            link = post.get("post_url", "")
            time = post.get("posted_at", {}).get("date", "No time")

            result.append({
                "caption": caption,
                "link": link,
                "time": time
            })

        print("FINAL RESULT:", result)
        return result

    except Exception as e:
        print("ERROR:", str(e))
        return [{"error": "Something went wrong"}]