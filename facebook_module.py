import requests
from urllib.parse import urlparse
import os

API_KEY = os.getenv("RAPID_API_KEY")

def extract_name(url):
    path = urlparse(url).path
    parts = path.split("/")

    # Case: /people/name/id
    if "people" in parts:
        idx = parts.index("people")
        return parts[idx + 1]

    # Case: normal username
    return parts[-1]


def scrape_facebook(url):
    try:
        name = extract_name(url)

        if not name:
            return [{"error": "Invalid Facebook URL"}]

        print("SEARCH NAME:", name)

        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": "facebook-scraper3.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        # 🔍 STEP 1: SEARCH PAGE
        search_url = "https://facebook-scraper3.p.rapidapi.com/search/pages"

        response = requests.get(search_url, headers=headers, params={"query": name})

        print("SEARCH STATUS:", response.status_code)

        if response.status_code != 200:
            print("ERROR:", response.text)
            return [{"error": "Search failed"}]

        data = response.json()
        print("SEARCH JSON:", data)

        pages = data.get("results", []) or data.get("data", [])

        if not pages:
            return [{"error": "Page not found"}]

        page_id = (
            pages[0].get("facebook_id")
            or pages[0].get("id")
            or pages[0].get("page_id")
        )
        print("PAGE ID:", page_id)

        if not page_id:
            return [{"error": "Page ID not found"}]

        # 📄 STEP 2: GET POSTS
        post_url = "https://facebook-scraper3.p.rapidapi.com/page/posts"

        response = requests.get(post_url, headers=headers, params={"page_id": page_id})

        print("POST STATUS:", response.status_code)

        if response.status_code != 200:
            print("ERROR:", response.text)
            return [{"error": "Posts fetch failed"}]

        data = response.json()
        print("POST JSON:", data)

        posts = data.get("data", []) or data.get("posts", [])

        if not posts:
            return [{
                "caption": "Facebook page found",
                "link": url,
                "time": "Click to view",
                "error": "No posts available"
            }]

        result = []

        for post in posts[:5]:
            result.append({
                "caption": post.get("text", "No caption"),
                "link": post.get("post_url", ""),
                "time": post.get("time", "No time")
            })

        print("FINAL RESULT:", result)
        return result

    except Exception as e:
        print("ERROR:", str(e))
        return [{"error": "Something went wrong"}]