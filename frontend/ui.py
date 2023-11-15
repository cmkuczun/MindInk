import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


def on_button_click():
    user_input = entry.get()
    messagebox.showinfo("Message", f"Hello, {user_input}!")

def on_radio_button_click():
    selected_option = selected_option_var.get()
    label.config(text=f"Selected Option: {selected_option}")


# def create_gradient(canvas, x1, y1, x2, y2, color1, color2):
#     canvas.create_rectangle(x1, y1, x2, y2, fill=color1, outline="")
#     canvas.create_rectangle(x1, y1, x2, y2, fill=color2, outline="", stipple="gray50")

def draw_logo(canvas):
    # Load the MindInk logo
    logo_image = Image.open("/Users/claudia/ai-proj-mindink/MindInk/frontend/mindink-logo.png")  # Replace with the path to your logo image
    logo_image = logo_image.resize((100, 100), Image.LANCZOS)  # Resize the logo as needed
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Create a label to display the logo
    logo_label = tk.Label(canvas, image=logo_photo, bg="white")
    logo_label.image = logo_photo  # Keep a reference to the image to prevent garbage collection
    logo_label.place(x=40, y=40)  # Adjust the coordinates and padding as needed


def on_selection_change(event):
    selected_flower = flower_var.get()
    result_label.config(text=f"Selected Flower: {selected_flower}")


# Create the main window
window = tk.Tk()
window.title("MindInk")

# Set the window to fullscreen
window.attributes('-fullscreen', True)

# Create a canvas widget for the gradient background
canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight(), highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# # Set gradient colors
color1 = "#228B22"  # Forest Green
# color2 = "#2E8B57"  # Sea Green

# # Create a polygon with gradient color
# gradient_polygon = [(0, 0), (window.winfo_screenwidth(), 0), (window.winfo_screenwidth(), window.winfo_screenheight()), (0, window.winfo_screenheight())]
# canvas.create_polygon(gradient_polygon, fill=color1, outline="")
# canvas.create_polygon(gradient_polygon, fill=color2, outline="", stipple="gray50")

# Create a variable to store the selected option
selected_option_var = tk.StringVar()

# Create 14 radio buttons
options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5",
           "Option 6", "Option 7", "Option 8", "Option 9", "Option 10",
           "Option 11", "Option 12", "Option 13", "Option 14"]

for i, option in enumerate(options):
    radio_button = tk.Radiobutton(window, text=option, variable=selected_option_var, value=option, command=on_radio_button_click)
    radio_button.place(x=50, y=250 + i * 30)  # Adjust the coordinates as needed


# Create a label to display the selected option
label = tk.Label(window, text="Selected Option: None", font=("Helvetica", 16), fg="white", bg=color1)
x_mid = window.winfo_screenwidth() // 2
y_bottom = window.winfo_screenheight() - 100
screen_height = window.winfo_screenheight()
label.place(x=x_mid, y=y_bottom, anchor=tk.CENTER)  # Adjust the coordinates as needed

draw_logo(canvas)

flower_label = tk.Label(window, text="Select a flower", font=("Helvetica", 16), fg="white", bg=color1)
flower_label.place(x=10, y=500)

# Create a variable to store the selected flower
flower_var = tk.StringVar()

# Create a drop-down menu (OptionMenu) for flower selection
flowers = ["Rose", "Sunflower", "Tulip", "Lily", "Daisy"]
flower_menu = tk.OptionMenu(window, flower_var, *flowers)
flower_menu.config(font=("Helvetica", 14))
flower_menu.place(x=10, y=550)

# Set the default value for the drop-down menu
flower_var.set(flowers[0])

# Bind the selection change event
flower_var.trace_add("write", on_selection_change)

# Create a label to display the selected flower
result_label = tk.Label(window, text="Selected Flower: None", font=("Helvetica", 16), fg="white", bg=color1)
result_label.place(x=10,y=600)

# Raise the flower selection elements to the foreground
flower_label.lift()
flower_menu.lift()

# Start the main event loop
window.mainloop()


# Create 14 radio buttons
# options = ["Astilbe", "Iris", "Bellflower", "Calendula", "Rose",
#         "California Poppy", "Daisy", "Carnation", "Black-Eyed Susan", "Coreopsis",
#         "Tulip", "Dandelion", "Water Lily", "Sunflower"]

