from pyaxis import pyaxis
import matplotlib.pyplot as plt
#import tkinter as tk
from tkinter import *
import customtkinter as tk
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import poli_sci_kit

import os.path


# Setting up theme of the app
customtkinter.set_appearance_mode("light")

# Parse the dataset
dossier_script = os.path.dirname(__file__) # TODO: Fix - without os.path
fp = os.path.join(dossier_script, r"../Dataset/Dataset.px")
print(fp)

# fp = r"../MA_VI/Dataset/Dataset.px"

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
party_colors = ['#000000', '#ffed00', '#64a12d', '#be3075', '#eb001f', '#009ee0']

# Party colors
party_colors_dict = {
    "PLR": "#0022BB",
    "PDC": "#888800",
    "PS": "#992244",
    "UDC": "#009900",
    "PL": "#999999",
    "AdI": "#999999",
    "PEV": "#999999",
    "PCS": "#449922",
    "PVL": "#009900",
    "PBD": "#aa3388",
    "PST": "#999999",
    "PSA": "#009900",
    "POCH": "#999999",
    "PES": "#999999",
    "AVF": "#009900",
    "Sol.": "#999999",
    "Rép.": "#999999",
    "DS": "#009900",
    "UDF": "#999999",
    "PSL": "#999999",
    "Lega": "#009900",
    "MCR": "#999999",
    "Sép.": "#999999",
    "Autres": "#444444"
}

def plot_parliament(jahr):

    seat_allocations = [20,10]
    parties = ["one","two"]
    party_colors = ["#ff00ff", "00ff00"]

    # WIP

    # T5
    # print("T5:")
    # Garder que l'année 2019
    df_2019 = data_df[data_df['Jahr'] == '2019']
    print(df_2019.head(6))

    elect = df_2019[(df_2019['Partei'] != "Parteien - Total") & (df_2019['Ergebnisse'] == 'Gewählte') & (df_2019['Kanton'] != "Schweiz")]
    elect_filtered = elect[elect['Geschlecht'].isin(['Mann', 'Frau'])]
    #elect_filtered = elect
    elect_filtered['DATA'] = np.where(~elect_filtered['DATA'].str.contains(r'\d'), '0', elect_filtered['DATA']) # Filter empty values
    elect_filtered['DATA'] = elect_filtered['DATA'].astype(int)
    
    # print("elect:")
    # print(elect_filtered.head(7)) # at this stage: "Zürich  2019    FDP       Mann   Gewählte     3"
    
    # Combine by gender
    # print("combined gender:")
    #elect_allgender = elect_filtered.groupby('Geschlecht').sum() # ça fait l'inverse: Total Homme vs Femme au parlement, indépendamment du parti/kanton.
    #df_sieges_par_canton_parti = elect_filtered.groupby(['Kanton', 'Partei'])['DATA'].sum().reset_index() # On obtient "Aargau - FDP - 2" par ex, beacuoup de 0...
    df_sieges_par_canton_parti = elect_filtered.groupby(['Partei'])['DATA'].sum().reset_index() # On obtient "Aargau - FDP - 2" par ex, beacuoup de 0...
    # print(df_sieges_par_canton_parti.head(7))
    # print("somme", df_sieges_par_canton_parti['DATA'].sum())
    # print("liste partis:\n", df_sieges_par_canton_parti["Partei"])

    # Combined by canton

    #pivot_data = elect_filtered.pivot(index='Jahr', columns='Geschlecht', values='DATA')

    # WIP - End

    trad_german_to_french = {v: k for k, v in french_to_german.items()}

    df_sieges_par_canton_parti["Partis"] =  df_sieges_par_canton_parti["Partei"].map(trad_german_to_french)
    df_sieges_par_canton_parti["Couleur"] = df_sieges_par_canton_parti["Partis"].map(party_colors_dict)

    #print("liste couleur:\n", df_sieges_par_canton_parti["Couleur"],df_sieges_par_canton_parti["Partis"])

    

    # Enlever les partis non élus
    df_sieges_par_canton_parti = df_sieges_par_canton_parti[df_sieges_par_canton_parti['DATA'] != 0]

    print(df_sieges_par_canton_parti.head(7))
    print(df_sieges_par_canton_parti["Couleur"].tolist())

    ax2 = poli_sci_kit.plot.parliament(
    allocations=df_sieges_par_canton_parti["DATA"].tolist(),
    labels=df_sieges_par_canton_parti["Partei"].tolist(),
    colors=df_sieges_par_canton_parti["Couleur"].tolist(),
    style="semicircle",
    num_rows=8,
    marker_size=120,
    speaker=False
    )

    return ax2.figure

