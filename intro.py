import tkinter as tk
import math

def create_circle(canvas, x, y, radius, color="blue"):
    return canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

def on_circle_hover(event):
    item_id = event.widget.find_closest(event.x, event.y)
    if item_id:
        canvas.itemconfig(item_id, fill="red")

def on_circle_leave(event):
    item_id = event.widget.find_closest(event.x, event.y)
    if item_id:
        canvas.itemconfig(item_id, fill="blue")

# Create a Tkinter window
root = tk.Tk()
root.title("Interactive Circles on Hover")

# Number of rows and columns in the grid
rows, columns = 2, 4

# Create a canvas
canvas = tk.Canvas(root, width=400, height=200)
canvas.pack()

# Calculate the spacing between circles
circle_spacing_x = canvas.winfo_reqwidth() / columns
circle_spacing_y = canvas.winfo_reqheight() / rows

# Create circles in the grid and bind hover events
for row in range(rows):
    for col in range(columns):
        x = (col + 0.5) * circle_spacing_x
        y = (row + 0.5) * circle_spacing_y
        radius = min(circle_spacing_x, circle_spacing_y) / 3
        circle_id = create_circle(canvas, x, y, radius)
        canvas.tag_bind(circle_id, "<Enter>", on_circle_hover)
        canvas.tag_bind(circle_id, "<Leave>", on_circle_leave)

# Start the Tkinter event loop
root.mainloop()
