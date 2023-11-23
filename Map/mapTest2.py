import customtkinter as tk
from pyaxis import pyaxis
import pandas as pd
import map as gc
from info import french_to_german_party, party_list_complet, party_list,canton_list,type_map_list,gender_list,french_to_german_gender
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Setting up theme of the app
tk.set_appearance_mode("light")
#set file path (or URL)
fp = "Dataset/Dataset.px"
#parse contents of *.px file
px = pyaxis.parse(uri = fp , encoding = 'ANSI')

#store data as pandas dataframe
data_df = px['DATA']
data_df=pd.DataFrame(data_df)

def updatePlot():
    type =      type_combobox.get()
    party =     party_combobox.get()
    gender =    gender_combobox.get()
    if type == "Evolution_genre":
        gender_t=french_to_german_gender[gender]
        fig = gc.plot_diff_gender(data_df, gender_t, "2015", "2019")
    elif type == "Best_party":
        fig=gc.plot_best_party(data_df,"2019")
    else:
        party_t=french_to_german_party[party]
        fig=gc.plot_nb_elu_party(data_df, party_t, "2015", "2019")
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=5, column=0, columnspan=20)
    canvas.draw()
    
def _quit():
    window.quit()
    window.destroy()


# GUI setup
window = tk.CTk()
window.title("Sélection du parti et du canton")


# Type map
type_label = tk.CTkLabel(window, text="Type of map:")
type_label.grid(row=1, column=0, padx=0, pady=20)

type_combobox = tk.CTkComboBox(window, values=type_map_list, state="readonly")
type_combobox.grid(row=1, column=1, padx=0, pady=20)
type_combobox.set("Best_party")

# party dropdown
party_label = tk.CTkLabel(window, text="Canton:")
party_label.grid(row=2, column=0, padx=0, pady=20)

party_combobox = tk.CTkComboBox(window, values=party_list, state="readonly")
party_combobox.grid(row=2, column=1, padx=0, pady=20)
party_combobox.set("PS")


# Gender dropdown
gender_label = tk.CTkLabel(window, text="Genre:")
gender_label.grid(row=3, column=0, padx=0, pady=20)

gender_combobox = tk.CTkComboBox(window, values=gender_list, state="readonly")
gender_combobox.grid(row=3, column=1, padx=0, pady=20)
gender_combobox.set("Homme")

# Plot button
plot_button = tk.CTkButton(window, text="Plot", command=lambda: updatePlot())
plot_button.grid(row=3, column=5, columnspan=2, pady=20)

updatePlot()

window.protocol("WM_DELETE_WINDOW", _quit)
window.mainloop()










"""
--------------------------------------------------------------
* changer les couleur et les nom des party
* créé un mimi-interface de choix
*chercher les event et décscription
--------------------------------------------------------------
"""



