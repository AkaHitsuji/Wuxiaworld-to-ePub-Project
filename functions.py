# imported libraries
import sys
import requests
import os
import re
import ebooklib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from ebooklib import epub
from booksDB import novels

# global variables
novel_url = 'https://www.wuxiaworld.com/novel/'
chinese_novel_url = 'https://www.wuxiaworld.com/language/chinese'
list_of_links = []
list_of_chapters = []
cover_page_exists = False

def download_links(url_link, novel_name):
    list_of_links = []
    page = requests.get(url_link).text
    soup = BeautifulSoup(page, 'html.parser')
    for a in soup.find_all('a', href=re.compile("novel/"+ novel_name)):
        list_of_links.append(a['href'])
    return list_of_links

def download_cover(url_link, novel_name, window, lbl_coverPage):
    global cover_page_exists
    page = requests.get(url_link).text
    soup = BeautifulSoup(page, 'html.parser')
    soup = soup.find('a', href=re.compile("novel/" + novel_name))
    soup = soup.find_all('img')

    image_url = 'https://www.wuxiaworld.com'+ soup[0]['src']

    try:
        r = requests.get(image_url)
        r.raise_for_status()
        img_data = requests.get(image_url).content
        with open('cover_page.jpg', 'wb') as handler:
            handler.write(img_data)
        lbl_coverPage.configure(text="Cover Page Downloaded.")
        window.update()
        print("Cover page downloaded")
        cover_page_exists = True
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        lbl_coverPage.configure(text="Cover image does not exist.")
        window.update()
        print("Cover page image was not downloaded")
        cover_page_exists = False

def download_chapter(url_link, file_name):
    page = requests.get(url_link).text
    file = open(file_name, "w", encoding="utf8")
    file.write(page)
    file.close()

def get_title(soup):
    chapter_title = soup.find("img", {"src": '/images/title-icon.png'}).find_next_sibling().text
    # <img src="/images/title-icon.png"/>
    return chapter_title

def clean_chapter(file_in, file_out):
    raw = open(file_in, "r", encoding="utf8")
    soup = BeautifulSoup(raw, 'html.parser')
    chapter_title = get_title(soup)
    list_of_chapters.append(chapter_title)

    soup = soup.find("div", {"class": 'fr-view'})
    text = soup.get_text(separator='\n\n')
    text = text.replace("Previous Chapter", "").replace("Next Chapter", "")
    text = text.lstrip().rstrip()

    text = text.replace(chapter_title, "")
    text = text.lstrip().rstrip()
    raw.close()
    file = open(file_out, "w", encoding="utf8")
    file.write(text)
    os.remove(file_in)

def remove_file(file_in):
    os.remove(file_in)

def create_epub(selected_novel, list_of_links, window, lbl_numOfChapters, lbl_coverPage):
    book = epub.EpubBook()

    # set metadata
    book.set_identifier('id123456')
    book.set_title(selected_novel + ' - EPUB generator by AkaHitsuji')
    book.set_language('en')

    if cover_page_exists:
        book.set_cover("cover_page.jpg", open('cover_page.jpg', 'rb').read())
        remove_file("cover_page.jpg")
        lbl_coverPage.configure(text="Cover page set for ePub")
        print("Cover page removed")
    # TODO: create cover page from title and name etc
    else:
        print("No cover page exists")

    list_of_epub_chapters = []
    array_length = len(list_of_links)
    chapter_number = 1
    for i in range(array_length):
        chapter_title = list_of_links[i].split("/")[3]
        download_chapter('https://www.wuxiaworld.com' + list_of_links[i], chapter_title + '.html')
        clean_chapter(chapter_title + '.html', chapter_title + '.xhtml')
        chapter_content = open(chapter_title + '.xhtml', "r", encoding="utf8")
        chapter_content = BeautifulSoup(chapter_content, 'html.parser')
        chapter_content = chapter_content.get_text()
        chapter_content = "<br />".join(chapter_content.split("\n"))
        print("Chapter",chapter_number,"downloaded")
        remove_file(chapter_title + '.xhtml')

        # create chapter
        epub_chapter = epub.EpubHtml(title=list_of_chapters[i], file_name=chapter_title + '.xhtml', lang='hr')
        epub_chapter.content = '<head>\n<title>' + list_of_chapters[i] + '</title>\n</head>\n<body>\n<strong>' + list_of_chapters[i] + '</strong>\n<p>' + chapter_content + '</p>\n</body>\n</html>'

        # update tkinter to display progress
        lbl_numOfChapters.configure(text=str(chapter_number)+"/"+str(array_length)+" chapters downloaded")
        window.update()

        # add chapter
        book.add_item(epub_chapter)
        list_of_epub_chapters.append(epub_chapter)

        # for testing: set limit on test printing
        chapter_number+=1
        if chapter_number==5:
            break

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
    epub.write_epub(selected_novel + '.epub', book)

# button clicked function
def clicked(window, selected_option, lbl_download, lbl_numOfChapters, lbl_confirmation, lbl_coverPage):
    selected_novel = selected_option.get()
    novel_name = novels[selected_novel]
    list_of_links = download_links(novel_url+novel_name, novel_name)

    lbl_download.configure(text=selected_novel+" selected.\nDownload starting now.")
    lbl_numOfChapters.configure(text="0/"+str(len(list_of_links))+" chapters downloaded")
    window.update()

    lbl_coverPage.configure(text="Downloading Cover Page.")
    window.update()

    download_cover(chinese_novel_url, novel_name, window, lbl_coverPage)
    create_epub(selected_novel, list_of_links, window, lbl_numOfChapters, lbl_coverPage)

    lbl_confirmation.configure(text="ePub created")
