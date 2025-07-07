from bs4 import BeautifulSoup
# Открываем наш HTML-файл и передаём содержимое в переменную htmlcontent
with open('assets/sample_1.html', 'r', encoding="utf-8") as file:
    html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    # Ищем тег ul с атрибутом id=thebestlist. Обратите внимание,
    # если элементов будет несколько, будет выведен только первый.
    # Так как у нас список только один, он будет "напечатан" весь, вместе с дочерними элементами
    print(soup.find('ul', attrs={'id': 'thebestlist'}))
    # А тут в цикле перебираем все найденные теги li (то есть элементы списка)
    for tag in soup.find_all('li'):
        print(tag.text)