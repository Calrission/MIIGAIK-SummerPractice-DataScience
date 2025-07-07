import uuid
from requests import RequestException
import html_datasource
from homeworks.homework_1 import cache, utils, parser, saver
from homeworks.homework_1.constants import INDEX
from homeworks.homework_1.csv_builder import DataFrameCsvBuilder

if cache.check_is_saved(INDEX):
    index_content = cache.read(INDEX)
    print(f"✅ Received index from cache")
else:
    try:
        index_content = html_datasource.get_index_html()
        cache.save(INDEX, index_content)
        print(f"✅ Received index from web")
    except RequestException as e:
        print("💀 Fail fetch index.html")
        print(e)
        quit()

builder = DataFrameCsvBuilder()

urls = parser.parse_index_to_urls(index_content)
length = len(urls)
for i, url in enumerate(urls):
    try:
        name = utils.url2name(url)
        if cache.check_is_saved(name):
            page = cache.read(name)
            print(f"⚒️ {i + 1}/{length} - (cache) {url}")
        else:
            page = html_datasource.get_html(url)
            cache.save(name, page)
            print(f"⚒️ {i + 1}/{length} - {url}")
        header, rows = parser.parse_page(page)
        if not builder.is_exist_header:
            builder.add_header(header)
        builder.add_rows(rows)
    except RequestException as e:
        print(f"⚠️ Request fail fetch page {url=}")
        print(e)
    except Exception as e:
        print(f"⚠️ Unknown fail fetch page {url=}")
        print(e)

df = builder.build()
path = saver.save(f"{uuid.uuid4().hex}.csv", df)
print(f"✅ Success - {path}")
