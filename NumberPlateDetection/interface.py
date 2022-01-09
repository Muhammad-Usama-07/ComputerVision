import tkinter
from tkinter import *
from PIL import ImageTk, Image


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

lb1 = tkinter.Label(text="Number Plate Detection Application", bg="#2A9BE1", relief="solid",
                    height=2, font="Bahnschrift 20 bold", anchor=CENTER)
lb1.pack(side=TOP, fill=BOTH)

lb2 = tkinter.Label(text="Upload Image", bg="#7DBCE3", font="Bahnschrift 22 bold ")
lb2.place(relx=0.2, rely=0.2 )

image_path = './images/rough.png'
    # Getting image
my_pic = Image.open(image_path)
    # Resizing Image
global resized
resized = my_pic.resize((520, 350), Image.ANTIALIAS)
    # Displaying image
new_pic = ImageTk.PhotoImage(resized)
img_label = tkinter.Label(image=new_pic, bg='black')
img_label.image = new_pic
img_label.place(relx=0.3, rely=0.6, anchor=CENTER)

upload_button = tkinter.Button(text='click to upload', bg='#2A9BE1',
                               font=("Times%New%Roman", 15, "bold"),
                               relief="solid")
upload_button.place(relx=0.2, rely=0.9)

window.mainloop()
