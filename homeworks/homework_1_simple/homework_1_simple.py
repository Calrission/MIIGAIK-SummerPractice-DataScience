from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
}


def parse_index_to_urls(content_index_html: str) -> list[str]:
    bs = BeautifulSoup(content_index_html, "html.parser")
    items_tags = bs.find_all("li")
    return [tag.text for tag in items_tags]


def parse_page(page_html: str) -> (list[str], list[list[str]]):
    rows = []
    bs = BeautifulSoup(page_html, "html.parser")
    table_tag = bs.find("table", {"id": "credit_customers"})
    headers_tag = table_tag.find("thead")
    headers_items_tags = headers_tag.find_all("th")
    headers_table = [item.text for item in headers_items_tags]
    table_body_tag = table_tag.find("tbody")
    rows_tags = table_body_tag.find_all("tr")
    for row_tag in rows_tags:
        rows_items_tags = row_tag.find_all("td")
        rows_items = [tag_row_item.text for tag_row_item in rows_items_tags]
        rows.append(rows_items)
    return headers_table, rows


def get_index_html() -> str:
    response = requests.get("https://ratcatcher.ru/media/summer_prac/parcing/21/index.html", headers=HEADERS)
    response.raise_for_status()
    return response.text


def get_html(site: str) -> str:
    response = requests.get(site, headers=HEADERS)
    response.raise_for_status()
    return response.text


def save(columns: list[str], data: list[list[str]]) -> str:
    df = pd.DataFrame(data, columns=columns)
    csv_content = df.to_csv(index=False, lineterminator='\n').strip()
    name = datetime.now().strftime('%H%M%S') + ".csv"
    with open(name, 'w') as f:
        f.write(csv_content)
    return name


index_html = get_index_html()
urls = parse_index_to_urls(index_html)
headers = None
all_content = []
for i in range(len(urls)):
    url = urls[i]
    print(f"{i+1}/{len(urls)} - {url}")
    html = get_html(url)
    headers, content = parse_page(html)
    all_content.extend(content)
filename = save(headers, all_content)
print(filename)
