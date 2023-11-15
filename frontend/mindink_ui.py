from tkinter import Tk
from tkinter import *
from PIL import Image, ImageTk

#Create object 
root = Tk() 
  
# Adjust size 
root.geometry( "500x700" ) 
  
# Change the label text 
def show(): 
    label.config( text = clicked.get() ) 
    # TODO: function to make call to SD API

  
# Dropdown menu options 
options = [ 
    "Astilbe", "Iris", "Bellflower", "Calendula", "Rose",\
    "California Poppy", "Daisy", "Carnation", "Black-Eyed Susan", "Coreopsis",\
    "Tulip", "Dandelion", "Water Lily", "Sunflower"
] 
  
# datatype of menu text 
clicked = StringVar() 
  
# initial menu text 
clicked.set( "Astilbe" ) 

logo_image = Image.open("/Users/claudia/ai-proj-mindink/MindInk/frontend/mindink-logo.png")  # Replace with the path to your logo image
logo_image = logo_image.resize((90, 90), Image.LANCZOS)  # Resize the logo as needed
logo_photo = ImageTk.PhotoImage(logo_image)

# Create a label to display the logo
logo_label = Label(root, image=logo_photo, bg="white")
logo_label.image = logo_photo  # Keep a reference to the image to prevent garbage collection
logo_label.place(x=10, y=10)  # Adjust the coordinates and padding as needed

minkink_title = Label(root, text='MindInk', font='Helvetica 24 bold')
minkink_title.pack(pady=10)
label = Label(root , text = "Select flower to generate image!") 
label.pack(padx=10, pady=5)
# Create Dropdown menu 
drop = OptionMenu( root , clicked , *options ) 
drop.pack(padx=10, pady=5) 
  
# Create button, it will change label text 
button = Button( root , text = "Generate Image", command = show).pack(padx=10, pady=5) 
  
# Create Label 
label = Label( root , text = " " ) 
label.pack(padx=10, pady=5) 
  
# Execute tkinter 
root.mainloop() 