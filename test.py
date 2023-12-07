import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

def create_circle_image(canvas, x, y, radius, image_path):
    # Chargez l'image
    original_image = Image.open(image_path)
    original_image = original_image.resize((2 * radius, 2 * radius), Image.LANCZOS)

    # Créez un masque circulaire
    mask = Image.new("L", (2 * radius, 2 * radius), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 2 * radius, 2 * radius), fill=255)

    # Appliquez le masque à l'image
    image = Image.new("RGBA", (2 * radius, 2 * radius), (255, 255, 255, 0))
    image.paste(original_image, (0, 0), mask)

    tk_image = ImageTk.PhotoImage(image)
    image_list.append(tk_image)

    # Créez le cercle sur le canevas
    #canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill='white', outline='black')

    # Placez l'image dans le cercle
    canvas.create_image(x, y, image=tk_image,anchor=tk.CENTER)


root = tk.Tk()
root.title("Images dans deux Cercles")

# Créez un canevas Tkinter
canvas = tk.Canvas(root, width=400, height=200)
canvas.pack()
image_list = []

# Spécifiez les coordonnées du centre du premier cercle, le rayon et le chemin de la première image
center_x1, center_y1 = 100, 100
circle_radius1 = 50
image_path1 = "Images/11sep.png"  # Remplacez par le chemin de votre première image

# Appelez la fonction pour créer le premier cercle avec la première image
create_circle_image(canvas, center_x1, center_y1, circle_radius1, image_path1)

# Spécifiez les coordonnées du centre du deuxième cercle, le rayon et le chemin de la deuxième image
center_x2, center_y2 = 300, 100
circle_radius2 = 50
image_path2 = "Images/Maquette.png"  # Remplacez par le chemin de votre deuxième image

# Appelez la fonction pour créer le deuxième cercle avec la deuxième image
create_circle_image(canvas, center_x2, center_y2, circle_radius2, image_path2)

# Lancez la boucle principale Tkinter
root.mainloop()
