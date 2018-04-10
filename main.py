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
novel_url = 'https://www.wuxiaworld.com/novel/'
chinese_novel_url = 'https://www.wuxiaworld.com/language/chinese'
list_of_links = []
list_of_chapters = []

def download_cover(url_link):
    page = requests.get(url_link).text
    soup = BeautifulSoup(page, 'html.parser')
    soup = soup.find('a', href=re.compile("novel/against-the-gods"))
    soup = soup.find_all('img')

    image_url = 'https://www.wuxiaworld.com'+ soup[0]['src']
    img_data = requests.get(image_url).content
    with open('cover_page.jpg', 'wb') as handler:
        handler.write(img_data)


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
    file.write(text)
    os.remove(file_in)

# main code
download_links(novel_url+'against-the-gods')
download_cover(chinese_novel_url)

# create epub
book = epub.EpubBook()

# set metadata
book.set_identifier('id123456')
book.set_title('Against the Gods')
book.set_language('en')
book.set_cover("cover_page.jpg", open('cover_page.jpg', 'rb').read())

book.add_author('Author Authorowski')
book.add_author('Danko Bananko', file_as='Gospodin Danko Bananko', role='ill', uid='coauthor')

list_of_epub_chapters = []
array_length = len(list_of_links)
counter = 0
for i in range(array_length):
    # for testing: only print first two chapters
    counter+=1
    if counter==3:
        break

    chapter_title = list_of_links[i].split("/")[3]
    download_chapter('https://www.wuxiaworld.com' + list_of_links[i], chapter_title + '.html')
    clean_chapter(chapter_title + '.html', chapter_title + '.xhtml')
    chapter_content = open(chapter_title + '.xhtml', "r", encoding="utf8")
    chapter_content = BeautifulSoup(chapter_content, 'html.parser')
    chapter_content = chapter_content.get_text(separator='\n\n')
    chapter_content = "<br />".join(chapter_content.split("\n"))

    # create chapter
    epub_chapter = epub.EpubHtml(title=list_of_chapters[i], file_name=chapter_title + '.xhtml', lang='hr')
    epub_chapter.content = '<head>\n<title>' + list_of_chapters[i] + '</title>\n</head>\n<body>\n<strong>' + list_of_chapters[i] + '</strong>\n<p>' + chapter_content + '</p>\n</body>\n</html>'

    # add chapter
    book.add_item(epub_chapter)
    list_of_epub_chapters.append(epub_chapter)

# define Table Of Contents
for epub_chapter in list_of_epub_chapters:
    book.toc.append(epub_chapter)

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# add CSS file
book.add_item(nav_css)

# basic spine
book.spine = ['nav']
for epub_chapter in list_of_epub_chapters:
    book.spine.append(epub_chapter)

# write to the file
epub.write_epub('ATGtest.epub', book)
