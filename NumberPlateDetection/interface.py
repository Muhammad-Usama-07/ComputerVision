import tkinter
from tkinter import *
from PIL import ImageTk, Image
from tkinter.ttk import *
import time
from tkinter import colorchooser, filedialog, messagebox
from tkinter import filedialog as fd
import PIL.ImageGrab as ImageGrab

window = Tk()

window.title('Number Plate Detection')
window.configure(bg='#7DBCE3')
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
app_width = 950
app_height = 650

x = int((screen_width / 2) - (app_width / 2))
y = int((screen_height / 2) - (app_height / 2))
window.geometry(f"{app_width}x{app_height}+{x}+{y}")

lb1 = tkinter.Label(text="Number Plate Detection App", bg="#2A9BE1", relief="solid",
                    height=1, font="Times%New%Roman 18 bold", anchor=CENTER)
lb1.pack(side=TOP, fill=BOTH)



window.mainloop()
