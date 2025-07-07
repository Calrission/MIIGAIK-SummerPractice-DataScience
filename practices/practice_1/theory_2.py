import re

pattern = 'Привет'
string = 'Привет, как твои дела? Привет, нормально, учу регулярные выражения.'
result = re.findall(pattern, string)

# В данном примере будет выведено ['Привет', 'Привет']
print(result)

pattern = 'Привет'
string = 'Привет, как твои дела? Привет, нормально, учу регулярные выражения.'
result = re.search(pattern, string)

# В данном примере будет выведено <re.Match object; span=(0, 6), match='Привет'>
print(result)

pattern = 'Привет'
string = 'Как твои дела? Привет, нормально, учу регулярные выражения.'
result = re.search(pattern, string)

# В данном примере будет выведено <re.Match object; span=(15, 21), match='Привет'>
print(result)

pattern = 'Привет'
string = 'Привет, как твои дела? Привет, нормально, учу регулярные выражения.'
result = re.split(pattern, string)

# В данном примере будет выведено ['', ', как твои дела? ', ', нормально, учу регулярные выражения.']
print(result)

pattern = 'Привет'
replace = 'Пока'
string = 'Привет, как твои дела? Привет, нормально, учу регулярные выражения.'
result = re.sub(pattern, replace, string)

# В данном примере будет выведено Пока, как твои дела? Пока, нормально, учу регулярные выражения.
print(result)

pattern = 'Привет'
replace = 'Пока'
string = 'Привет, как твои дела? Привет, нормально, учу регулярные выражения.'
result = re.subn(pattern, replace, string)

# Выведет ('Пока, как твои дела? Пока, нормально, учу регулярные выражения.', 2)
print(result)
