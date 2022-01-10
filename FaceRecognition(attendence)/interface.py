import tkinter
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog as fd
import cv2 as cv
import re


window = Tk()

bg = '#3B6597'
btn_bg = '#0F307D'
fg = '#ECF0F1'

window.title('Face Recognition Attendence System')
window.configure(bg=bg)
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
app_width = 950
app_height = 650

x = int((screen_width / 2) - (app_width / 2))
y = int((screen_height / 2) - (app_height / 2))
window.geometry(f"{app_width}x{app_height}+{x}+{y}")

lb1 = tkinter.Label(text="Face Recognition Attendence System", bg=btn_bg, fg = fg,relief="solid",
                    height=2, font="Bahnschrift 20 bold", anchor=CENTER)
lb1.pack(side=TOP, fill=BOTH)

lb2 = tkinter.Label(text="Live Camera", bg=bg, fg = fg,font="Bahnschrift 24 bold ")
lb2.place(relx=0.1, rely=0.2 )


image_path = './images/rough.png'
    # Getting image
my_pic = Image.open(image_path)
    # Resizing Image
resized = my_pic.resize((520, 350), Image.ANTIALIAS)
    # Displaying image
new_pic = ImageTk.PhotoImage(resized)
img_label = tkinter.Label(image=new_pic, bg='black')
img_label.image = new_pic
img_label.place(relx=0.3, rely=0.6, anchor=CENTER)

upload_button = tkinter.Button(text='Access Camera', bg=btn_bg,fg = fg,
                               font=("Times%New%Roman", 15, "bold"),
                               relief="solid")
upload_button.place(relx=0.2, rely=0.9)

window.mainloop()
