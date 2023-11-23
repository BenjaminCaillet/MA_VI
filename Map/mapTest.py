import customtkinter as tk
import matplotlib.pyplot as plt
from pyaxis import pyaxis
import pandas as pd
import map as gc
from util.info import french_to_german, party_list_complet, party_list
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

fig=gc.plot_best_party(data_df,"2019")

plt.show()








"""
--------------------------------------------------------------
* changer les couleur et les nom des party
* créé un mimi-interface de choix
*chercher les event et décscription
--------------------------------------------------------------
"""



