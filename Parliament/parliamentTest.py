from pyaxis import pyaxis
import numpy as np
import matplotlib.pyplot as plt
import customtkinter as tk
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from parliament import plot_parliament, party_colors_dict, french_to_german

import os.path

# Setting up theme of the app
customtkinter.set_appearance_mode("light")

# Parse the dataset
# fp = r"Dataset/Dataset.px"
# px = pyaxis.parse(uri=fp, encoding='ANSI')
# data_df = px['DATA']

# Parse the dataset
dossier_script = os.path.dirname(__file__) # TODO: Fix - without os.path
fp = os.path.join(dossier_script, r"../Dataset/Dataset.px")
print(fp)
px = pyaxis.parse(uri=fp, encoding='ANSI')
data_df = px['DATA']

def updatePlot():
    
    #translated_list = [french_to_german[partei] for partei in selected_jahr]
    jahr_list = ["2019","2015","2011","2007","2003","1999","1995","1991","1987","1983","1979","1975","1971"]
    jahr = jahr_combobox.get()
    fig = plot_parliament(data_df, jahr_list, jahr)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=4, column=0, columnspan=20)
    print(jahr_list)
    canvas.draw()
    
    
def _quit():
    window.quit()
    window.destroy()

# GUI setup
window = tk.CTk()
window.title("Jahr Selection")


# Jahr dropdown
jahr_label = tk.CTkLabel(window, text="Année:")
jahr_label.grid(row=2, column=0, padx=0, pady=20)
jahr_list = ["2019","2015","2011","2007","2003","1999","1995","1991","1987","1983","1979","1975","1971"]
jahr_combobox = tk.CTkComboBox(window, values=jahr_list)
jahr_combobox.grid(row=2, column=1, padx=0, pady=20)
jahr_combobox.set("2019")

# Plot button
plot_button = tk.CTkButton(window, text="Plot", command=updatePlot)
plot_button.grid(row=3, column=0, columnspan=2, pady=20)

updatePlot()

window.protocol("WM_DELETE_WINDOW", _quit)
window.mainloop()