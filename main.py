# urllib2 and BeautifulSoup libraries
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import os
import re

test_url = 'https://www.wuxiaworld.com/novel/against-the-gods'

# use Mozilla to open webpage to bypass mod_security that blocks bots and pass into htmltext
url = 'https://www.wuxiaworld.com/novel/against-the-gods/atg-chapter-1'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
htmltext = urlopen(req).read()

# parse html into BeautifulSoup and store in variable soup
soup = BeautifulSoup(htmltext, 'html.parser')

# extract story section into ResultSet
# soup_story = soup.find_all("p")
# print(soup_story)
# for line in soup_story:
#     print(line.text)

def download_links(url_link):
    page = requests.get(url_link).text
    soup = BeautifulSoup(page, 'html.parser')
    # soup = soup.find_all('a', href='novel')
    list_of_links = []
    counter = 0
    for a in soup.find_all('a', href=re.compile("novel/against-the-gods")):
        list_of_links.append(a['href'])
        counter+=1
    print("Number of Chapters: ", counter)
    print("Number of chapters in list_of_links: ", len(list_of_links))


def download_chapter(url_link, file_name):
    page = requests.get(url_link).text
    file = open(file_name, "w", encoding="utf8")
    file.write(page)
    file.close()

def clean_chapter(file_in, file_out):
    raw = open(file_in, "r", encoding="utf8")
    soup = BeautifulSoup(raw, 'html.parser')
    soup = soup.find("div", {"class": 'fr-view'})
    text = soup.get_text(separator='\n')
    text = text.replace("Previous Chapter", "").replace("Next Chapter", "")
    text = text.lstrip().rstrip()
    # find chapter title, store and remove it
    chapter_title = text.split('\n', 1)[0]
    text = text.replace(chapter_title, "")
    text = text.lstrip().rstrip()
    raw.close()
    file = open(file_out, "w", encoding="utf8")
    file.write(text)
    file.close()
    os.remove(file_in)

download_links(test_url)
download_chapter(url, 'test.html')
clean_chapter('test.html','clean.xhtml')




# create epub
# epub = zipfile.ZipFile(novelname + "_" + chapter_s + "-" + chapter_e + ".epub", "w")
# epub.writestr("mimetype", "application/epub+zip")
# # creating the container.xml file
# epub.writestr("META-INF/container.xml", '''<container version="1.0"
# xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
#   <rootfiles>
#     <rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>
#   </rootfiles>
# </container>''')
