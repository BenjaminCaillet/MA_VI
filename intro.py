import tkinter as tk
import math

events = ["Crise 19xx","Crise 20xx","Crise yyyy","Crise ABCD","1234","5678","Un événement important et long","Ceci"]
events_colors = ["#84848a"] * 4 + ["#84848a"] * 4
events_colors_hover = ["#5f5f63"] * 4 + ["#5f5f63"] * 4



def create_circle(canvas, x, y, radius, color="white"):
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
        
def on_circle_click(event):
    item_id = event.widget.find_closest(event.x, event.y)
    if item_id:
        circle_number = int(event.widget.gettags(item_id)[0])  # Get the circle number from tags
        # Handle the click event - you can customize this part
        print(f"Clicked on circle: {events[circle_number-1]}")

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
        circle_id = create_circle(canvas, x, y, radius, color='grey')
        circle_number = row * columns + col + 1
        canvas.create_text(x, y, text=events[circle_idx], font=("Helvetica", 8), fill='white')
        canvas.addtag_withtag(circle_number, circle_id)  # Add circle number as a tag
        canvas.tag_bind(circle_id, "<Enter>", on_circle_hover)
        canvas.tag_bind(circle_id, "<Leave>", on_circle_leave)
        
         # Bind the click event to the circle
        canvas.tag_bind(circle_id, "<Button-1>", on_circle_click)

# Start the Tkinter event loop
intro.mainloop()
