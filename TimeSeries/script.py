from pyaxis import pyaxis
import matplotlib.pyplot as plt
#import tkinter as tk
from tkinter import *
import customtkinter as tk
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Setting up theme of the app
customtkinter.set_appearance_mode("light")


partei_list = ["PLR","PDC","PS","UDC","PVL","PES"]

# Parse the dataset
fp = r"Dataset/Dataset.px"
px = pyaxis.parse(uri=fp, encoding='ANSI')
data_df = px['DATA']

french_to_german = {
    "Partis - Total": "Parteien - Total",
    "PLR": "FDP",
    "PDC": "CVP",
    "PS": "SP",
    "UDC": "SVP",
    "PL": "LPS",
    "AdI": "LdU",
    "PEV": "EVP",
    "PCS": "CSP",
    "PVL": "GLP",
    "PBD": "BDP",
    "PST": "PdA",
    "PSA": "PSA",
    "POCH": "POCH",
    "PES": "GPS",
    "AVF": "FGA",
    "Sol.": "Sol.",
    "Rép.": "Rep.",
    "DS": "SD",
    "UDF": "EDU",
    "PSL": "FPS",
    "Lega": "Lega",
    "MCR": "MCR",
    "Sép.": "Sep.",
    "Autres": "Übrige"
}

def plot_data(selected_partei, kanton):
    # Data filtering
    elect = data_df[(data_df['Partei'].isin(selected_partei)) & (data_df['Ergebnisse'] == 'Gewählte') & (data_df['Kanton'] == kanton) & (data_df['Geschlecht'] == "Geschlecht - Total")]
    #elect = data_df[(data_df['Partei'] == partei) & (data_df['Ergebnisse'] == 'Gewählte') & (data_df['Kanton'] == kanton) & (data_df['Geschlecht'] == "Geschlecht - Total")]
    elect_filtered = elect
    elect_filtered['DATA'] = np.where(~elect_filtered['DATA'].str.contains(r'\d'), '0', elect_filtered['DATA']) # Filter empty values
    elect_filtered['DATA'] = elect_filtered['DATA'].astype(int)
    pivot_data = elect_filtered.pivot(index='Jahr', columns='Partei', values='DATA')
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_data.plot(kind='line', ax=ax)
    ax.set_title('Elected Men and Women by Year ' + ' in ' + kanton)
    ax.set_ylabel('Number Elected')
    ax.set_xlabel('Year')
    ax.legend(title="Geschlecht")
    
    return fig

def updatePlot(selected_partei):
    
    translated_list = [french_to_german[partei] for partei in selected_partei]
    kanton = kanton_combobox.get()
    fig = plot_data(translated_list, kanton)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=4, column=0, columnspan=20)
    print(translated_list)
    canvas.draw()
    
def open_selection_popup():
    # Create a popup
    popup = tk.CTkToplevel(window)
    popup.title("Select partei")
    
    # Variables to store checkbox states
    vars_ = [tk.BooleanVar() for _ in partei_list]
    
    # Create checkboxes for each item
    checkboxes = []
    for i, item in enumerate(partei_list):
        cb = tk.CTkCheckBox(popup, text=item, variable=vars_[i])
        cb.pack(anchor="w", padx=10, pady=5)
        checkboxes.append(cb)

    # OK button to print selected partei and destroy popup
    def confirm_selection():
        selected_partei = [item for i, item in enumerate(partei_list) if vars_[i].get()]
        updatePlot(selected_partei)
        popup.destroy()
    
    ok_button = tk.CTkButton(popup, text="OK", command=confirm_selection)
    ok_button.pack(pady=10)
    
def _quit():
    window.quit()
    window.destroy()

# GUI setup
window = tk.CTk()
window.title("Partei and Kanton Selection")

# Button to open the popup
btn = tk.CTkButton(window, text="Select partei", command=open_selection_popup)
btn.grid(row=0, column=0, padx=0, pady=20)

# Partei dropdown
partei_label = tk.CTkLabel(window, text="Parti:")
partei_label.grid(row=1, column=0, padx=0, pady=20)
partei_combobox = tk.CTkComboBox(window, values=partei_list)
partei_combobox.grid(row=1, column=1, padx=0, pady=20)
partei_combobox.set("UDC")

selected_partei = partei_list

# Kanton dropdown
kanton_label = tk.CTkLabel(window, text="Canton:")
kanton_label.grid(row=2, column=0, padx=0, pady=20)
kanton_list = ["Schweiz","Zürich","Bern / Berne","Luzern","Uri","Schwyz","Obwalden","Nidwalden","Glarus","Zug","Fribourg / Freiburg","Solothurn","Basel-Stadt","Basel-Landschaft","Schaffhausen","Appenzell Ausserrhoden","Appenzell Innerrhoden","St. Gallen","Graubünden / Grigioni / Grischun","Aargau","Thurgau","Ticino","Vaud","Valais / Wallis","Neuchâtel","Genève","Jura"]
kanton_combobox = tk.CTkComboBox(window, values=kanton_list)
kanton_combobox.grid(row=2, column=1, padx=0, pady=20)
kanton_combobox.set("Schweiz")

# Plot button
plot_button = tk.CTkButton(window, text="Plot", command=updatePlot)
plot_button.grid(row=3, column=0, columnspan=2, pady=20)

updatePlot(partei_list)

window.protocol("WM_DELETE_WINDOW", _quit)
window.mainloop()