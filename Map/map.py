import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from pyaxis import pyaxis
import pandas as pd
dictionary_canton_to_french = {
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
    #download the map
    switzerland = gpd.read_file(path)
    #delete useless coloumn
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
    #change the value of the name canton in french
    switzerland['NAME']=transormation_vo_French(switzerland['NAME'])
    return switzerland
def fusion_data_map(switzerland,data_frame):
    #fusion of map and value to see
    data_subset = data_frame[['Kanton', 'DATA']]
    data_subset.columns = ['NAME', 'DATA']
    switzerland = switzerland.merge(data_subset, on='NAME', how='left')

    return switzerland
def transormation_vo_French(data):
    #transformation of french name canton
    data=data.replace(dictionary_canton_to_french)
    return data
def plot_num(switzerland,mode=0):
    #Change the data type
    switzerland['DATA'] = switzerland['DATA'].astype(int)
    #define the size of plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    # Create a custom colormap with just two colors: red and blue
    cmap_colors = ['#FF0000', '#0000FF']
    custom_cmap = LinearSegmentedColormap.from_list('CustomRedToBlue', cmap_colors, N=256)
    #plot the map whit color blue to red
    if mode == 0:
        switzerland.plot(column='DATA', cmap=custom_cmap,ax=ax, legend=True)
    if mode == 1:
        switzerland.plot(column='DATA', cmap="RdBu", ax=ax, legend=True)
    #add a limite of canton
    switzerland.boundary.plot(ax=ax, color='black', linewidth=0.5)
    # add legend
    plt.axis('off')
    plt.title('Carte de la Suisse')
    plt.show()

def plot_obj(switzerland):
    # define the size of plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    # plot the map
    switzerland.plot(column='DATA', cmap="viridis", legend=True)
    # add a limite of canton
    switzerland.boundary.plot(ax=ax, color='black', linewidth=0.5)
    # add legend
    plt.title('Carte de la Suisse')
    plt.axis('off')
    plt.show()
