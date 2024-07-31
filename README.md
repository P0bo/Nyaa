# Nyaa API Scraper

This project is a Python-based web scraper for the Nyaa torrent site. It fetches torrent information based on specific IDs and saves the data to local JSON files.

## Features

- Scrape specific torrent data by ID
- Save scraped data to JSON files

## Requirements

- Python 3.6+
- `requests` library
- `beautifulsoup4` library

## Installation

Install the required libraries using pip:
```sh
pip install requests beautifulsoup4
```

## Usage

The script can be used to scrape detailed information about a specific torrent using its ID and save it to a JSON file.

### Scrape Torrent Data by ID

Fetch detailed information about a specific torrent using its ID and save it to a JSON file named `<id>.json`.

**Example Command**:
```sh
python nyaa_scraper.py <id>
```

### Example

Here's a complete example of using the script to fetch and save torrent data by ID:

```sh
python nyaa_scraper.py 12345
```

This command will fetch the torrent data with ID 12345 and save the details in `12345.json`.

## Constants and Configuration

The script uses a `Constants` class to define base URLs and default profile picture URLs. These can be customized in the script as needed.

```python
class Constants:
    NyaaBaseUrl = "https://nyaa.si"
    NyaaAltUrl = "https://nyaa.smartass08.xyz"
    DefaultProfilePic = "https://raw.githubusercontent.com/Yash-Garg/Nyaa-Api-Go/dev/static/default.png"
```
