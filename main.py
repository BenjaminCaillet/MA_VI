from pyaxis import pyaxis
import matplotlib.pyplot as plt
import customtkinter as tk
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from TimeSeries.timeSeries import plot_party, plot_gender, party_list, party_list_complet, french_to_german
from Parliament.parliament import plot_parliament
from util.translate import party_french_to_german
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import Map.map as gc
from Map.info import french_to_german_party, party_list_complet, party_list,canton_list,type_map_list,gender_list,french_to_german_gender
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Setting up theme of the app
customtkinter.set_appearance_mode("light")

# Parse the dataset
fp = r"Dataset/Dataset.px"
px = pyaxis.parse(uri=fp, encoding='ANSI')
data_df = px['DATA']

def updatePlotTime(selected_party):
    
    translated_list = [french_to_german[party] for party in selected_party]
    canton = canton_combobox.get()
    
    if gender_combobox.get() == "Total" :
        figTime = plot_party(data_df,translated_list, canton)
    else :
        figTime = plot_gender(data_df, canton)
    figTime.set_size_inches(15,4)
    canvasTime = FigureCanvasTkAgg(figTime, master=window)
    canvas_widget_time = canvasTime.get_tk_widget()
    canvas_widget_time.grid(row=1, column=5, columnspan=15, rowspan=10)
    #print(translated_list)
    canvasTime.draw()

def updatePlotParlement():
    
    #First plot
    jahr_list = ["2019","2015","2011","2007","2003","1999","1995","1991","1987","1983","1979","1975","1971"]
    jahr = jahr_combobox_1.get()
    figParlement_1 = plot_parliament(data_df, jahr_list, jahr)
    figParlement_1.set_size_inches(5,2.5)

    canvasParlement_1 = FigureCanvasTkAgg(figParlement_1, master=window)
    canvas_widget_parlement_1 = canvasParlement_1.get_tk_widget()
    canvas_widget_parlement_1.grid(row=16, column=5, columnspan=5,rowspan=5)
    canvasParlement_1.draw()
    
    #Second plot
    jahr = jahr_combobox_2.get()
    figParlement_2 = plot_parliament(data_df, jahr_list, jahr)
    figParlement_2.set_size_inches(5,2.5)

    canvasParlement_2 = FigureCanvasTkAgg(figParlement_2, master=window)
    canvas_widget_parlement_2 = canvasParlement_2.get_tk_widget()
    canvas_widget_parlement_2.grid(row=21, column=5, columnspan=5,rowspan=5)
    canvasParlement_2.draw()
    
def updatePlotMap():
    type =      type_map_combobox.get()
    party =     party_map_combobox.get()
    gender =    gender_map_combobox.get()
    if type == "Evolution_genre":
        gender_t=french_to_german_gender[gender]
        fig = gc.plot_diff_gender(data_df, gender_t, "2015", "2019")
    elif type == "Best_party":
        fig=gc.plot_best_party(data_df,"2019")
    else:
        party_t=french_to_german_party[party]
        fig=gc.plot_nb_elu_party(data_df, party_t, "2015", "2019")
    fig.set_size_inches(7,4)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=16, column=14, columnspan=7,rowspan=8)
    canvas.draw()
    
def open_selection_popup():
    # Create a popup
    popup = tk.CTkToplevel(window)
    popup.title("Select Party")

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
    
def _quit():
    window.quit()
    window.destroy()

# GUI setup
window = tk.CTk()
window.after(0, lambda:window.state('zoomed'))
window.title("Sélection du parti et du canton")
window.configure()
window.configure(background='white')

# PLOT PART

# Button to open the popup
btn = tk.CTkButton(window, text="Sélection des partis", command=open_selection_popup)
btn.grid(row=2, column=3, padx=0, pady=20)

selected_party = party_list

