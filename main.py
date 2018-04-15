# imported libraries
import functions
from booksDB import novels
from tkinter import *
from tkinter import ttk

# global variables
novel_url = 'https://www.wuxiaworld.com/novel/'
chinese_novel_url = 'https://www.wuxiaworld.com/language/chinese'
list_of_links = []
list_of_novels = []

# get list of novels
for title in novels:
    list_of_novels.append(title)

# tkinter code
window = Tk()

window.title("Wuxiaworld to ePub")
window.geometry('500x300')

lbl = Label(window, text="Welcome to Wuxiaworld to ePub, a project created by AkaHitsuji.\nTo begin, select a novel in the drop down list below,\nthen click download to download the novel in its ePub format!\nIt's as simple as that :)")
lbl.grid(column=0, row=0)

option = StringVar()
selected_option = ttk.Combobox(window, width = 42, textvariable = option, state = "readonly")
selected_option["values"] = list_of_novels
selected_option.grid(column = 0, row = 1)
selected_option.current(0)

def clicked():
    lbl.configure(text="Button was clicked !!")

btn = Button(window, text="Click Me", command=clicked)
btn.grid(column=0, row=2)

window.mainloop()

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

functions.create_epub(selected_novel, list_of_links)
print("ePub created")
