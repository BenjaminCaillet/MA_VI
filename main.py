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

switzerland = gc.creat_geoswitz('Dataset/Swiss.geojson')

def updatePlotTime(selected_party):
    
    translated_list = [french_to_german[party] for party in selected_party]
    canton = canton_combobox.get()
    year = jahr_textbox_1.get()
    
    if gender_combobox.get() == "Total" :
        figTime = plot_party(data_df,translated_list, canton)
    else :
        figTime = plot_gender(data_df, canton)
    figTime.set_size_inches(14,4)
    canvasTime = FigureCanvasTkAgg(figTime, master=window)
    canvas_widget_time = canvasTime.get_tk_widget()
    canvas_widget_time.grid(row=0, column=5, columnspan=20, rowspan=10)
    canvasTime.draw()

def updatePlotParlement(dateLow,dateHigh):
    #First plot
    jahr = dateLow
    
    figParlement_1 = plot_parliament(data_df, jahr, point_size=50)
    figParlement_1.set_size_inches(5,3)

    canvasParlement_1 = FigureCanvasTkAgg(figParlement_1, master=window)
    canvas_widget_parlement_1 = canvasParlement_1.get_tk_widget()
    canvas_widget_parlement_1.grid(row=3, column=13, columnspan=7,rowspan=20)
    canvasParlement_1.draw()
    
    #Second plot
    jahr = dateHigh
    figParlement_2 = plot_parliament(data_df, jahr, point_size=50, legend=True)
    figParlement_2.set_size_inches(5,3)

    canvasParlement_2 = FigureCanvasTkAgg(figParlement_2, master=window)
    canvas_widget_parlement_2 = canvasParlement_2.get_tk_widget()
    canvas_widget_parlement_2.grid(row=13, column=13, columnspan=7,rowspan=20)
    canvasParlement_2.draw()
    
def mapCallback():
    result = find_closest_dates(jahr_textbox_1.get(),jahr_list)
    dateHigh = result[0]
    dateLow = result[1]
    updatePlotMap(dateLow,dateHigh)

    
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
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=7, column=5, columnspan=9,rowspan=20)
    canvas.draw()
    
def open_selection_popup():
    # Create a popup
    popup = tk.CTkToplevel(window)
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
        
    return [str(closest1), str(closest2)]
    
def _quit():
    window.quit()
    window.destroy()
    
def displayAll():
    result = find_closest_dates(jahr_textbox_1.get(),jahr_list)
    dateHigh = result[0]
    dateLow = result[1]
    updatePlotParlement(dateLow,dateHigh)
    updatePlotMap(dateLow,dateHigh)

# GUI setup
window = tk.CTk()
window.after(0, lambda:window.state('zoomed'))
window.title("Sélection du parti et du canton")

canvas= tk.CTkCanvas(window,width=1920, height=1080, bg='white')
canvas.grid(row=0, column=0, columnspan=21,rowspan=25)

# PLOT PART

# Button to open the popup
btn = tk.CTkButton(window, text="Sélection des partis", command=open_selection_popup,bg_color="white")
btn.grid(row=1, column=4, padx=0, pady=0)

selected_party = party_list

# Canton dropdown
canton_label = tk.CTkLabel(window, text="Canton:",bg_color="white")
canton_label.grid(row=3, column=3, padx=0, pady=0)
canton_list = ["Schweiz","Zürich","Bern / Berne","Luzern","Uri","Schwyz","Obwalden","Nidwalden","Glarus","Zug","Fribourg / Freiburg","Solothurn","Basel-Stadt","Basel-Landschaft","Schaffhausen","Appenzell Ausserrhoden","Appenzell Innerrhoden","St. Gallen","Graubünden / Grigioni / Grischun","Aargau","Thurgau","Ticino","Vaud","Valais / Wallis","Neuchâtel","Genève","Jura"]
canton_combobox = tk.CTkComboBox(window, values=canton_list,state="readonly", command=lambda value: updatePlotTime(selected_party))
canton_combobox.grid(row=3, column=4, padx=0, pady=0)
canton_combobox.set("Schweiz")

# Gender dropdown
gender_label = tk.CTkLabel(window, text="Genre:",bg_color="white")
gender_label.grid(row=4, column=3, padx=0, pady=0)
gender_combobox = tk.CTkComboBox(window, values=["Total","Homme/Femme"],state="readonly", command=lambda value: updatePlotTime(selected_party))
gender_combobox.grid(row=4, column=4, padx=0, pady=0)
gender_combobox.set("Total")

every_year = ["2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998", "1997", "1996", "1995", "1994", "1993", "1992", "1991", "1990", "1989", "1988", "1987", "1986", "1985", "1984", "1983", "1982", "1981", "1980", "1979", "1978", "1977", "1976", "1975", "1974", "1973", "1972", "1971"]

# Jahr dropdown
jahr_label_1 = tk.CTkLabel(window, text="Année:",bg_color="white")
jahr_label_1.grid(row=5, column=3, padx=0, pady=0)
jahr_textbox_1 = tk.CTkComboBox(window, values=every_year, command=lambda value:  displayAll())
jahr_textbox_1.grid(row=5, column=4, padx=0, pady=0)
jahr_textbox_1.set("2010")

# PARLEMENT PART
jahr_list = ["2019","2015","2011","2007","2003","1999","1995","1991","1987","1983","1979","1975","1971"]

# MAP PART

# Type map
type_map_label = tk.CTkLabel(window, text="Type de carte:",bg_color="white")
type_map_label.grid(row=11, column=3, padx=0, pady=0)

type_map_combobox = tk.CTkComboBox(window, values=type_map_list, state="readonly", command=lambda value: mapCallback())
type_map_combobox.grid(row=11, column=4, padx=0, pady=0)
type_map_combobox.set("Meilleur parti")

# party dropdown
party_map_label = tk.CTkLabel(window, text="Parti:",bg_color="white")
party_map_label.grid(row=12, column=3, padx=0, pady=0)

party_map_combobox = tk.CTkComboBox(window, values=party_list, state="readonly", command=lambda value: mapCallback())
party_map_combobox.grid(row=12, column=4, padx=0, pady=0)
party_map_combobox.set("PS")

# Gender dropdown
gender_map_label = tk.CTkLabel(window, text="Genre:",bg_color="white")
gender_map_label.grid(row=13, column=3, padx=0, pady=0)

gender_map_combobox = tk.CTkComboBox(window, values=gender_list, state="readonly",bg_color="white", command=lambda value: mapCallback())
gender_map_combobox.grid(row=13, column=4, padx=0, pady=0)
gender_map_combobox.set("Homme")

updatePlotTime(selected_party)
displayAll()

#window.rowconfigure(0, mize=30)
#window.rowconfigure(1, minsize=30)
#window.rowconfigure(14, minsize=30)

#window.columnconfigure(1, minsize=30)
#window.columnconfigure(4, minsize=30)
#window.columnconfigure(10, minsize=30)
#window.columnconfigure(13, minsize=30)

window.protocol("WM_DELETE_WINDOW", _quit)
window.mainloop()