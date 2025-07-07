from bs4 import BeautifulSoup

with open('assets/theory_1.html', 'r') as file:
    content = file.read()
    soup = BeautifulSoup(content, "html.parser")

for child in soup.descendants:
    if child.name:
        print(child.name)