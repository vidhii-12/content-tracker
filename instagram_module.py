import requests
import datetime
import os

API_KEY = os.getenv("RAPID_API_KEY")

def get_instagram_data(username):
    url = "https://instagram120.p.rapidapi.com/api/instagram/posts"

    payload = {
        "username": username,
        "maxId": ""
    }

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "instagram120.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("STATUS:", response.status_code)

    if response.status_code != 200:
        print("ERROR:", response.text)
        return [{"error": "API failed"}]

    data = response.json()

    result = []

    try:
        posts = data.get("result", {}).get("edges", [])

        for post in posts[:10]:  # limit to 5
            node = post.get("node", {})

            caption = node.get("caption", {}).get("text", "No caption")

            link = f"https://www.instagram.com/p/{node.get('code')}"

            

            timestamp = node.get("taken_at", None)

            if timestamp:
                time = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            else:
                 time = "No time"

            result.append({
                "caption": caption,
                "link": link,
                "time": time
            })

    except Exception as e:
        print("PARSE ERROR:", e)
        return [{"error": "Parsing failed"}]

    print("FINAL RESULT:", result)

    return result