import requests
from bs4 import BeautifulSoup
import json
import time


class Constants:
    NyaaBaseUrl = "https://nyaa.si"
    NyaaAltUrl = "https://nyaa.smartass08.xyz"
    DefaultProfilePic = "https://raw.githubusercontent.com/Yash-Garg/Nyaa-Api-Go/dev/static/default.png"

    NyaaEndpoints = {
        "all": {"all": "0_0"},
        "anime": {"all": "1_0", "amv": "1_1", "eng": "1_2", "non-eng": "1_3", "raw": "1_4"},
        "audio": {"all": "2_0", "lossless": "2_1", "lossy": "2_2"},
        "manga": {"all": "3_0", "eng": "3_1", "non-eng": "3_2", "raw": "3_3"},
        "live_action": {"all": "4_0", "eng": "4_1", "promo": "4_2", "non-eng": "4_3", "raw": "4_4"},
        "pictures": {"all": "5_0", "graphics": "5_1", "photos": "5_2"},
        "software": {"all": "6_0", "applications": "6_1", "games": "6_2"},
    }


def check_nyaa_url():
    try:
        resp = requests.get(Constants.NyaaBaseUrl)
        if resp.status_code == 200:
            return Constants.NyaaBaseUrl
        else:
            return Constants.NyaaAltUrl
    except Exception as e:
        print("Error checking Nyaa URL:", str(e))
        return Constants.NyaaAltUrl


def get_category_id(cat, subcat):
    if subcat is None:
        return Constants.NyaaEndpoints[cat]["all"]
    else:
        return Constants.NyaaEndpoints[cat][subcat]


def file_info_scraper(url):
    response = requests.get(url)
    if response.status_code == 200:
        response_body = response.text
        soup = BeautifulSoup(response_body, 'html.parser')
        container = soup.find_all("div", class_="container")[-1]
        file_id = int(url.split("/")[4])

        torrent_data = {
            'title': container.find("h3", class_="panel-title").text.strip(),
            'file': Constants.NyaaBaseUrl + container.find("div", class_="panel-footer").find_all('a')[0]['href'],
            'link': f"{Constants.NyaaBaseUrl}/view/{file_id}",
            'id': file_id,
            'magnet': container.find("div", class_="panel-footer").find_all('a')[1]['href'],
            'size': container.find_all("div", class_="row")[3].find_all('div')[1].text.strip(),
            'category': container.find_all("div", class_="row")[0].find_all('div')[1].text.strip(),
            'uploaded': container.find_all("div", class_="row")[0].find_all('div')[3].text.strip(),
            'seeders': int(container.find_all("div", class_="row")[1].find_all('div')[3].text.strip()),
            'leechers': int(container.find_all("div", class_="row")[2].find_all('div')[3].text.strip()),
            'completed': int(container.find_all("div", class_="row")[3].find_all('div')[3].text.strip()),
        }

        comment_count = int(container.find("div", id="comments").find("h3", class_="panel-title").text.split("-")[-1].strip())
        comments = []

        if comment_count > 0:
            comment_panels = container.find("div", id="comments").find_all("div", class_="comment-panel")
            for comment_panel in comment_panels:
                element = comment_panel.find("div", class_="panel-body")
                comment = {
                    'name': element.find("a").text.strip(),
                    'content': element.find("div", class_="comment-body").find("div", class_="comment-content").text.strip(),
                    'image': element.find("img", class_="avatar")['src'] if element.find("img", class_="avatar") else Constants.DefaultProfilePic,
                    'timestamp': element.find("a").contents[0].strip()
                }
                comments.append(comment)

        file_info = {
            'torrent': torrent_data,
            'description': container.find("div", id="torrent-description").text.strip(),
            'submittedBy': container.find_all("div", class_="row")[1].find_all('div')[1].text.strip(),
            'infoHash': container.find_all("div", class_="row")[4].find_all('div')[1].text.strip(),
            'commentInfo': {
                'count': comment_count,
                'comments': comments,
            }
        }

        return file_info
    else:
        return None


def scrape_nyaa(url):
    response = requests.get(url)
    if response.status_code == 200:
        response_body = response.text
        soup = BeautifulSoup(response_body, 'html.parser')
        table = soup.find("tbody")

        torrents = []
        for row in table.find_all("tr"):
            torrent_path = row.find_all('td')[1].find_all('a')[-1]['href']
            file_path = row.find_all('td')[2].find_all('a')[0]['href']
            torrent = {
                'id': int(torrent_path.split('/')[2]),
                'title': row.find_all('td')[1].find_all('a')[-1].text,
                'link': Constants.NyaaBaseUrl + torrent_path,
                'file': Constants.NyaaBaseUrl + file_path,
                'category': row.find_all('td')[0].find('a')['title'],
                'size': row.find_all('td')[3].text,
                'uploaded': row.find_all('td')[4].text,
                'seeders': int(row.find_all('td')[5].text),
                'leechers': int(row.find_all('td')[6].text),
                'completed': int(row.find_all('td')[7].text),
                'magnet': row.find_all('td')[2].find_all('a')[1]['href']
            }
            torrents.append(torrent)

        return torrents
    else:
        return None


def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    base_url = check_nyaa_url()

    # Example usage for fileInfoScraper
    file_info_url = f"{base_url}/view/12345"
    file_info = file_info_scraper(file_info_url)
    if file_info:
        save_to_file(file_info, 'file_info.json')
        print(f"File info saved to file_info.json")
    else:
        print("Failed to scrape file info")

    # Example usage for scrapeNyaa
    category_url = f"{base_url}?q=&c=1_0&p=1&s=id&o=desc&f=0"
    torrents = scrape_nyaa(category_url)
    if torrents:
        save_to_file(torrents, 'torrents.json')
        print(f"Torrents saved to torrents.json")
    else:
        print("Failed to scrape torrents")


if __name__ == "__main__":
    main()