# Canton dropdown
canton_label = tk.CTkLabel(window, text="Canton:")
canton_label.grid(row=4, column=2, padx=0, pady=20)
canton_list = ["Schweiz","Zürich","Bern / Berne","Luzern","Uri","Schwyz","Obwalden","Nidwalden","Glarus","Zug","Fribourg / Freiburg","Solothurn","Basel-Stadt","Basel-Landschaft","Schaffhausen","Appenzell Ausserrhoden","Appenzell Innerrhoden","St. Gallen","Graubünden / Grigioni / Grischun","Aargau","Thurgau","Ticino","Vaud","Valais / Wallis","Neuchâtel","Genève","Jura"]
canton_combobox = tk.CTkComboBox(window, values=canton_list,state="readonly")
canton_combobox.grid(row=4, column=3, padx=0, pady=20)
canton_combobox.set("Schweiz")

# Gender dropdown
gender_label = tk.CTkLabel(window, text="Genre:")
gender_label.grid(row=5, column=2, padx=0, pady=20)
gender_combobox = tk.CTkComboBox(window, values=["Total","Homme/Femme"],state="readonly")
gender_combobox.grid(row=5, column=3, padx=0, pady=20)
gender_combobox.set("Total")

# Plot button
plot_button = tk.CTkButton(window, text="Plot", command=lambda: updatePlotTime(selected_party))
plot_button.grid(row=6, column=3, columnspan=1, pady=20)

# PARLEMENT PART

jahr_list = ["2019","2015","2011","2007","2003","1999","1995","1991","1987","1983","1979","1975","1971"]

# Jahr dropdown
jahr_label_1 = tk.CTkLabel(window, text="Année:")
jahr_label_1.grid(row=16, column=2, padx=0, pady=20)
jahr_combobox_1 = tk.CTkComboBox(window, values=jahr_list)
jahr_combobox_1.grid(row=16, column=3, padx=0, pady=20)
jahr_combobox_1.set("2015")

jahr_label_2 = tk.CTkLabel(window, text="Année:")
jahr_label_2.grid(row=17, column=2, padx=0, pady=20)
jahr_combobox_2 = tk.CTkComboBox(window, values=jahr_list)
jahr_combobox_2.grid(row=17, column=3, padx=0, pady=20)
jahr_combobox_2.set("2019")

# Plot button
plot_button = tk.CTkButton(window, text="Plot", command=updatePlotParlement)
plot_button.grid(row=18, column=3, columnspan=1, pady=20)

# MAP PART

# Type map
type_map_label = tk.CTkLabel(window, text="Type of map:")
type_map_label.grid(row=16, column=11, padx=0, pady=20)

type_map_combobox = tk.CTkComboBox(window, values=type_map_list, state="readonly")
type_map_combobox.grid(row=16, column=12, padx=0, pady=20)
type_map_combobox.set("Best_party")

# party dropdown
party_map_label = tk.CTkLabel(window, text="Canton:")
party_map_label.grid(row=17, column=11, padx=0, pady=20)

party_map_combobox = tk.CTkComboBox(window, values=party_list, state="readonly")
party_map_combobox.grid(row=17, column=12, padx=0, pady=20)
party_map_combobox.set("PS")


# Gender dropdown
gender_map_label = tk.CTkLabel(window, text="Genre:")
gender_map_label.grid(row=18, column=11, padx=0, pady=20)

gender_map_combobox = tk.CTkComboBox(window, values=gender_list, state="readonly")
gender_map_combobox.grid(row=18, column=12, padx=0, pady=20)
gender_map_combobox.set("Homme")

# Plot button
plot_map_button = tk.CTkButton(window, text="Plot", command=lambda: updatePlotMap())
plot_map_button.grid(row=20, column=12, columnspan=2, pady=20)

updatePlotParlement()
updatePlotTime(selected_party)
updatePlotMap()

window.rowconfigure(0, minsize=30)
window.rowconfigure(1, minsize=30)
window.rowconfigure(14, minsize=30)

window.columnconfigure(1, minsize=30)
window.columnconfigure(4, minsize=30)
window.columnconfigure(10, minsize=30)
window.columnconfigure(13, minsize=30)

window.protocol("WM_DELETE_WINDOW", _quit)
window.mainloop()