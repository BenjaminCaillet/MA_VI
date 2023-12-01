import tkinter as tk
import math

events = ["Crise 19xx","Crise 20xx","Crise yyyy","Crise ABCD",      "1234","5678","Un événement important et long","Ceci",]
events_colors = ["#0000FF"] * 4 + ["#FF0000"] * 4
events_colors_hover = ["#0000cc"] * 4 + ["#cc0000"] * 4



def create_circle(canvas, x, y, radius, color="blue"):
    return canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

def on_circle_hover(event):
    item_id = event.widget.find_closest(event.x, event.y)
    if item_id:
        circle_number = int(event.widget.gettags(item_id)[0])  # Get the circle number from tags
        label.config(text=f"Afficher événement: {events[circle_number-1]}")  # Update the label text
        canvas.itemconfig(item_id, fill=events_colors_hover[circle_number-1])

def on_circle_leave(event):
    item_id = event.widget.find_closest(event.x, event.y)
    if item_id:
        circle_number = int(event.widget.gettags(item_id)[0])  # Get the circle number from tags
        canvas.itemconfig(item_id, fill=events_colors[circle_number-1])
        label.config(text="")  # Clear the label when leaving a circle

# Create a Tkinter window
intro = tk.Tk()
intro.title("Interactive Circles with Label")

# Number of rows and columns in the grid
rows, columns = 2, 4

# Create a canvas
canvas = tk.Canvas(intro, width=600, height=400)
canvas.pack()

# Create a Label at the top
label = tk.Label(intro, text="", font=("Helvetica", 12))
label.pack(side=tk.TOP)

# Calculate the spacing between circles
circle_spacing_x = canvas.winfo_reqwidth() / columns
circle_spacing_y = canvas.winfo_reqheight() / rows

# Create circles in the grid, bind hover events, and add circle numbers as tags
for row in range(rows):
    for col in range(columns):
        x = (col + 0.5) * circle_spacing_x
        y = (row + 0.5) * circle_spacing_y
        radius = min(circle_spacing_x, circle_spacing_y) / 3
        circle_idx = 4*(row) + (col)
        print(circle_idx,row,col)
        circle_id = create_circle(canvas, x, y, radius, color=events_colors[circle_idx])
        circle_number = row * columns + col + 1
        canvas.addtag_withtag(circle_number, circle_id)  # Add circle number as a tag
        canvas.tag_bind(circle_id, "<Enter>", on_circle_hover)
        canvas.tag_bind(circle_id, "<Leave>", on_circle_leave)

# Start the Tkinter event loop
intro.mainloop()
