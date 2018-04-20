# imported libraries
import functions
from booksDB import novels
from tkinter import *
from tkinter import ttk

# get list of novels
functions.create_DB()
list_of_novels = []
for title in novels:
    list_of_novels.append(title)

# tkinter code
window = Tk()

window.title("Wuxiaworld to ePub")
window.geometry('500x300')

lbl = Label(window, text="Wuxiaworld to ePub - a project created by AkaHitsuji.\nTo begin, select a novel in the drop down list below,\nthen click download to download the novel in its ePub format! :)\nI created this so that I could read the novels offline.")
lbl.grid(column=0, row=0)

option = StringVar()
selected_option = ttk.Combobox(window, width = 42, textvariable = option, state = "readonly")
selected_option["values"] = list_of_novels
selected_option.grid(column = 0, row = 1)
selected_option.current(0)

lbl_download = Label(window, text="")
lbl_download.grid(column=0, row=4)

lbl_coverPage = Label(window, text="")
lbl_coverPage.grid(column=0, row=5)

lbl_numOfChapters = Label(window, text="")
lbl_numOfChapters.grid(column=0, row=6)

lbl_confirmation = Label(window, text="")
lbl_confirmation.grid(column=0, row=7)

btn = Button(window, text="Download", command= lambda: functions.clicked(window, selected_option, lbl_download, lbl_numOfChapters, lbl_confirmation, lbl_coverPage))
btn.grid(column=0, row=2)

window.mainloop()
