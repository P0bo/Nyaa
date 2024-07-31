import requests
from bs4 import BeautifulSoup
import json
import sys

class Constants:
    NyaaBaseUrl = "https://nyaa.si"
    DefaultProfilePic = "https://i.imgur.com/TKkz0qM.png"

def fetch_torrent_info(torrent_id):
    url = f"{Constants.NyaaBaseUrl}/view/{torrent_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch torrent info for ID {torrent_id}. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    panel = soup.find('div', class_='panel panel-default')

    if not panel:
        print("No panel found. The structure might be different.")
        return

    print("Panel found")

    rows = panel.find_all('div', class_='row')

    try:
        torrent_data = {
            "id": int(torrent_id),
            "title": panel.find('h3', class_='panel-title').text.strip() if panel.find('h3', class_='panel-title') else "Unknown Title",
            # Use the correct attribute and structure to get the file and magnet links
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
        print("An error occurred while accessing panel data:", e)
        return

    print("Torrent data extracted:", torrent_data)

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

    # In the new structure, comments are missing
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

    with open(f"{torrent_id}.json", "w", encoding='utf-8') as f:
        json.dump(file_info, f, ensure_ascii=False, indent=4)

    print(f"Information saved to {torrent_id}.json")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python nyaa_scraper.py <id>")
        sys.exit(1)

    torrent_id = sys.argv[1]
    fetch_torrent_info(torrent_id)
