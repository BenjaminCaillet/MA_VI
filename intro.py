import tkinter as tk
import math
from PIL import Image, ImageFilter, ImageGrab, ImageTk, ImageDraw
import matplotlib.pyplot as plt

events = ["Crise 19xx","Crise 20xx","Crise yyyy","Crise ABCD","1234","5678","Un événement important et long","Ceci"]
images_path = ["Images/11sep.png","Images/11sep2.png","Images/11sep.png","Images/11sep.png","Images/11sep.png","Images/11sep.png","Images/11sep.png","Images/Maquette.png"]
events_colors = ["#84848a"] * 4 + ["#84848a"] * 4
events_colors_hover = ["#5f5f63"] * 4 + ["#5f5f63"] * 4



def create_circle(canvas, x, y, radius, color="white"):
    return canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
def create_rectangle(canvas, x, y, radius, color="white"):
    return 1


def create_circle_with_image(canvas, x, y, radius, image_path, text,circle_number):


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

    tk_image = ImageTk.PhotoImage(image)

    # Draw the image inside the circle
    canvas.create_image(x, y, image=tk_image,state=tk.DISABLED,tags=circle_number)
    image_list.append(tk_image)



    # Draw text on top of the image
    canvas.create_text(x, y+radius+40, text=text, font=("Helvetica", 8), fill='black', tags="circle_image_text",state=tk.DISABLED)

    circle_id = create_circle(canvas, x, y, radius+4, color='grey')

    canvas.itemconfig(circle_id, outline="", fill="")
    image_circle_mapping[circle_number] = circle_id
    return circle_id
def on_circle_hover(event):
    item_id = event.widget.find_closest(event.x, event.y)
    item_type = event.widget.type(item_id)
    if item_type=="oval":
        circle_number = int(event.widget.gettags(item_id)[0])  # Get the circle number from tags
        #label.config(text=f"Afficher événement: {events[circle_number-1]}")  # Update the label text
        #canvas.itemconfig(item_id, fill=events_colors_hover[circle_number-1])

        # Déplacer le texte explicatif à gauche ou à droite
        x, y, _, _ = event.widget.coords(item_id)
        h_l=explanation_label.winfo_height()
        w_l=explanation_label.winfo_width()
        if x < canvas.winfo_reqwidth() / 2:
            explanation_label.place(x=x + (radius+4)*2 +40, y=y+radius-(h_l/2))
        else:
            explanation_label.place(x=x -w_l - 40, y=y+radius-(h_l/2))
        explanation_label.config(text=f"Afficher événement: {events[circle_number-1]}")
    elif item_type =="image":
        circle_number = int(event.widget.gettags(item_id)[0])
        item_id = image_circle_mapping[circle_number]
        label.config(text=f"Afficher événement: {events[circle_number-1]}")  # Update the label text
        #canvas.itemconfig(item_id, fill=events_colors_hover[circle_number-1])

        # Déplacer le texte explicatif à gauche ou à droite
        x, y, _, _ = event.widget.coords(item_id)
        h_l=explanation_label.winfo_height()
        w_l=explanation_label.winfo_width()
        if x < canvas.winfo_reqwidth() / 2:
            explanation_label.place(x=x + (radius+4)*2 +40, y=y+radius-(h_l/2))
        else:
            explanation_label.place(x=x -w_l - 40, y=y+radius-(h_l/2))

def on_circle_leave(event):
    item_id = event.widget.find_closest(event.x, event.y)
    item_type = event.widget.type(item_id)
    if item_type=="oval":
        circle_number = int(event.widget.gettags(item_id)[0])  # Get the circle number from tags
        #canvas.itemconfig(item_id, fill=events_colors[circle_number-1])
        label.config(text="")  # Clear the label when leaving a circle
        explanation_label.place_forget()  # Cacher le texte explicatif
    elif item_type =="image":
        circle_number = int(event.widget.gettags(item_id)[0])
        item_id=image_circle_mapping[circle_number]
        #anvas.itemconfig(item_id, fill=events_colors[circle_number - 1])
        label.config(text="")  # Clear the label when leaving a circle
        explanation_label.place_forget()  # Cacher le texte explicatif



def on_circle_click(event):
    item_id = event.widget.find_closest(event.x, event.y)
    if item_id:
        circle_number = int(event.widget.gettags(item_id)[0])  # Get the circle number from tags
        # Handle the click event - you can customize this part
        print(f"Clicked on circle: {events[circle_number-1]}")









image_circle_mapping = {}
# Create a Tkinter window
intro = tk.Tk()
intro.title("Interactive Circles with Label")

# Number of rows and columns in the grid
rows, columns = 2, 4

# Create a canvas
windos_w=1920
windos_h=1080
canvas = tk.Canvas(intro, width=windos_w, height=windos_h,bg='white')
canvas.pack()

#creat a image list for the save
image_list=[]
# Create a Label at the top
label = tk.Label(intro, text="", font=("Helvetica", 12),state=tk.DISABLED)
label.pack(side=tk.TOP)


# Create a Label of circle
explanation_label = tk.Label(intro, text="C'est un text test pour l'instant", font=("Helvetica", 10),state=tk.DISABLED)
explanation_label.config(bg="white")
explanation_label.place_forget()  # Initialiser en tant que caché



# Calculate the spacing between circles
circle_spacing_x = canvas.winfo_reqwidth() / columns
circle_spacing_y = canvas.winfo_reqheight() / rows
radius = int(min(circle_spacing_x, circle_spacing_y) / 3)
# Create circles in the grid, bind hover events, and add circle numbers as tags
for row in range(rows):
    for col in range(columns):
        x = (col + 0.5) * circle_spacing_x
        y = (row + 0.5) * circle_spacing_y
        circle_idx = 4*(row) + (col)
        print(circle_idx,row,col)
        circle_number = row * columns + col + 1
        circle_id = create_circle_with_image(canvas, x, y, radius,images_path[circle_idx],events[circle_idx],circle_number)
        #canvas.create_text(x, y, text=events[circle_idx], font=("Helvetica", 8), fill='white')
        canvas.addtag_withtag(circle_number, circle_id)  # Add circle number as a tag
        canvas.tag_bind(circle_id, "<Enter>", on_circle_hover)
        canvas.tag_bind(circle_id, "<Leave>", on_circle_leave)
        
         # Bind the click event to the circle
        canvas.tag_bind(circle_id, "<Button-1>", on_circle_click)

# Start the Tkinter event loop
intro.mainloop()
