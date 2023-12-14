import customtkinter as tk
import math
from PIL import Image, ImageFilter, ImageGrab, ImageTk, ImageDraw
import matplotlib.pyplot as plt

events = ["Crise 19xx","Crise 20xx","Crise yyyy","Crise ABCD","1234","5678","Un événement important et long","Ceci"]
images_path = ["Images/11sep.png","Images/11sep2.png","Images/11sep.png","Images/11sep.png","Images/11sep.png","Images/11sep.png","Images/11sep.png","Images/Maquette.png"]
events_colors = ["#84848a"] * 4 + ["#84848a"] * 4
events_colors_hover = ["#5f5f63"] * 4 + ["#5f5f63"] * 4


def create_circle_button_with_image(window, x, y, radius, image_path, text,button_id):

    # Chargez l'image
    original_image = Image.open(image_path)
    original_image = original_image.resize((int(2 * radius), int(2 * radius)), Image.LANCZOS)

    # Créez un masque circulaire
    mask = Image.new("L", (int(2 * radius), int(2 * radius)), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, int(2 * radius), int(2 * radius)), fill=255)

    # Appliquez le masque à l'image
    image = Image.new("RGBA", (int(2 * radius), int(2 * radius)), (255, 255, 255, 0))
    image.paste(original_image, (0, 0), mask)

    tk_image = tk.CTkImage(image,image,(int(2 * radius), int(2 * radius)))

    # Create the circular button
    button = tk.CTkButton(window, image=tk_image, command=lambda :button_click(button_id))
    button.configure(width=2 * radius, height=2 * radius, border_width=0,corner_radius=0,anchor="w",fg_color="transparent")

    # Pack the button at the specified position
    button.place(x=x - radius, y=y - radius)

    button.bind("<Enter>", lambda event: button_enter(event, button_id))
    button.bind("<Leave>", lambda event: button_leave(event, button_id))
    button.configure(text="")
    # Create a label for the text
    label = tk.CTkLabel(window, text=text)
    label.place(x=x, y=y + radius+10)
    return button,label


def on_circle_hover(event):
    item_id = event.widget.find_closest(event.x, event.y)
    item_type = event.widget.type(item_id)
    if (item_type=="oval") or (item_type=="image"):
        if item_type=="oval":
            circle_number = int(event.widget.gettags(item_id)[0])  # Get the circle number from tags
        elif item_type =="image":
            circle_number = int(event.widget.gettags(item_id)[0])
            item_id = image_circle_mapping[circle_number]
        label.configure(text=f"Afficher événement: {events[circle_number-1]}")  # Update the label text
        #canvas.itemconfig(item_id, fill=events_colors_hover[circle_number-1])

        # Déplacer le texte explicatif à gauche ou à droite
        x, y, _, _ = event.widget.coords(item_id)
        h_l=explanation_label.winfo_height()
        w_l=explanation_label.winfo_width()
        if x < app.winfo_reqwidth() / 2:
            explanation_label.place(x=x + (radius+4)*2 +40, y=y+radius-(h_l/2))
        else:
            explanation_label.place(x=x -w_l - 40, y=y+radius-(h_l/2))

        for i, tk_image in enumerate(image_list):
            if i + 1 == circle_number:
                continue  # Skip the current image
            app.itemconfig(image_circle_mapping[i + 1], state="hidden")

def on_circle_leave(event):
    item_id = event.widget.find_closest(event.x, event.y)
    item_type = event.widget.type(item_id)
    if (item_type == "oval") or (item_type == "image"):
        if item_type=="oval":
            circle_number = int(event.widget.gettags(item_id)[0])  # Get the circle number from tags
            #canvas.itemconfig(item_id, fill=events_colors[circle_number-1])
        elif item_type =="image":
            circle_number = int(event.widget.gettags(item_id)[0])
            item_id=image_circle_mapping[circle_number]
            #anvas.itemconfig(item_id, fill=events_colors[circle_number - 1])
        label.config(text="")  # Clear the label when leaving a circle
        explanation_label.place_forget()  # Cacher le texte explicatif

        for i, tk_image in enumerate(image_list):
            app.itemconfig(image_circle_mapping[i + 1], state="normal")

def button_click(button_id):
        # Handle the click event - you can customize this part
        print(f"Clicked on circle: {events[button_id - 1]}")

def button_enter(event,button_id):

    label.configure(text=f"Afficher événement: {events[button_id - 1]}")
    button=button_map[button_id]
    # Déplacer le texte explicatif à gauche ou à droite
    x = button.winfo_x()
    y = button.winfo_y()
    h_l = explanation_label.cget("height")
    w_l = explanation_label.cget("width")
    if x < app.winfo_reqwidth() / 2:
        explanation_label.place(x=x + (radius + 4) * 2 + 40, y=y + radius - (h_l / 2))
    else:
        explanation_label.place(x=x - w_l - 40, y=y + radius - (h_l / 2))

    for i, tk_image in enumerate(image_list):
        if i + 1 == circle_number:
            continue  # Skip the current image
        app.itemconfig(image_circle_mapping[i + 1], state="hidden")




def button_leave(event,button_id):
    for id in range(rows*columns):
        if id != button_id:
            button=button_map[id]
            button.place()



image_circle_mapping = {}
# Create a Tkinter window
app = tk.CTk()
app.title("Interactive Circles with Label")
# Number of rows and columns in the grid
rows, columns = 2, 4
windos_w=1600
windos_h=800
app.geometry("{}x{}".format(windos_w,windos_h))


#creat a image list for the save
image_list=[]
button_map = {}

# Create a Label at the top
label = tk.CTkLabel(app, text="", font=("Helvetica", 12),state=tk.DISABLED)



# Create a Label of circle
explanation_label = tk.CTkLabel(app, text="C'est un text test pour l'instant", font=("Helvetica", 10),state=tk.DISABLED)
explanation_label.configure(fg_color="white")
explanation_label.place_forget()  # Initialiser en tant que caché



# Calculate the spacing between circles
circle_spacing_x = windos_w / columns

circle_spacing_y = windos_h / rows

radius = int(min(circle_spacing_x, circle_spacing_y) / 3)
# Create circles in the grid, bind hover events, and add circle numbers as tags
for row in range(rows):
    for col in range(columns):
        x = (col + 0.5) * circle_spacing_x
        y = (row + 0.5) * circle_spacing_y
        circle_idx = 4*(row) + (col)
        print(circle_idx,row,col)
        circle_number = row * columns + col + 1
        button,label_id = create_circle_button_with_image(app, x, y, radius,images_path[circle_idx],events[circle_idx],circle_idx)
        button_map[circle_idx] = button

# Start the Tkinter event loop
app.mainloop()
