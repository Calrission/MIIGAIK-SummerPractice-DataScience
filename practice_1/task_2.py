from pprint import pprint

import requests
from bs4 import BeautifulSoup

response = requests.get("https://moskva.kitabi.ru/transport/sluzhby-taksi")
data = []
if response.status_code != 200:
    print("Something went wrong")
    print(response.text)
else:
    try:
        html_content = response.content
        soup = BeautifulSoup(response.text, "html.parser")
        companies_list = soup.find("div", {"class": "companies-list"})
        companies = companies_list.find_all("div", {"class": "block-white company-list-item"})
        for company in companies:
            try:
                img = "https://moskva.kitabi.ru/" + company.find("img").get("src")
                title = company.find("div", attrs={"class": "company-list-item-title"}).text
                contacts = company.find("div", attrs={"class": "company-info-contacts"})
                contacts_values = contacts.find_all("div", attrs={"class": "company-info-contacts-row-value"})
                data.append((img, title))
            except Exception as e:
                print("Something went wrong")
                print(e)
        print(data)
    except Exception as e:
        print(html_content)

