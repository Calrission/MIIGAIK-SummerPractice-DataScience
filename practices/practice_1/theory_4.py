import requests
from bs4 import BeautifulSoup

response = requests.get("https://news.ycombinator.com/")
if response.status_code == 200:
    html_content = response.content
    print(html_content)
    soup = BeautifulSoup(html_content, "html.parser")
    for child in soup.descendants:
        if child.name:
            print(child.name)
else:
    print(response)
