from pyaxis import pyaxis
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Parse the dataset
fp = r"Dataset.px"
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
window = tk.Tk()
window.title("Partei and Kanton Selection")

# Partei dropdown
partei_label = tk.Label(window, text="Parti:")
partei_label.grid(row=0, column=0, padx=0, pady=20)
partei_list = ["Partis - Total","PLR","PDC","PS","UDC","PL","AdI","PEV","PCS","PVL","PBD","PT","PSA","POCH","PES","AVF","Sol.","Rép.","DS","UDF","PSL","Lega","MCR","Sép.","Autres"]
partei_combobox = ttk.Combobox(window, values=partei_list)
partei_combobox.grid(row=0, column=1, padx=0, pady=20)
partei_combobox.set("UDC")

# Kanton dropdown
kanton_label = tk.Label(window, text="Canton:")
kanton_label.grid(row=1, column=0, padx=0, pady=20)
kanton_list = ["Schweiz","Zürich","Bern / Berne","Luzern","Uri","Schwyz","Obwalden","Nidwalden","Glarus","Zug","Fribourg / Freiburg","Solothurn","Basel-Stadt","Basel-Landschaft","Schaffhausen","Appenzell Ausserrhoden","Appenzell Innerrhoden","St. Gallen","Graubünden / Grigioni / Grischun","Aargau","Thurgau","Ticino","Vaud","Valais / Wallis","Neuchâtel","Genève","Jura"]
kanton_combobox = ttk.Combobox(window, values=kanton_list)
kanton_combobox.grid(row=1, column=1, padx=0, pady=20)
kanton_combobox.set("Schweiz")

# Plot button
plot_button = tk.Button(window, text="Plot", command=on_button_click)
plot_button.grid(row=2, column=0, columnspan=2, pady=20)

partei_fr = partei_combobox.get()
partei = french_to_german[partei_fr]
kanton = kanton_combobox.get()
    
fig = plot_data(partei, kanton)

canvas = FigureCanvasTkAgg(fig, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=3, column=0, columnspan=20)
canvas.draw()

window.protocol("WM_DELETE_WINDOW", _quit)
window.mainloop()