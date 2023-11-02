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
    "PL": "#0022BB",
    "AdI": "#999999",
    "PEV": "#666622",
    "PCS": "#449922",
    "PVL": "#229922",
    "PBD": "#aa3388",
    "PST": "#999999",
    "PSA": "#009900",
    "POCH": "#999999",
    "PES": "#999999",
    "AVF": "#009900",
    "Sol.": "#770000",
    "Rép.": "#999999",
    "DS": "#009900",
    "UDF": "#222222",
    "PSL": "#999999",
    "Lega": "#000044",
    "MCR": "#999999",
    "Sép.": "#999999",
    "Autres": "#444444"
}

def plot_parliament(data_df, jahr_list, jahr):

    # seat_allocations = [20,10]
    # parties = ["one","two"]
    # party_colors = ["#ff00ff", "00ff00"]

    # Garder que l'année X
    df_jahr = data_df[data_df['Jahr'] == jahr]
    print(df_jahr.head(6))

    elect = df_jahr[(df_jahr['Partei'] != "Parteien - Total") & (df_jahr['Ergebnisse'] == 'Gewählte') & (df_jahr['Kanton'] != "Schweiz")]
    elect_filtered = elect[elect['Geschlecht'].isin(['Mann', 'Frau'])]
    #elect_filtered = elect
    elect_filtered['DATA'] = np.where(~elect_filtered['DATA'].str.contains(r'\d'), '0', elect_filtered['DATA']) # Filter empty values
    elect_filtered['DATA'] = elect_filtered['DATA'].astype(int)
    
    # Combine by party
    df_sieges_par_parti = elect_filtered.groupby(['Partei'])['DATA'].sum().reset_index() 
    # print(df_sieges_par_canton_parti.head(7))
    # print("somme", df_sieges_par_canton_parti['DATA'].sum())
    # print("liste partis:\n", df_sieges_par_canton_parti["Partei"])


    trad_german_to_french = {v: k for k, v in french_to_german.items()}

    df_sieges_par_parti["Partis"] =  df_sieges_par_parti["Partei"].map(trad_german_to_french)
    df_sieges_par_parti["Couleur"] = df_sieges_par_parti["Partis"].map(party_colors_dict)

    #print("liste couleur:\n", df_sieges_par_canton_parti["Couleur"],df_sieges_par_canton_parti["Partis"])

    # Enlever les partis non élus
    df_sieges_par_parti = df_sieges_par_parti[df_sieges_par_parti['DATA'] != 0]

    print(df_sieges_par_parti.head(7))
    print(df_sieges_par_parti["Couleur"].tolist())

    ax2 = poli_sci_kit.plot.parliament(
    allocations=df_sieges_par_parti["DATA"].tolist(),
    labels=df_sieges_par_parti["Partei"].tolist(),
    colors=df_sieges_par_parti["Couleur"].tolist(),
    style="semicircle",
    num_rows=8,
    marker_size=120,
    speaker=False
    )

    return ax2.figure

