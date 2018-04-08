# urllib2 and BeautifulSoup libraries
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# use Mozilla to open webpage to bypass mod_security that blocks bots and pass into htmltext
req = Request('https://www.wuxiaworld.com/novel/against-the-gods/atg-chapter-1', headers={'User-Agent': 'Mozilla/5.0'})
htmltext = urlopen(req).read()

# parse html into BeautifulSoup and store in variable soup
soup = BeautifulSoup(htmltext, 'html.parser')

# extract story section into ResultSet
soup_story = soup.find_all("p")
print(soup_story)
for line in soup_story:
    print(line.text)

# extract title
# chapter_title = soup_story.find("strong")
# print(chapter_title)

# to see xml
# print(soup.prettify())
# print(soup.get_text())
