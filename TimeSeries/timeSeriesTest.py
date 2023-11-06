from pyaxis import pyaxis
import matplotlib.pyplot as plt
import customtkinter as tk
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from timeSeries import plot_party, plot_gender, party_list, party_list_complet, french_to_german

# Setting up theme of the app
customtkinter.set_appearance_mode("light")

# Parse the dataset
fp = r"Dataset/Dataset.px"
px = pyaxis.parse(uri=fp, encoding='ANSI')
data_df = px['DATA']

def updatePlot(selected_party):
    
    translated_list = [french_to_german[party] for party in selected_party]
    canton = canton_combobox.get()
    
    if gender_combobox.get() == "Total" :
        fig = plot_party(data_df,translated_list, canton)
    else :
        fig = plot_gender(data_df, canton)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=5, column=0, columnspan=20)
    print(translated_list)
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
        updatePlot(selected_party)
        popup.destroy()

    ok_button = tk.CTkButton(popup, text="OK", command=confirm_selection)
    ok_button.pack(after=container, anchor="center", pady=10)
    
def _quit():
    window.quit()
    window.destroy()

# GUI setup
window = tk.CTk()
window.title("Sélection du parti et du canton")

# Button to open the popup
btn = tk.CTkButton(window, text="Sélection des partis", command=open_selection_popup)
btn.grid(row=0, column=0, padx=0, pady=20)

selected_party = party_list

# Canton dropdown
canton_label = tk.CTkLabel(window, text="Canton:")
canton_label.grid(row=1, column=0, padx=0, pady=20)
canton_list = ["Schweiz","Zürich","Bern / Berne","Luzern","Uri","Schwyz","Obwalden","Nidwalden","Glarus","Zug","Fribourg / Freiburg","Solothurn","Basel-Stadt","Basel-Landschaft","Schaffhausen","Appenzell Ausserrhoden","Appenzell Innerrhoden","St. Gallen","Graubünden / Grigioni / Grischun","Aargau","Thurgau","Ticino","Vaud","Valais / Wallis","Neuchâtel","Genève","Jura"]
canton_combobox = tk.CTkComboBox(window, values=canton_list,state="readonly")
canton_combobox.grid(row=1, column=1, padx=0, pady=20)
canton_combobox.set("Schweiz")

# Gender dropdown
gender_label = tk.CTkLabel(window, text="Genre:")
gender_label.grid(row=2, column=0, padx=0, pady=20)
gender_list = ["Total","Homme/Femme"]
gender_combobox = tk.CTkComboBox(window, values=gender_list,state="readonly")
gender_combobox.grid(row=2, column=1, padx=0, pady=20)
gender_combobox.set("Total")



# Plot button
plot_button = tk.CTkButton(window, text="Plot", command=lambda: updatePlot(selected_party))
plot_button.grid(row=3, column=0, columnspan=2, pady=20)

updatePlot(selected_party)

window.protocol("WM_DELETE_WINDOW", _quit)
window.mainloop()


