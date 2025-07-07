from bs4 import BeautifulSoup


def parse_index_to_urls(index_html: str) -> list[str]:
    bs = BeautifulSoup(index_html, "html.parser")
    items_tags = bs.find_all("li")
    return [i.text for i in items_tags]


def parse_page(page_html: str) -> (list[str], list[list[str]]):
    rows = []
    bs = BeautifulSoup(page_html, "html.parser")
    table_tag = bs.find("table", {"id": "credit_customers"})
    headers_tag = table_tag.find("thead")
    headers_items_tags = headers_tag.find_all("th")
    headers = [i.text for i in headers_items_tags]
    table_body_tag = table_tag.find("tbody")
    rows_tags = table_body_tag.find_all("tr")
    for row_tag in rows_tags:
        rows_items_tags = row_tag.find_all("td")
        rows_items = [i.text for i in rows_items_tags]
        rows.append(rows_items)
    return headers, rows
