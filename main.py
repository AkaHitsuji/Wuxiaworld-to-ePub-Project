# imported libraries
import functions
from booksDB import novels

# global variables
novel_url = 'https://www.wuxiaworld.com/novel/'
chinese_novel_url = 'https://www.wuxiaworld.com/language/chinese'
list_of_links = []

# main code
while True:
    selected_novel = input("Name of novel: ")
    if selected_novel in novels:
        break
    else:
        print("Novel does not exist, please input again.")

novel_name = novels[selected_novel]

list_of_links = functions.download_links(novel_url+novel_name, novel_name)
print("Number of Chapters: ", len(list_of_links))

functions.download_cover(chinese_novel_url, novel_name)
print("Cover page downloaded.")

functions.create_epub(selected_novel, list_of_links)
print("ePub created")
