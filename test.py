# imported libraries
import sys
import requests
import os
import re
import ebooklib
from bs4 import BeautifulSoup


# print(url_link)
page = requests.get("https://www.wuxiaworld.com/novel/lord-of-all-realms/chapter-22-an-impasse").text
file = open("test.html", "w", encoding="utf8")
file.write(page)
file.close()

raw = open("test.html", "r", encoding="utf8")
soup = BeautifulSoup(raw, 'html.parser')
# chapter_title = get_title(soup)
# list_of_chapters.append(chapter_title)

soup = soup.find_all("div", {"class": 'fr-view'})
print('This is the output before\n\n\n',soup)
soup = soup[0]
print('this is the output after\n\n\n',soup)
text = soup.get_text(separator='\n\n')
text = text.replace("Previous Chapter", "").replace("Next Chapter", "")
text = text.lstrip().rstrip()

# text = text.replace(chapter_title, "")
text = text.lstrip().rstrip()

print(text)
