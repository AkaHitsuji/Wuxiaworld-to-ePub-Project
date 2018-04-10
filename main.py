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
    file.write(text)
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
    chapter_content = open(chapter_title + '.xhtml', "r", encoding="utf8")
    chapter_content = BeautifulSoup(chapter_content, 'html.parser')
    chapter_content = chapter_content.get_text(separator='\n\n')
    chapter_content = "<br />".join(chapter_content.split("\n"))

    # create chapter
    epub_chapter = epub.EpubHtml(title=chapter_title, file_name=chapter_title + '.xhtml', lang='hr')
    epub_chapter.content = '<head>\n<title>' + chapter_title + '</title>\n</head>\n<body>\n<strong>' + chapter_title + '</strong>\n<p>' + chapter_content + '</p>\n</body>\n</html>'

    # add chapter
    book.add_item(epub_chapter)
    list_of_epub_chapters.append(epub_chapter)

# define Table Of Contents
for epub_chapter in list_of_epub_chapters:
    book.toc.append(epub_chapter)
# book.toc = (epub.Link('intro.xhtml', 'Introduction', 'intro'),
#             (epub.Section('Languages'),
#             (list_of_epub_chapters))
#             )
print(book.toc)

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

# if __name__ == '__main__':
#     book = epub.EpubBook()
#
#     # add metadata
#     book.set_identifier('sample123456')
#     book.set_title('Sample book')
#     book.set_language('en')
#
#     book.add_author('Aleksandar Erkalovic')
#
#     # intro chapter
#     c1 = epub.EpubHtml(title='Introduction', file_name='intro.xhtml', lang='hr')
#     c1.content=u'<html><head></head><body><h1>Introduction</h1><p>Introduction paragraph where i explain what is happening.</p></body></html>'
#
#     # defube style
#     style = '''BODY { text-align: justify;}'''
#
#     default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css", content=style)
#     book.add_item(default_css)
#
#
#     # about chapter
#     c2 = epub.EpubHtml(title='About this book', file_name='about.xhtml')
#     c2.content='<h1>About this book</h1><p>Helou, this is my book! There are many books, but this one is mine.</p>'
#     c2.set_language('hr')
#     c2.properties.append('rendition:layout-pre-paginated rendition:orientation-landscape rendition:spread-none')
#     c2.add_item(default_css)
#
#     # add chapters to the book
#     book.add_item(c1)
#     book.add_item(c2)
#
#
#
#     # create table of contents
#     # - add manual link
#     # - add section
#     # - add auto created links to chapters
#
#     book.toc = (epub.Link('intro.xhtml', 'Introduction', 'intro'),
#                 (epub.Section('Languages'),
#                  (c1, c2))
#                 )
#
#     # add navigation files
#     book.add_item(epub.EpubNcx())
#     book.add_item(epub.EpubNav())
#
#     # define css style
#     style = '''
# @namespace epub "http://www.idpf.org/2007/ops";
# body {
#     font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
# }
# h2 {
#      text-align: left;
#      text-transform: uppercase;
#      font-weight: 200;
# }
# ol {
#         list-style-type: none;
# }
# ol > li:first-child {
#         margin-top: 0.3em;
# }
# nav[epub|type~='toc'] > ol > li > ol  {
#     list-style-type:square;
# }
# nav[epub|type~='toc'] > ol > li > ol > li {
#         margin-top: 0.3em;
# }
# '''
#
#     # add css file
#     nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
#     book.add_item(nav_css)
#
#     # create spine
#     book.spine = ['nav', c1, c2]
#     print(book.spine)
#
#     # create epub file
#     epub.write_epub('test.epub', book, {})
