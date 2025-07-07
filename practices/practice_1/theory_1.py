import re

# Проверьте, начинается ли строка с «The» и заканчивается ли она на «Spain»:

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)

if x:
    print("Есть совпадение")
else:
    print("Нет совпадения")

