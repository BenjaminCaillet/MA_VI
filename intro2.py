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
    button.configure(width=0, height=0, border_width=0,corner_radius=0,fg_color="transparent",border_spacing=0)

    # Pack the button at the specified position
    button.place(x=x - radius, y=y - radius)

    button.bind("<Enter>", lambda event: button_enter(event, button_id))
    button.bind("<Leave>", lambda event: button_leave(event, button_id))
    button.configure(text=text,hover=True,compound="top",anchor="S")

    return button

def button_click(button_id):
        # Handle the click event - you can customize this part
        print(f"Clicked on circle: {events[button_id - 1]}")

def button_enter(event,button_id):

    explanation_label.configure(text=f"Afficher événement: {events[button_id]}")
    # Déplacer le texte explicatif à gauche ou à droite
    circle_idx = 4 * (row) + (col)
    row_b=int(button_id/4)
    col_b=button_id%4
    x_b = (col_b + 0.5) * circle_spacing_x
    y_b = (row_b + 0.5) * circle_spacing_y
    w_b = explanation_label.winfo_reqwidth()
    if col_b <  2:
        explanation_label.place(x=x_b+radius+30, y=y_b)
    else:
        explanation_label.place(x=x_b-30-w_b, y=y_b)
    for id in range(rows*columns):
        if id != button_id:
            button=button_map[id]
            button.place_forget()



def button_leave(event,button_id):
    for row in range(rows):
        for col in range(columns):
            x = (col + 0.5) * circle_spacing_x
            y = (row + 0.5) * circle_spacing_y
            circle_idx = 4 * (row) + (col)
            button=button_map[circle_idx]
            button.place(x=x - radius, y=y - radius)
    explanation_label.place_forget()




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
        button= create_circle_button_with_image(app, x, y, radius,images_path[circle_idx],events[circle_idx],circle_idx)
        button_map[circle_idx] = button

# Create a Label of circle
explanation_label = tk.CTkLabel(app, text="C'est un text test pour l'instant", font=("Helvetica", 10),state="disabled")
explanation_label.configure(fg_color="white")
explanation_label.place()
#explanation_label.place_forget()  # Initialiser en tant que caché




# Start the Tkinter event loop
app.mainloop()
