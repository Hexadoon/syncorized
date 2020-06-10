# pyintaller --onefile --icon="filename without quotes" -w first.py 
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
import os
os.system('clear')

root = Tk()
root.title("Syncorized")
#root.geometry("1024x480")

image1 = Image.open("../images/moroccan-flower.png")
background_image = ImageTk.PhotoImage(image1)
w = background_image.width()
h = background_image.height()
root.geometry("%dx%d+50+30" % (w, h))

background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def hello():
    hello_label = Label(root, text = "Hello " + myTextbox.get())
    hello_label.pack()

myLabel = Label(root, text = "Enter your name: ")
myLabel.pack(padx = 50, pady = 50)

myTextbox = Entry(root, width = 30)
myTextbox.pack()

#myButton = Button(root, text = "Submit your file", command = hello, state=DISABLED)

def open():
    #myLabel = Label(root, text = "hi").pack()
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes =[('All Files', '*.*')])
    if root.filename != '':
        my_label2 = Label(root, text = root.filename).pack()

File_button = Button(root, text = "Open Audio File", command = open, padx = 50, pady=10, fg = "green",activeforeground="white",activebackground="yellow", highlightbackground = "red").pack()

#myLabel.grid(row=0,column=0)
#myTextbox.grid(row=1,column=1)
#myButton.grid(row=2,column=0)
myButton = Button(root, text = "Render", command = hello, padx = 50, pady=10, fg = "blue", highlightbackground='gray', activebackground="purple", activeforeground="white")
myButton.pack()

button_quit = Button(root, text = "Exit Program", command= root.quit).pack()

root.mainloop()

# b = Button(win, text='Times Up!',bg="yellow", fg="green", activebackground="purple", activeforeground="white", command=quit)
# b.pack(ipadx=root.winfo_screenwidth()/2,ipady=root.winfo_screenheight()/2)
