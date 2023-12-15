import customtkinter as tk
import numpy as np
from PIL import Image, ImageDraw


# events names
# events = ["Crise 19xx","Crise 20xx","Crise yyyy","Crise ABCD","1234","5678","Un événement important et long","Ceci"]
events = ["Tchernobyl + Schweizerhalle 1986","Crise du chômage de 1992",
          "Union Européenne dès 1992","Répartition F/H de 1971 à 1995",
          "Accords Bilatéraux II 2005","Fukushima 2011",
          "Manifestations Climat 2018","Répartition F/H de 1995 à 2019"]
images_path = ["Images/Tchernobyl.PNG","Images/chomage.png",
               "Images/Europe.png","Images/FemStrike1991.png",
               "Images/Bilateral.png","Images/Fukushima.png",
               "Images/ClimateStrike.png","Images/FemStrike2014.png"]

events_descriptions_part1= [
    """
    L'accident nucléaire de Tchernobyl en 1986, et plus localement l'accident
    de Schweizerhalle, ont attisés les débats sur la sécurité nucléaire et industrielle.
    L'heure est à la question de l'environnement, et l'impact de la société sur celui-ci.
    Le Parti Ecologiste Suisse (futurs Vert-es) prend de l'envergure.
    """,
    """
    La crise de l'emploi de 1992, marquée par une augmentation significative du chômage, 
    a engendré des tensions économiques et sociales. Les élections de 1995 ont été fortement influencées 
    par ces préoccupations économiques, mettant en lumière les propositions des candidats pour 
    faire face à la crise et stimuler l'emploi.
    """,
    """
    Avec le traité de Maastricht de 1992, la construction de l'Union Européenne a démarré, mais en Suisse, le rejet
    par référendum à l'Espace Economique Européen la même année a marqué la position du peuple.
    Lors des élections de 1995, puis de 1999, les débats ont porté sur les implications de cette intégration, 
    les relations internationales et la souveraineté nationale, faisant de l'Europe un enjeu central de la campagne.
    L'UDC, parti souverainiste, s'est démarqué des partis de droite plus économiques et plus pro-européens. 
    """,
    """
    ...
    """,
]
events_descriptions_part2= [
    """
    Les Accords Bilatéraux II, signés avec l'Union Européenne en 2005, ont ravivé les débats
    sur la relation entre la Suisse et l'UE. En 2007, les élections ont été marquées par ses débats, 
    renforçant entre autre la position nationaliste de l'UDC.
    """,
    """
    La catastrophe nucléaire de Fukushima en 2011 (Japon), a suscité des inquiétudes quant à la sûreté nucléaire. 
    Cette catastrophe a eu un impact direct sur l'opinion publique suisse, influençant les élections de la
    même année sur la place du nucléaire dans le mix énergétique du pays. Les Verts Libéraux ont pu
    sortir leur épingle du jeu, aux dépends des Vert-es.
    """,
    """
    En 2018, les "Grèves du Climat" et autres manifestations écologistes ont attiré l'attention sur 
    l'urgence climatique. Les élections de 2019 ont été fortement marquées par ces préoccupations, 
    résultant en une "vague verte" sur les résultats.
    """,
    """
    ...
    """,
]

events_descriptions = events_descriptions_part1 + events_descriptions_part2

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
    image_map[button_id]=tk_image

    # Creat the tranparent image
    image = image.convert("RGBA")
    pixels = np.array(image)
    pixels[:, :, 3] = 50
    new_image = Image.fromarray(pixels, "RGBA")

    # Appliquez le masque à l'image
    image = Image.new("RGBA", (int(2 * radius), int(2 * radius)), (255, 255, 255, 0))
    image.paste(new_image, (0, 0), mask)


    tk_new_image = tk.CTkImage(image, image, (int(2 * radius), int(2 * radius)))

    image_trans_map[button_id]=tk_new_image

    # Create the circular button
    button = tk.CTkButton(window, image=tk_image, command=lambda :button_click(button_id))
    button.configure(width=0, height=0, border_width=0,corner_radius=0,fg_color="transparent",border_spacing=0)

    # Pack the button at the specified position
    button.place(x=x - radius, y=y - radius)

    button.bind("<Enter>", lambda event: button_enter(event, button_id))
    button.bind("<Leave>", lambda event: button_leave(event, button_id))
    button.configure(text=text,hover=False,compound="top",anchor="S")
    button.configure(text_color="#FFFFFF")
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
            button.configure(image=image_trans_map[id])
            button.configure(text_color="#323232")



def button_leave(event,button_id):

    for row in range(rows):
        for col in range(columns):
            x = (col + 0.5) * circle_spacing_x
            y = (row + 0.5) * circle_spacing_y
            circle_idx = 4 * (row) + (col)
            button=button_map[circle_idx]
            button.place(x=x - radius, y=y - radius)
            button.configure(image=image_map[circle_idx])
            button.configure(text_color="#FFFFFF")
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
image_map={}
image_trans_map={}
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
