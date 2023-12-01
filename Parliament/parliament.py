from pyaxis import pyaxis
import matplotlib.pyplot as plt
#import tkinter as tk
from tkinter import *
import customtkinter as tk
import customtkinter

import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import poli_sci_kit

import sys
sys.path.append('.')
from util.info import colors_from_french_party, left_right_order_french_party
from util.translate import party_french_to_german

import os.path


# Setting up theme of the app
#customtkinter.set_appearance_mode("light")

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



def plot_parliament(data_df, jahr, point_size=100, legend=False):

    # seat_allocations = [20,10]
    # parties = ["one","two"]
    # party_colors = ["#ff00ff", "00ff00"]

    # Garder que l'année X
    df_jahr = data_df[data_df['Jahr'] == jahr]
    #print(df_jahr.head(6))

    elect = df_jahr[(df_jahr['Partei'] != "Parteien - Total") & (df_jahr['Ergebnisse'] == 'Gewählte') & (df_jahr['Kanton'] != "Schweiz")]
    elect_filtered = elect[elect['Geschlecht'].isin(['Mann', 'Frau'])]
    #elect_filtered = elect
    elect_filtered['DATA'] = np.where(~elect_filtered['DATA'].str.contains(r'\d'), '0', elect_filtered['DATA']) # Filter empty values
    elect_filtered['DATA'] = elect_filtered['DATA'].astype(int)
    
    # Combine by party
    df_sieges_par_parti = elect_filtered.groupby(['Partei'])['DATA'].sum().reset_index() 

    trad_german_to_french = {v: k for k, v in party_french_to_german.items()}

    df_sieges_par_parti["Partis"] =  df_sieges_par_parti["Partei"].map(trad_german_to_french)
    df_sieges_par_parti["Couleur"] = df_sieges_par_parti["Partis"].map(colors_from_french_party)

    #print("liste couleur:\n", df_sieges_par_canton_parti["Couleur"],df_sieges_par_canton_parti["Partis"])

    # Enlever les partis non élus
    df_sieges_par_parti = df_sieges_par_parti[df_sieges_par_parti['DATA'] != 0]

    # print("unsorted\n")
    # print(df_sieges_par_parti.head(7))
    # print("\nTEST\n")
    # print(left_right_order_french_party)
    # print(df_sieges_par_parti['Partis'])

    df_sieges_par_parti['Partis_cat'] = pd.Categorical(
            df_sieges_par_parti['Partis'], 
            categories=left_right_order_french_party, 
            ordered=True
        )
    df_sieges_par_parti.sort_values('Partis_cat',inplace=True)

    # print("sorted\n")
    # print(df_sieges_par_parti.head(7))
    # print(df_sieges_par_parti["Couleur"].tolist())

    fig, ax = plt.subplots(nrows=1,ncols=1)

    ax= poli_sci_kit.plot.parliament(
    allocations=df_sieges_par_parti["DATA"].tolist(),
    labels=df_sieges_par_parti["Partei"].tolist(),
    colors=df_sieges_par_parti["Couleur"].tolist(),
    style="semicircle",
    num_rows=7,  #8  # for ref: - 7 rows - https://www.parlament.ch/fr/organe/conseil-national/plan-sieges-cn
    marker_size=point_size,
    speaker=False
    )
    if legend :
        ax.legend(
        labels=df_sieges_par_parti["Partei"].tolist(),
        title="",
        title_fontsize=10,
        fontsize=8,
        ncol=7,
        loc='upper center',
        bbox_to_anchor=(0.5, 0.12),
        frameon=False,
        facecolor="#ffffff",
        framealpha=1,
        )
    
    ax.set_title("Parlement Suisse en "+ jahr)

    return fig
