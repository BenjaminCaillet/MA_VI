import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from pyaxis import pyaxis
import pandas as pd
dictionnaire_canton_vo_to_french = {
    'Schweiz':'Suisse',
    'Graubünden': 'Grisons',
    'Graubünden / Grigioni / Grischun': 'Grisons',
    'Bern': 'Berne',
    'Bern / Berne':'Berne',
    'Valais': 'Valais',
    'Valais / Wallis': 'Valais',
    'Waadt':'Vaud',
    'Ticino':'Tessin',
    'St. Gallen':'Saint-Gall',
    'Zürich':'Zurich',
    'Fribourg':'Fribourg',
    'Fribourg / Freiburg': 'Fribourg',
    'Luzern':'Lucerne',
    'Aargau':'Argovie',
    'Uri':'Uri',
    'Thurgau':'Thurgovie',
    'Schwyz':'Schwyz',
    'Jura':'Jura',
    'Neuchâtel':'Neuchâtel',
    'Solothurn':'Soleure',
    'Glarus':'Glaris',
    'Basel-Landschaft':'Bâle-Campagne',
    'Obwalden':'Obwald',
    'Nidwalden':'Nidwald',
    'Genčve':'Genève',
    'Schaffhausen':'Schaffhouse',
    'Appenzell Ausserrhoden':'Appenzell Rhodes-Extérieures',
    'Zug':'Zoug',
    'Appenzell Innerrhoden':'Appenzell Rhodes-Intérieures',
    'Basel-Stadt':' Bâle-Ville'
}
def creat_geoswitz(path):
    switzerland = gpd.read_file(path)
    switzerland = switzerland.drop(["DATUM_ERST",
                                    "DATUM_AEND",
                                    "EINWOHNERZ",
                                    "ERSTELL_J",
                                    "ERSTELL_M",
                                    "GRUND_AEND",
                                    "HERKUNFT",
                                    "ICC",
                                    "KANTONSFLA",
                                    "KANTONSNUM",
                                    "KT_TEIL",
                                    "REVISION_J",
                                    "REVISION_M",
                                    "REVISION_Q",
                                    "SEE_FLAECH",
                                    "HERKUNFT_J",
                                    "HERKUNFT_M"], axis=1)
    switzerland['NAME']=transormaton_VO_French(switzerland['NAME'])
    return switzerland
def fussion_data_carte(switzerland,data_frame):
    data_subset = data_frame[['Kanton', 'DATA']]
    data_subset.columns = ['NAME', 'DATA']
    switzerland = switzerland.merge(data_subset, on='NAME', how='left')

    return switzerland
def transormaton_VO_French(data):
    data=data.replace(dictionnaire_canton_vo_to_french)
    return data
def plot_num(switzerland):
    switzerland['DATA'] = switzerland['DATA'].astype(int)
    switzerland.plot(column='DATA', cmap="viridis", legend=True)
    # Ajoutez une légende
    plt.axis('off')
    plt.title('Carte de la Suisse')
    plt.show()

def plot_obj(switzerland):
    switzerland.plot(column='DATA', cmap="viridis", legend=True)
    # Ajoutez une légende
    plt.title('Carte de la Suisse')
    plt.axis('off')
    plt.show()
