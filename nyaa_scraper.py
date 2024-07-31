import requests
from bs4 import BeautifulSoup
import json
import sys
import re

class Constants:
    NyaaBaseUrl = "https://nyaa.si"
    DefaultProfilePic = "https://i.imgur.com/TKkz0qM.png"

def sanitize_filename(name):
    """Remove disallowed characters from the filename."""
    # Define the allowed characters regex (CJK characters, alphanumeric, and specific symbols)
    allowed_chars = r'[^a-zA-Z0-9\(\)\[\]\.\,\-\_一-龥ぁ-ゔァ-ヴー々〆〤\u4E00-\u9FFF]'

    # Replace disallowed characters with underscores
    sanitized_name = re.sub(allowed_chars, '_', name)

    # Limit the filename length to avoid OS-specific issues
    return sanitized_name[:255]

def fetch_torrent_info(torrent_id):
    url = f"{Constants.NyaaBaseUrl}/view/{torrent_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Skipped {torrent_id}")
        return False

    soup = BeautifulSoup(response.text, 'html.parser')
    panel = soup.find('div', class_='panel panel-default')

    if not panel:
        print(f"Skipped {torrent_id} - No panel found.")
        return False

    rows = panel.find_all('div', class_='row')

    try:
        title = panel.find('h3', class_='panel-title').text.strip() if panel.find('h3', class_='panel-title') else "Unknown Title"
        torrent_data = {
            "id": int(torrent_id),
            "title": title,
            "file": Constants.NyaaBaseUrl + panel.find('a', href=lambda x: x and x.endswith('.torrent'))['href'] if panel.find('a', href=lambda x: x and x.endswith('.torrent')) else "Unknown File URL",
            "magnet": panel.find('a', href=lambda x: x and x.startswith('magnet:'))['href'] if panel.find('a', href=lambda x: x and x.startswith('magnet:')) else "Unknown Magnet URL",
            "size": rows[3].find_all('div', class_='col-md-5')[0].text.strip() if len(rows[3].find_all('div', class_='col-md-5')) > 0 else "Unknown Size",
            "category": rows[0].find_all('div', class_='col-md-5')[0].text.strip() if len(rows[0].find_all('div', class_='col-md-5')) > 0 else "Unknown Category",
            "uploaded": rows[0].find_all('div', class_='col-md-5')[1].text.strip() if len(rows[0].find_all('div', class_='col-md-5')) > 1 else "Unknown Upload Date",
            "seeders": int(rows[1].find_all('div', class_='col-md-5')[1].text.strip()) if len(rows[1].find_all('div', class_='col-md-5')) > 1 else 0,
            "leechers": int(rows[2].find_all('div', class_='col-md-5')[1].text.strip()) if len(rows[2].find_all('div', class_='col-md-5')) > 1 else 0,
            "completed": int(rows[3].find_all('div', class_='col-md-5')[1].text.strip()) if len(rows[3].find_all('div', class_='col-md-5')) > 1 else 0,
            "info_hash": rows[4].find('div', class_='col-md-5').text.strip() if rows[4].find('div', class_='col-md-5') else "Unknown Info Hash"
        }
    except IndexError as e:
        print(f"Skipped {torrent_id} - Error parsing data: {e}")
        return False

    description = soup.find('div', id='torrent-description').text.strip() if soup.find('div', id='torrent-description') else "No description available"
    comments_section = soup.find('div', id='comments')

    if comments_section:
        try:
            comment_count = int(comments_section.find('h3', class_='panel-title').text.split('-')[-1].strip())
        except (AttributeError, ValueError):
            comment_count = 0
    else:
        comment_count = 0

    comments = []

    if comment_count > 0:
        comment_panels = comments_section.find_all('div', class_='comment-panel')
        for panel in comment_panels:
            body = panel.find('div', class_='panel-body')
            if body:
                comment = {
                    "name": body.find('a').text.strip() if body.find('a') else "Unknown User",
                    "content": body.find('div', class_='comment-body').find('div', class_='comment-content').text.strip() if body.find('div', class_='comment-body') and body.find('div', class_='comment-body').find('div', class_='comment-content') else "No content"
                }
                comments.append(comment)

    file_info = {
        "torrent": torrent_data,
        "description": description,
        "commentInfo": {
            "count": comment_count,
            "comments": comments
        }
    }

    # Sanitize the title for a valid filename
    filename = sanitize_filename(title) + ".json"
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(file_info, f, ensure_ascii=False, indent=4)

    print(f"Fetched {torrent_id}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python nyaa_scraper.py <id_start-id_end>")
        sys.exit(1)

    id_range = sys.argv[1]
    try:
        start_id, end_id = map(int, id_range.split('-'))
    except ValueError:
        print("Invalid range format. Use <id_start-id_end>")
        sys.exit(1)

    for torrent_id in range(start_id, end_id + 1):
        fetch_torrent_info(torrent_id)
