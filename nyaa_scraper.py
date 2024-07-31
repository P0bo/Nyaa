import requests
from bs4 import BeautifulSoup
import json
import sys

class Constants:
    NyaaBaseUrl = "https://nyaa.si"
    NyaaAltUrl = "https://nyaa.smartass08.xyz"
    DefaultProfilePic = "https://raw.githubusercontent.com/Yash-Garg/Nyaa-Api-Go/dev/static/default.png"

def fetch_torrent_info(torrent_id):
    url = f"{Constants.NyaaBaseUrl}/view/{torrent_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch torrent info")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    container = soup.find('body').find_all('div', class_='container')[-1]

    torrent_data = {
        "id": int(torrent_id),
        "title": container.find('h3', class_='panel-title').text.strip(),
        "file": Constants.NyaaBaseUrl + container.find('div', class_='panel-footer').find('a')['href'],
        "link": f"{Constants.NyaaBaseUrl}/view/{torrent_id}",
        "magnet": container.find('div', class_='panel-footer').find_all('a')[1]['href'],
        "size": container.find_all('div', class_='row')[3].find_all('div')[1].text.strip(),
        "category": container.find_all('div', class_='row')[0].find_all('div')[1].text.strip(),
        "uploaded": container.find_all('div', class_='row')[0].find_all('div')[3].text.strip(),
        "seeders": int(container.find_all('div', class_='row')[1].find_all('div')[3].text.strip()),
        "leechers": int(container.find_all('div', class_='row')[2].find_all('div')[3].text.strip()),
        "completed": int(container.find_all('div', class_='row')[3].find_all('div')[3].text.strip())
    }

    comment_section = container.find('div', id='comments')
    comment_count = int(comment_section.find('h3', class_='panel-title').text.split('-')[-1].strip())
    comments = []

    if comment_count > 0:
        comment_panels = comment_section.find_all('div', class_='comment-panel')
        for panel in comment_panels:
            body = panel.find('div', class_='panel-body')
            comment = {
                "name": body.find('a').text.strip(),
                "content": body.find('div', class_='comment-body').find('div', class_='comment-content').text.strip(),
                "image": body.find('img', class_='avatar')['src'] if body.find('img', class_='avatar') else Constants.DefaultProfilePic,
                "timestamp": body.find('a').find('time').text.strip()
            }
            comments.append(comment)

    file_info = {
        "torrent": torrent_data,
        "description": container.find('div', id='torrent-description').text.strip(),
        "submittedBy": container.find_all('div', class_='row')[1].find_all('div')[1].text.strip(),
        "infoHash": container.find_all('div', class_='row')[4].find_all('div')[1].text.strip(),
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
