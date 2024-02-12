"""Extracts comments for a given Steam Community profile."""

from datetime import datetime
import math
import json
import sys
import requests
from bs4 import BeautifulSoup


def build_comment_url(steam64_id):
    """Build the URL for fetching comments based on Steam ID."""
    base_url = "https://steamcommunity.com/comment/Profile/render/"
    return f"{base_url}{steam64_id}/-1/"


def fetch_comments(steam64_id, start=0, page_size=6):
    """Fetch comments for a given Steam profile."""
    url = build_comment_url(steam64_id)
    headers = {
        "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        ),
    }
    payload = {"start": start, "count": page_size}
    response = requests.post(url, headers=headers, data=payload, timeout=10)
    if response.status_code == 200:
        return response.json()
    print(
        f"Failed to fetch comments for {steam64_id}, status code: {response.status_code}"
    )
    return None


def parse_comments_html(comments_html):
    """Parse HTML to extract comment details."""
    soup = BeautifulSoup(comments_html, "html.parser")
    comments = soup.find_all("div", class_="commentthread_comment_content")
    parsed_comments = []
    for comment in comments:
        author_tag = comment.find("a", class_="commentthread_author_link")
        author = author_tag.text.strip()
        author_link = author_tag["href"]
        text = comment.find("div", class_="commentthread_comment_text").text.strip()
        timestamp_tag = comment.find("span", class_="commentthread_comment_timestamp")
        timestamp = timestamp_tag["title"] if timestamp_tag else "Unknown date"
        parsed_comments.append(
            {
                "timestamp": timestamp,
                "text": text,
                "author": author,
                "author_link": author_link,
            }
        )
    return parsed_comments


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python steam.py <Steam64 ID>")
        sys.exit(1)

    STEAM64_ID_ARG = sys.argv[1]
    all_comments = []

    initial_data = fetch_comments(STEAM64_ID_ARG)
    if initial_data:
        total_count = int(initial_data.get("total_count", 0))
        PAGE_SIZE_ARG = 6
        total_pages = math.ceil(total_count / PAGE_SIZE_ARG)

        for page in range(total_pages):
            start_arg = page * PAGE_SIZE_ARG
            data = fetch_comments(STEAM64_ID_ARG, start=start_arg, page_size=PAGE_SIZE_ARG)
            comments_html_arg = data.get("comments_html", "") if data else ""
            page_comments = parse_comments_html(comments_html_arg)
            all_comments.extend(page_comments)

    current_date = datetime.now().strftime("%d%m%y")
    with open(
        f"steam_comments_{STEAM64_ID_ARG}_{current_date}.json", "w", encoding="utf-8"
    ) as json_file:
        json.dump(all_comments, json_file, indent=4, ensure_ascii=False)
