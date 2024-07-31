# Nyaa API Scraper

This project is a Python-based web scraper for the Nyaa torrent site. It fetches torrent information based on various categories, user uploads, and specific IDs, and saves the data to local JSON files.

## Features

- Scrape torrent data by category
- Scrape user upload data
- Scrape specific torrent data by ID
- Save scraped data to JSON files

## Requirements

- Python 3.6+
- `requests` library
- `beautifulsoup4` library

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/nyaa-api-scraper.git
    cd nyaa-api-scraper
    ```

2. **Install the required Python libraries**:
    ```sh
    pip install -r requirements.txt
    ```

    If you don't have `requirements.txt`, you can manually install the libraries:
    ```sh
    pip install requests beautifulsoup4
    ```

## Usage

The script can be used to scrape different types of data from Nyaa. Below are the available commands and how to use them.

### 1. Scrape Torrent Data by ID

Fetch detailed information about a specific torrent using its ID and save it to a JSON file.

**Example Command**:
```sh
python nyaa_scraper.py --type id --id 12345 --output file_info.json
```

### 2. Scrape User Uploads

Fetch all torrents uploaded by a specific user and save them to a JSON file.

**Example Command**:
```sh
python nyaa_scraper.py --type user --username someuser --output user_uploads.json
```

### 3. Scrape Torrent Data by Category

Fetch torrents from a specific category and save them to a JSON file.

**Example Command**:
```sh
python nyaa_scraper.py --type category --category anime --subcategory eng --output anime_eng.json
```

### Arguments

- `--type`: Specifies the type of data to scrape (`id`, `user`, or `category`).
- `--id`: The ID of the torrent (required if `--type` is `id`).
- `--username`: The username of the uploader (required if `--type` is `user`).
- `--category`: The category of torrents to scrape (required if `--type` is `category`).
- `--subcategory`: The subcategory of torrents to scrape (optional).
- `--output`: The name of the output JSON file (default is `output.json`).

## Example

Here's a complete example of using the script to fetch and save torrent data by ID:

```sh
python nyaa_scraper.py --type id --id 12345 --output file_info.json
```

This command will fetch the torrent data with ID 12345 and save the details in `file_info.json`.

## Constants and Configuration

The script uses a `Constants` class to define base URLs and endpoint mappings. These can be customized in the script as needed.

```python
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
```
