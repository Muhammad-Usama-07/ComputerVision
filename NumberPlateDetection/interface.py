import tkinter
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog as fd
import cv2 as cv
import pytesseract
import re
import easyocr
patterns= [r'\w+']


num_plat_classif = cv.CascadeClassifier('../cascadeFiles/russian_number_plate.xml')
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\trainee4\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
counter = 0
# reader = easyocr.Reader(['en'])


def count():
    global counter
    counter +=1
    return counter

window = Tk()

def upload():


    filename = fd.askopenfilename()
    # print(count())
    lb5.config(text = "Car Passed : "+str(count()))


    img = cv.imread(filename)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    number = num_plat_classif.detectMultiScale(img, 1.2)
    for (x, y, w, h) in number:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        new_img_path = cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
        imgg = Image.fromarray(new_img_path)
        resized_img = imgg.resize((520, 350), Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(resized_img)
        img_label.configure(image=new_img)
        img_label.image = new_img
        # output = reader.readtext(roi_color)
        # print(output)
        # lb4.config(text = "Plate No. : " + str(output[-1][-2]))




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

lb2 = tkinter.Label(text="Upload and Recognitze Image", bg="#7DBCE3", font="Bahnschrift 24 bold ")
lb2.place(relx=0.1, rely=0.2 )
lb3 = tkinter.Label(text="Details", bg="#7DBCE3", font="Bahnschrift 26 bold ")
lb3.place(relx=0.7, rely=0.2)# relx=0.7, rely=0.2
lb4 = tkinter.Label(text="Plate No. : XXXXXX", bg="#7DBCE3", font="Bahnschrift 20 bold ")
lb4.place(relx=0.6, rely=0.4 )
lb5 = tkinter.Label(text="Car Passed : 0", bg="#7DBCE3", font="Bahnschrift 20 bold ")
lb5.place(relx=0.6, rely=0.5 )

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

lb2 = tkinter.Label(text="Detected Number Plate", bg="#7DBCE3", font="Bahnschrift 24 bold ")
lb2.place(relx=0.6, rely=0.6 )

image_path = './images/rough2.png'
    # Getting image
rough_pic2 = Image.open(image_path)
    # Resizing Image
resized2 = rough_pic2.resize((280, 80), Image.ANTIALIAS)
    # Displaying image
rough_pic2 = ImageTk.PhotoImage(resized2)
img_label2 = tkinter.Label(image=rough_pic2, bg='black')
img_label2.image = new_pic
img_label2.place(relx=0.8, rely=0.8, anchor=CENTER)

upload_button = tkinter.Button(text='click to upload', bg='#2A9BE1',
                               font=("Times%New%Roman", 15, "bold"),
                               relief="solid", command=upload)
upload_button.place(relx=0.4, rely=0.9)

window.mainloop()
