import re

COUNT_MAILS = 1000

# Регулярное выражение на валидацию почты
regex = re.compile(r"[\w._%+-]+@[\w.-]+\.[a-zA-z]{2,4}", flags=0)

very_many_emails = [f"example_{i}@gmail.{'1' if i % 2 == 0 else ''}com" for i in range(COUNT_MAILS)]

count = 0
for mail in very_many_emails:
    result = regex.match(mail)
    if result is not None:
        count += 1

print(f"{count}/{len(very_many_emails) // 2}")
