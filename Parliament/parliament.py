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
# Source: <https://en.wikipedia.org/wiki/List_of_political_parties_in_Switzerland#Names_in_the_national_languages>
# Source: <https://www.bfs.admin.ch/asset/en/27285176> 
# ANCIENNES LISTE - Utiliser info.py/colors_from_french_party
party_colors_dict = {
    "PLR": "#0022BB",   # PLR - Parti Libéral Radical (PL + PRD) -> Note: PRD = PLR, en allemand "FDP" dans les deux cas
    "PDC": "#888800",   # PDC - Parti Démocrate Chrétien - Maintenant 'Le Centre'
    "PS": "#992244",   # PS/PSS - Parti Socialiste
    "UDC": "#009900",   # UDC - Union Démocratique du Centre
    "PL": "#0022BB",  # Parti libéral suisse
    "AdI": "#999999", # Alliance des indépendants - Fondé par Duttweiler (Migros)... pardon?
    "PEV": "#666622", # Parti évangeliste
    "PCS": "#449922",  # Parti Chrétien Social (et non pas Parti Communiste Suisse)
    "PVL": "#229922",   # Parti Vert Libéral
    "PBD": "#aa3388",  # Parti Bourgois Démocrate - aujourd'hui Le Centre avec PDC
    "PST": "#999999", # Parti Suisse du travail
    "PSA": "#330000", # Partito socialista autonomo (TI) (1970 - 1988). depuis 1992 : membre du PS suisse.
    "POCH": "#999999",  # "Organisation progresssistes de Suisse" - Aujourd'hui SolédiaritéS, PST/POP et 'La Gauche'
    "PES": "#999999",   #  "Parti Ecologiste Suisse" -> Les Verts
    "AVF": "#009900",   # Alternative socialiste verte et groupements féministes (étiquette commune, 1975 - 2010), Gauche alternative.
    "Sol.": "#770000", # SolidaritéS
    "Rép.": "#999999",  # Parti républicain
    "DS": "#009900", # Démocrates suisses
    "UDF": "#222222", # Union Démocratique Suisse
    "PSL": "#330000",  # Parti Suisse de la Liberté (nom temporaire PA Parti Suisse automobilistes)
    "Lega": "#000044", # Lega - Ligue du Tessin
    "MCR": "#fee801", # "Mouvement Citoyens Romands", mais principalement MCG (Genève)
    "Sép.": "#999999", # Séparatistes - principalement jura bernois
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