def plot_data(partei, kanton):
    # Data filtering
    elect = data_df[(data_df['Partei'] == partei) & (data_df['Ergebnisse'] == 'Gewählte') & (data_df['Kanton'] == kanton)]
    elect_filtered = elect[elect['Geschlecht'].isin(['Mann', 'Frau'])]
    elect_filtered = elect
    elect_filtered['DATA'] = np.where(~elect_filtered['DATA'].str.contains(r'\d'), '0', elect_filtered['DATA']) # Filter empty values
    elect_filtered['DATA'] = elect_filtered['DATA'].astype(int)
    pivot_data = elect_filtered.pivot(index='Jahr', columns='Geschlecht', values='DATA')
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_data.plot(kind='bar', ax=ax)
    ax.set_title('Elected Men and Women by Year for ' + partei + ' in ' + kanton)
    ax.set_ylabel('Number Elected')
    ax.set_xlabel('Year')
    ax.legend(title="Geschlecht")

    # plt.show()
    
    return fig 

def on_button_click():
    partei_fr = partei_combobox.get()
    partei = french_to_german[partei_fr]
    kanton = kanton_combobox.get()
    
    fig = plot_data(partei, kanton)
    
    # Embed the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=3, column=0, columnspan=20)
    canvas.draw()
    
def _quit():
    window.quit()
    window.destroy()

# GUI setup
window = tk.CTk()
window.title("Partei and Kanton Selection")

# Partei dropdown
partei_label = tk.CTkLabel(window, text="Parti:")
partei_label.grid(row=0, column=0, padx=0, pady=20)
partei_list = ["Partis - Total","PLR","PDC","PS","UDC","PL","AdI","PEV","PCS","PVL","PBD","PT","PSA","POCH","PES","AVF","Sol.","Rép.","DS","UDF","PSL","Lega","MCR","Sép.","Autres"]
partei_combobox = tk.CTkComboBox(window, values=partei_list)
partei_combobox.grid(row=0, column=1, padx=0, pady=20)
partei_combobox.set("UDC")

# Kanton dropdown
kanton_label = tk.CTkLabel(window, text="Canton:")
kanton_label.grid(row=1, column=0, padx=0, pady=20)
kanton_list = ["Schweiz","Zürich","Bern / Berne","Luzern","Uri","Schwyz","Obwalden","Nidwalden","Glarus","Zug","Fribourg / Freiburg","Solothurn","Basel-Stadt","Basel-Landschaft","Schaffhausen","Appenzell Ausserrhoden","Appenzell Innerrhoden","St. Gallen","Graubünden / Grigioni / Grischun","Aargau","Thurgau","Ticino","Vaud","Valais / Wallis","Neuchâtel","Genève","Jura"]
kanton_combobox = tk.CTkComboBox(window, values=kanton_list)
kanton_combobox.grid(row=1, column=1, padx=0, pady=20)
kanton_combobox.set("Schweiz")

# Plot button
plot_button = tk.CTkButton(window, text="Plot", command=on_button_click)
plot_button.grid(row=2, column=0, columnspan=2, pady=20)

partei_fr = partei_combobox.get()
partei = french_to_german[partei_fr]
kanton = kanton_combobox.get()
    
#fig = plot_data(partei, kanton)
fig = plot_parliament(2019)


canvas = FigureCanvasTkAgg(fig, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=3, column=0, columnspan=20)
canvas.draw()

window.protocol("WM_DELETE_WINDOW", _quit)
window.mainloop()