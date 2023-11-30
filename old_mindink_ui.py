from tkinter import Tk
from tkinter import *
from PIL import Image, ImageTk
from main import *
from backend.classifier.predict import *

#Create object 
root = Tk() 
  
# Adjust size 
root.geometry( "500x900" ) 
  
# Change the label text 
def show(): 
    label.config( text = clicked.get() ) 
    print(clicked.get())

    # TODO: function to make call to SD API
    user_sel = clicked.get()
    # TODO: call get_image with user_sel


def sel():
    selection = ""
    if var.get() == 0:
        selection = "YES"
    else: 
        selection = "NO"
    sd_res_label.config(text = selection)


# Dropdown menu options 
options = [ 
    "Astilbe", "Iris", "Bellflower", "Calendula", "Rose",\
    "California Poppy", "Daisy", "Carnation", "Black-Eyed Susan", "Coreopsis",\
    "Tulip", "Dandelion", "Water Lily", "Sunflower"
] 
  
# datatype of menu text 
clicked = StringVar() 
  
# initial menu text 
clicked.set(options[0]) 

# display logo
logo_image = Image.open("/Users/claudia/intro-to-ai/ai-proj-mindink/MindInk/frontend/mindink-logo.png")  # Replace with the path to your logo image
logo_image = logo_image.resize((90, 90), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)

# create label to display  logo
logo_label = Label(root, image=logo_photo, bg="white")
logo_label.image = logo_photo
logo_label.place(x=10, y=10) # adjust placement

# generate & place title and first user instruction
minkink_title = Label(root, text='MindInk', font='Helvetica 24 bold')
minkink_title.pack(pady=10)
label = Label(root , text = "Select flower to generate image!") 
label.pack(padx=10, pady=5)

# create dropdown menu 
drop = OptionMenu(root, clicked, *options) 
drop.pack(padx=10, pady=5) 
  
# create button that will change label text 
# button = Button(root , text="Generate Image", command=show).pack(padx=10, pady=5) 
button = Button(root , text="Generate Image", command=lambda: get_image(clicked.get())).pack(padx=10, pady=5) 

# create label to display choice 
label = Label(root, text = " ") 
label.pack(padx=10, pady=5) 

# label signifying that image will be displayed below
sd_label = Label(root , text = "STANDARD DIFFUSION IMAGE", font="Helvetica 16 bold") 
sd_label.pack(padx=10, pady=10)

# TODO: while image not yet generated...


# set aside a 180x180 box to 
wid = 180
hgt = 180
canvas = Canvas(root, width=wid, height=hgt)
canvas.pack()

# get the image & resize it
flower_img = Image.open("rose-test.png")
resized_img = flower_img.resize((180,180), Image.LANCZOS)
new_img = ImageTk.PhotoImage(resized_img)
flower = canvas.create_image(wid/2, hgt/2, image=new_img, tags="target")  

# option for user to indicate whether output is correct
sd_gen_label = Label(root , text = "Is this correct?", font="Helvetica 12 bold") 
sd_gen_label.pack(padx=10, pady=5)

var = IntVar()
R1 = Radiobutton(root, text="Yes", variable=var, value=0, command=sel)
R1.pack(padx=10, pady=0)

R2 = Radiobutton(root, text="No", variable=var, value=1, command=sel)
R2.pack(padx=10, pady=0)

sd_res_label = Label(root, text="User Verification Needed")
sd_res_label.pack(padx=10, pady=5)

class_intro_label = Label(root, text="ResNet50 Image Classifier...", font="Helvetica 16 bold")
class_intro_label.pack(pady=15)
# TODO: get label/classification from image classifier
# must WAIT

class_res_label = Label(root, text="ResNet50 Output HERE")
class_res_label.pack(pady=10)

# TODO: format and predict using resnet50 classifier!!
## TODO: how to wait for API output???
# execute tkinter 
root.mainloop() 