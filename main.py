from pyaxis import pyaxis
import matplotlib.pyplot as plt
import customtkinter as tk
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from TimeSeries.timeSeries import plot_party, plot_gender, party_list, party_list_complet, french_to_german
from Parliament.parliament import plot_parliament
from util.translate import party_french_to_german
from PIL import Image, ImageFilter, ImageGrab, ImageTk, ImageDraw
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import Map.map as gc
from Map.info import french_to_german_party, party_list_complet, party_list,canton_list,type_map_list,gender_list,french_to_german_gender,dictionary_canton_to_german
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

events = ["Tchernobyl + Schweizerhalle 1986","Crise du chômage de 1992",
          "Union Européenne dès 1992","Répartition F/H de 1971 à 1995",
          "Accords Bilatéraux II 2005","Fukushima 2011",
          "Manifestations Climat 2018","Répartition F/H de 1995 à 2019"]
dates = ["1986","1992","1992","1971","2005","2011","2018","1995"]
images_path = ["Images/Tchernobyl.PNG","Images/chomage.png",
               "Images/Europe.png","Images/FemStrike1991.png",
               "Images/Bilateral.png","Images/Fukushima.png",
               "Images/ClimateStrike.png","Images/FemStrike2014.png"]
event_id = 0

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
    """,
]
label_weight=[0,0,1000,500,0,0,1000,1000]
label_high = [0,-60,0,0,0,0,0,0]

events_descriptions = events_descriptions_part1 + events_descriptions_part2

events_colors = ["#84848a"] * 4 + ["#84848a"] * 4
events_colors_hover = ["#5f5f63"] * 4 + ["#5f5f63"] * 4

# Setting up theme of the app
customtkinter.set_appearance_mode("light")

# Parse the dataset
fp = r"Dataset/Dataset.px"
px = pyaxis.parse(uri=fp, encoding='ANSI')
data_df = px['DATA']
image_map={}
image_trans_map={}

switzerland = gc.creat_geoswitz('Dataset/Swiss.geojson')

def button_click(button_id):
    # Handle the click event
    global event_id
    event_id = button_id
    selected_year = dates[button_id]
    jahr_textbox_1.set(selected_year)
    canton_combobox.set(selected_canton)
    gender_combobox.set(selected_gender)
    type_map_combobox.set(selected_map_mod)
    gender_map_combobox.set(selected_map_gender)
    
    if event_id == 0 :
        party_map_combobox.set("PES")
    if event_id == 1 :
        party_map_combobox.set("PS")
    if event_id == 2 :
        party_map_combobox.set("UDC")
    if event_id == 3 :
        party_map_combobox.set("PS")
        type_map_combobox.set("Evolution genre")
        gender_combobox.set("Homme/Femme")
        gender_map_combobox.set("Femme")
    if event_id == 4 :
        party_map_combobox.set("UDC")
    if event_id == 5 :
        party_map_combobox.set("PES")
    if event_id == 6 :
        party_map_combobox.set("PES")
    if event_id == 7 :
        party_map_combobox.set("PS")
        type_map_combobox.set("Evolution genre")
        gender_combobox.set("Homme/Femme")
        gender_map_combobox.set("Femme")
    mapConfig()
    displayMain()

def button_enter(event,button_id):
    # Déplacer le texte explicatif à gauche ou à droite
    row_b = int(button_id / 4)
    col_b = button_id % 4
    x_b = (col_b + 0.5) * circle_spacing_x
    if row == 0 :
        y_b = (row_b + 0.6) * circle_spacing_y
    else :
        y_b = (row_b + 0.5) * circle_spacing_y

    if col_b < 2:
        label_map[button_id].place(x=x_b + radius + 30, y=y_b+label_high[button_id])
    else:
        label_map[button_id].place(x=x_b - 30 - label_weight[button_id], y=y_b+label_high[button_id])

    for id in range(rows*columns):
        if id != button_id:
            button=button_map[id]
            button.configure(image=image_trans_map[id])
            button.configure(text_color="#323232")

def button_leave(event,button_id):
    for row in range(rows):
        for col in range(columns):
            x = (col + 0.5) * circle_spacing_x
            if row == 0 :
                y = (row + 0.6) * circle_spacing_y
            else :
                y = (row + 0.5) * circle_spacing_y
            circle_idx = 4 * (row) + (col)
            button=button_map[circle_idx]
            button.place(x=x - radius, y=y - radius)
            button.configure(image=image_map[circle_idx])
            button.configure(text_color="#000000")
    label_map[button_id].place_forget()

def create_circle_button_with_image(window, x, y, radius, image_path, text, button_id):
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
    button = tk.CTkButton(pageIntro, image=tk_image, command=lambda :button_click(button_id))
    button.configure(width=0, height=0, border_width=0,corner_radius=0,fg_color="transparent",border_spacing=0)

    # Pack the button at the specified position
    button.place(x=x - radius, y=y - radius)

    button.bind("<Enter>", lambda event: button_enter(event, button_id))
    button.bind("<Leave>", lambda event: button_leave(event, button_id))
    button.configure(text=text,hover=False,compound="top",anchor="S")
    button.configure(text_color="#000000")
    return button

def updatePlotTime(selected_party):
    translated_list = [french_to_german[party] for party in selected_party]
    canton = canton_combobox.get()
    canton = dictionary_canton_to_german[canton]
    year = jahr_textbox_1.get()
    
    if gender_combobox.get() == "Total" :
        figTime = plot_party(data_df,translated_list, canton,year)
    else :
        figTime = plot_gender(data_df, canton,year)
    figTime.set_size_inches(14,4)
    canvasTime = FigureCanvasTkAgg(figTime, master=pageMain)
    canvas_widget_time = canvasTime.get_tk_widget()
    canvas_widget_time.grid(row=0, column=3, columnspan=20, rowspan=9)
    canvasTime.draw()

def updatePlotParlement(dateLow,dateHigh):
    #First plot
    jahr = dateLow
    
    figParlement_1 = plot_parliament(data_df, jahr, point_size=50)
    figParlement_1.set_size_inches(5,3)

    canvasParlement_1 = FigureCanvasTkAgg(figParlement_1, master=pageMain)
    canvas_widget_parlement_1 = canvasParlement_1.get_tk_widget()
    canvas_widget_parlement_1.grid(row=3, column=12, columnspan=7,rowspan=20)
    canvasParlement_1.draw()
    
    #Second plot
    jahr = dateHigh
    figParlement_2 = plot_parliament(data_df, jahr, point_size=50, legend=True)
    figParlement_2.set_size_inches(5,3)

    canvasParlement_2 = FigureCanvasTkAgg(figParlement_2, master=pageMain)
    canvas_widget_parlement_2 = canvasParlement_2.get_tk_widget()
    canvas_widget_parlement_2.grid(row=13, column=12, columnspan=7,rowspan=20)
    canvasParlement_2.draw()
    
def mapConfig():
    type = type_map_combobox.get()
    if type == "Evolution genre":
        party_map_combobox.grid_remove()
        party_map_label.grid_remove()
        gender_map_combobox.grid(row=15, column=2, padx=0, pady=0)
        gender_map_label.grid(row=15, column=1, padx=0, pady=0)
    else :
        gender_map_combobox.grid_remove()
        gender_map_label.grid_remove()
        party_map_combobox.grid(row=15, column=2, padx=0, pady=0)
        party_map_label.grid(row=15, column=1, padx=0, pady=0)
        
    mapCallback()
    
def mapCallback():
    result = find_closest_dates(jahr_textbox_1.get(),jahr_list)
    dateHigh = result[0]
    dateLow = result[1]
    updatePlotMap(dateLow,dateHigh)
    
def dateCallback():
    global event_id
    event_id = 0
    displayAll()
    
def updatePlotMap(dateLow,dateHigh):
    type = type_map_combobox.get()
    party = party_map_combobox.get()
    gender = gender_map_combobox.get()
    if type == "Evolution genre":
        gender_t=french_to_german_gender[gender]
        fig = gc.plot_diff_gender(switzerland,data_df, gender_t, dateLow, dateHigh)
    elif type == "Meilleur parti":
        fig=gc.plot_best_party(switzerland,data_df,dateHigh)
    else:
        party_t=french_to_german_party[party]
        fig=gc.plot_nb_elu_party(switzerland,data_df, party_t, dateLow, dateHigh)
    fig.set_size_inches(8,6)
    canvas = FigureCanvasTkAgg(fig, master=pageMain)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=6, column=3, columnspan=10,rowspan=22)
    canvas.draw()
    
def open_selection_popup():
    # Create a popup
    popup = tk.CTkToplevel(pageMain)
    popup.title("Sélection du parti")

    # Set a fixed height
    popup_height = 400
    popup.geometry(f'200x{popup_height}')

    # Create a container frame
    container = tk.CTkFrame(popup)
    container.pack(fill='both', expand=True)

    # Create a canvas and attach a scrollbar to it
    canvas = tk.CTkCanvas(container)
    scrollbar = tk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack the scrollbar to the right and fill in the Y direction
    scrollbar.pack(side="right", fill="y")

    # Pack the canvas to expand and fill in both directions
    canvas.pack(side="left", fill="both", expand=True)

    # Create a frame inside the canvas to hold the widgets
    checkbox_frame = tk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=checkbox_frame, anchor="nw")

    # Variables to store checkbox states
    vars_ = [tk.BooleanVar() for _ in party_list_complet]

    # Create checkboxes for each item
    checkboxes = []
    for i, item in enumerate(party_list_complet):
        cb = tk.CTkCheckBox(checkbox_frame, text=item, variable=vars_[i])
        cb.pack(anchor="w", padx=10, pady=5)
        checkboxes.append(cb)

    # Update the scrollregion of the canvas to encompass the checkbox frame
    checkbox_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # OK button to print selected party and destroy popup
    def confirm_selection():
        selected_party = [item for i, item in enumerate(party_list_complet) if vars_[i].get()]
        updatePlotTime(selected_party)
        popup.destroy()

    ok_button = tk.CTkButton(popup, text="OK", command=confirm_selection)
    ok_button.pack(after=container, anchor="center", pady=10)

def find_closest_dates(date_str, jahr_list):
    date = int(date_str)
    jahr_list = [int(year) for year in jahr_list]
    jahr_list.sort()
    
    closest1 = None
    closest2 = None
    
    for i in range(len(jahr_list)) :
        if i > 0 & i < len(jahr_list):
            if (date > jahr_list[i]) and (date <= jahr_list[i+1]) :
                closest1 = jahr_list[i+1]
                closest2 = jahr_list[i]
                break
    global event_id
    if event_id == 3 :
        closest1 = 1995
        closest2 = 1971
    if event_id == 7 :
        closest1 = 2019
        closest2 = 1995
    return [str(closest1), str(closest2)]

def create_circle(canvas, x, y, radius, color="white"):
    return canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

def on_circle_hover(event):
    item_id = event.widget.find_closest(event.x, event.y)
    if item_id:
        circle_number = int(event.widget.gettags(item_id)[0])  # Get the circle number from tags
        canvas.itemconfig(item_id, fill=events_colors_hover[circle_number-1])

def on_circle_leave(event):
    item_id = event.widget.find_closest(event.x, event.y)
    if item_id:
        circle_number = int(event.widget.gettags(item_id)[0])  # Get the circle number from tags
        canvas.itemconfig(item_id, fill=events_colors[circle_number-1])
        
def on_circle_click(event):
    item_id = event.widget.find_closest(event.x, event.y)
    if item_id:
        circle_number = int(event.widget.gettags(item_id)[0])  # Get the circle number from tags
        jahr_textbox_1.set(dates[circle_number])
        displayAll()
    
def _quit():
    window.quit()
    window.destroy()
    
def displayAll():
    result = find_closest_dates(jahr_textbox_1.get(),jahr_list)
    dateHigh = result[0]
    dateLow = result[1]
    updatePlotTime(selected_party)
    updatePlotParlement(dateLow,dateHigh)
    updatePlotMap(dateLow,dateHigh)
    
def displayIntro():
    pageMain.place(relx=2, rely=2,anchor=tk.CENTER)
    pageIntro.place(relx=0.5, rely=0.5,anchor=tk.CENTER)
    
def displayMain():
    pageIntro.place(relx=2, rely=2,anchor=tk.CENTER)
    pageMain.place(relx=0.5, rely=0.53,anchor=tk.CENTER)
    updatePlotTime(selected_party)
    displayAll()

windos_w=1920
windos_h=1080

selected_canton = "Suisse"
selected_gender = "Total"
selected_year = "2010"
selected_map_mod = "Evolution parti"
selected_parti = "PS"
selected_map_gender = "Homme"

button_id_ = 0

# GUI setup
window = tk.CTk()
window.geometry("1920x1080")
#window.after(0, lambda:window.state('zoomed'))
pageMain = tk.CTkFrame(window,windos_w,windos_h)

window.title("Sélection du parti et du canton")

canvas = tk.CTkCanvas(pageMain,width=1920, height=1080, bg='white')
canvas.grid(row=0, column=0, columnspan=21,rowspan=25)

# PLOT PART

# Button to open the popup
btn = tk.CTkButton(pageMain, text="Retour", command=displayIntro,bg_color="white")
btn.grid(row=1, column=0, padx=0, pady=0)

# Button to open the popup
btn = tk.CTkButton(pageMain, text="Sélection des partis", command=open_selection_popup,bg_color="white")
btn.grid(row=3, column=2, padx=0, pady=0)

selected_party = party_list

# Canton dropdown
canton_label = tk.CTkLabel(pageMain, text="Canton:",bg_color="white")
canton_label.grid(row=4, column=1, padx=0, pady=0)
canton_list = ['Suisse','Grisons','Berne','Valais','Vaud','Tessin','Saint-Gall','Zurich','Fribourg','Lucerne','Argovie','Uri','Thurgovie','Schwyz','Jura','Neuchâtel','Soleure','Glaris','Bâle-Campagne','Obwald','Nidwald','Genève','Schaffhouse','Appenzell Rhodes-Extérieures','Zoug',' Bâle-Ville']
canton_combobox = tk.CTkComboBox(pageMain, values=canton_list,state="readonly", command=lambda value: updatePlotTime(selected_party))
canton_combobox.grid(row=4, column=2, padx=0, pady=0)
canton_combobox.set(selected_canton)

# Gender dropdown
gender_label = tk.CTkLabel(pageMain, text="Genre:",bg_color="white")
gender_label.grid(row=5, column=1, padx=0, pady=0)
gender_combobox = tk.CTkComboBox(pageMain, values=["Total","Homme/Femme"],state="readonly", command=lambda value: updatePlotTime(selected_party))
gender_combobox.grid(row=5, column=2, padx=0, pady=0)
gender_combobox.set(selected_gender)

every_year = ["2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998", "1997", "1996", "1995", "1994", "1993", "1992", "1991", "1990", "1989", "1988", "1987", "1986", "1985", "1984", "1983", "1982", "1981", "1980", "1979", "1978", "1977", "1976", "1975", "1974", "1973", "1972", "1971"]

# Jahr dropdown
jahr_label_1 = tk.CTkLabel(pageMain, text="Année:",bg_color="white")
jahr_label_1.grid(row=1, column=1, padx=0, pady=0)
jahr_textbox_1 = tk.CTkComboBox(pageMain, values=every_year, command=lambda value: dateCallback())
jahr_textbox_1.grid(row=1, column=2, padx=0, pady=0)
jahr_textbox_1.set(selected_year)

# PARLEMENT PART
jahr_list = ["2019","2015","2011","2007","2003","1999","1995","1991","1987","1983","1979","1975","1971"]

# MAP PART

# Type map
type_map_label = tk.CTkLabel(pageMain, text="\tType de carte:",bg_color="white")
type_map_label.grid(row=14, column=1, padx=0, pady=0)

type_map_combobox = tk.CTkComboBox(pageMain, values=type_map_list, state="readonly", command=lambda value: mapConfig())
type_map_combobox.grid(row=14, column=2, padx=0, pady=0)
type_map_combobox.set(selected_map_mod)

# Gender dropdown
gender_map_label = tk.CTkLabel(pageMain, text="Genre:",bg_color="white")
gender_map_label.grid(row=15, column=1, padx=0, pady=0)

gender_map_combobox = tk.CTkComboBox(pageMain, values=gender_list, state="readonly",bg_color="white", command=lambda value: mapCallback())
gender_map_combobox.grid(row=15, column=2, padx=0, pady=0)
gender_map_combobox.set(selected_map_gender)

gender_map_combobox.grid_remove()
gender_map_label.grid_remove()

# party dropdown
party_map_label = tk.CTkLabel(pageMain, text="Parti:",bg_color="white")
party_map_label.grid(row=15, column=1, padx=0, pady=0)

party_map_combobox = tk.CTkComboBox(pageMain, values=party_list, state="readonly", command=lambda value: mapCallback())
party_map_combobox.grid(row=15, column=2, padx=0, pady=0)
party_map_combobox.set(selected_parti)

updatePlotTime(selected_party)
displayAll()

pageIntro = tk.CTkFrame(window,windos_w,windos_h)

window.title("Interactive Circles with Label")
# Number of rows and columns in the grid
rows, columns = 2, 4

#creat a image list for the save
image_map={}
image_trans_map={}
button_map = {}
label_map = {}

# Calculate the spacing between circles
circle_spacing_x = windos_w / columns

circle_spacing_y = windos_h / rows

radius = int(min(circle_spacing_x, circle_spacing_y) / 3)

#titre
titre = tk.CTkLabel(pageIntro, text="Visualisation de l'impact d’événements historiques sur la répartition des sièges à l'assemblée fédérale suisse", font=("Helvetica", 35),state="disabled")
titre.place(x=int(windos_w/2)-850,y=70)

# Create circles in the grid, bind hover events, and add circle numbers as tags
for row in range(rows):
    for col in range(columns):
        x = (col + 0.5) * circle_spacing_x
        if row == 0 :
            y = (row + 0.6) * circle_spacing_y
        else :
            y = (row + 0.5) * circle_spacing_y
        circle_idx = 4*(row) + (col)
        button= create_circle_button_with_image(pageIntro, x, y, radius,images_path[circle_idx],events[circle_idx],circle_idx)
        button_map[circle_idx] = button
# Create a Label of circle
for row in range(rows):
    for col in range(columns):
        x = (col + 0.5) * circle_spacing_x
        if row == 0 :
            y = (row + 0.6) * circle_spacing_y
        else :
            y = (row + 0.5) * circle_spacing_y
        circle_idx = 4 * (row) + (col)
        explanation_label = tk.CTkLabel(pageIntro, text=events_descriptions[circle_idx], font=("Helvetica", 15),state="disabled")
        if col < 2:
            explanation_label.place(x=x + radius + 30, y=y+label_high[circle_idx])
            explanation_label.configure(justify="left")
        else:
            explanation_label.place(x=x - 30 - radius-label_weight[circle_idx], y=y+label_high[circle_idx])
            explanation_label.configure(justify="right")
        explanation_label.place_forget()
        label_map[circle_idx]=explanation_label

pageIntro.place(relx=0.5, rely=0.5,anchor=tk.CENTER)

window.protocol("WM_DELETE_WINDOW", _quit)
window.mainloop()