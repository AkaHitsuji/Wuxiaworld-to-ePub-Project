# imported libraries
import sys
import requests
import os
import re
import ebooklib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from ebooklib import epub

# global variables
test_url = 'https://www.wuxiaworld.com/novel/against-the-gods'
list_of_links = []
list_of_chapters = []

def download_links(url_link):
    page = requests.get(url_link).text
    soup = BeautifulSoup(page, 'html.parser')
    for a in soup.find_all('a', href=re.compile("novel/against-the-gods")):
        list_of_links.append(a['href'])
    print("Number of Chapters: ", len(list_of_links))

def download_chapter(url_link, file_name):
    page = requests.get(url_link).text
    file = open(file_name, "w", encoding="utf8")
    file.write(page)
    file.close()

def clean_chapter(file_in, file_out):
    raw = open(file_in, "r", encoding="utf8")
    soup = BeautifulSoup(raw, 'html.parser')
    soup = soup.find("div", {"class": 'fr-view'})
    text = soup.get_text(separator='\n\n')
    text = text.replace("Previous Chapter", "").replace("Next Chapter", "")
    text = text.lstrip().rstrip()
    # find chapter title, store and remove it
    chapter_title = text.split('\n', 1)[0]
    list_of_chapters.append(chapter_title)

    text = text.replace(chapter_title, "")
    text = text.lstrip().rstrip()
    raw.close()
    file = open(file_out, "w", encoding="utf8")
    file.write('<html xmlns="http://www.w3.org/1999/xhtml">')
    file.write("\n<head>")
    file.write("\n<title>" + chapter_title + "</title>")
    file.write("\n</head>")
    file.write("\n<body>")
    file.write("\n<strong>" + chapter_title + "</strong>" + "\n<p>")
    file.write(text)
    file.write("</p>")
    file.write("\n</body>")
    file.write("\n</html>")
    os.remove(file_in)

# main code
download_links(test_url)

# counter = 0
# for chapter in list_of_links:
#     # for testing: only print first two chapters
#     counter+=1
#     if counter==3:
#         break
#
#     chapter_title = chapter.split("/")[3]
#     download_chapter('https://www.wuxiaworld.com' + chapter, chapter_title + '.html')
#     clean_chapter(chapter_title + '.html', chapter_title + '.xhtml')

# create epub
book = epub.EpubBook()

# set metadata
book.set_identifier('id123456')
book.set_title('Sample book')
book.set_language('en')

book.add_author('Author Authorowski')
book.add_author('Danko Bananko', file_as='Gospodin Danko Bananko', role='ill', uid='coauthor')

list_of_epub_chapters = []
counter = 0
for chapter in list_of_links:
    # for testing: only print first two chapters
    counter+=1
    if counter==3:
        break

    chapter_title = chapter.split("/")[3]
    download_chapter('https://www.wuxiaworld.com' + chapter, chapter_title + '.html')
    clean_chapter(chapter_title + '.html', chapter_title + '.xhtml')

    # create chapter
    epub_chapter = epub.EpubHtml(title=chapter_title, file_name=chapter_title + '.xhtml', lang='hr')
    epub_chapter.content = chapter_title + '.xhtml'
    # add chapter
    book.add_item(epub_chapter)
    list_of_epub_chapters.append(epub_chapter)
    print(list_of_epub_chapters)

# define Table Of Contents
book.toc = (list_of_epub_chapters)

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# add CSS file
book.add_item(nav_css)

# basic spine
# book.spine = ['nav', c1]

# write to the file
epub.write_epub('ATGtest.epub', book)
