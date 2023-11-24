import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap, ListedColormap
import numpy as np
from matplotlib.ticker import MultipleLocator
from pyaxis import pyaxis
import pandas as pd

from info import dictionary_canton_to_french, colors_from_french_party,french_to_german_party


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
def fusion_data_map(switzerland,data_frame,mode=0):
    #fusion of map and value to see
    if mode == 0:
        data_subset = data_frame[['Kanton', 'DATA']]
        data_subset.columns = ['NAME', 'DATA']
    if mode == 1:
        data_subset = data_frame[['Kanton', 'Partei']]
        data_subset.columns = ['NAME', 'Partei']
    switzerland = switzerland.merge(data_subset, on='NAME', how='left')

    return switzerland
def transormation_vo_French(data):
    #transformation of french name canton
    data=data.replace(dictionary_canton_to_french)
    return data
def plot_num(switzerland,mode=0,title='Carte de la Suisse'):
    #Change the data type
    switzerland['DATA'] = switzerland['DATA'].astype(int)
    sorted_data = sorted(switzerland['DATA'])
    #define the size of plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    # normalistion legende
    vmin = switzerland['DATA'].min()
    vmax = switzerland['DATA'].max()
    if abs(vmin) > abs(vmax):
        vmax = abs(vmin)
    else:
        vmin = -vmax
    norm = TwoSlopeNorm(vmin=vmin - 0.5, vcenter=0, vmax=vmax + 0.5)

    # Create a custom colormap with just two colors: red and blue
    cmap_colors = ['#FF0000', '#FFFFFF', '#00FF00']
    custom_cmap = LinearSegmentedColormap.from_list('CustomRedToGreen', cmap_colors, N=(vmax - vmin) + 1)

    #plot the map whit color blue to red
    if mode == 0:
        sw=switzerland.plot(column='DATA', cmap=custom_cmap,ax=ax, legend=False,norm=norm)
    if mode == 1:
        sw=switzerland.plot(column='DATA', cmap="RdBu_r", ax=ax, legend=False,norm=norm)
    #add a limite of canton
    switzerland.boundary.plot(ax=ax, color='black', linewidth=0.5)
    # add legend
    plt.axis('off')
    plt.title(title)
    # Customize the colorbar ticks with integers
    ticks = np.arange(vmin, vmax + 1, 1)
    cbar = plt.colorbar(sw.get_children()[0], ax=ax, ticks=ticks, orientation='vertical')
    return fig

def plot_obj(switzerland,name_data="DATA",title='Carte de la Suisse'):
    # define the size of plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    # plot the map
    #switzerland.plot(column=name_data, ax=ax, cmap="viridis", legend=True)

    cmap = ListedColormap([colors_from_french_party[legend] for legend in switzerland["Partis"]])
    switzerland.plot(column=name_data,ax=ax, cmap=cmap, legend=True)

    unique_legends = list(set(switzerland["Partis"]))  # Supprimer les duplicatas
    legend_handles = []
    for legend in unique_legends:
        color = colors_from_french_party[legend]
        handle = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10)
        legend_handles.append((handle, legend))
    ax.legend(*zip(*legend_handles), title='Légendes', loc='upper right')

    # add a limite of canton
    switzerland.boundary.plot(ax=ax, color='black', linewidth=0.5)
    # add legend
    plt.title(title)
    plt.axis('off')
    return fig
def plot_nb_elu_party(dataset,party,year_old,year_new):
    mask_old = dataset["Jahr"] == year_old
    mask_new = dataset["Jahr"] == year_new
    dataset_old = dataset[mask_old].drop(columns="Jahr")
    dataset_new = dataset[mask_new].drop(columns="Jahr")
    subset_old = dataset_old[
        (dataset_old['Ergebnisse'] == 'Gewählte') &
        (dataset_old['Partei'] == party) &
        (dataset_old['Geschlecht'] == 'Geschlecht - Total')]
    subset_new = dataset_new[
        (dataset_new['Ergebnisse'] == 'Gewählte') &
        (dataset_new['Partei'] == party) &
        (dataset_new['Geschlecht'] == 'Geschlecht - Total')]

    data_old = pd.to_numeric(subset_old["DATA"], errors='coerce')
    data_old = data_old.fillna(0).astype(int)
    data_old=np.array(data_old)
    data_new = pd.to_numeric(subset_new["DATA"], errors='coerce')
    data_new= data_new.fillna(0).astype(int)
    data_new = np.array(data_new)
    data_com = data_new-data_old

    subset_com=pd.DataFrame(subset_old)

    subset_com["DATA"]=data_com
    subset_com["Kanton"] = transormation_vo_French(subset_com["Kanton"])
    switzerland = creat_geoswitz('mapSwiss.geojson')
    switzerland_data = fusion_data_map(switzerland, subset_com)

    trad_german_to_french = {v: k for k, v in french_to_german_party.items()}
    party=trad_german_to_french[party]
    name="Evolution du "+party+" entre "+year_old+" et "+year_new
    fig=plot_num(switzerland_data,0,name)
    return fig

def plot_diff_gender(dataset,gender,year_old,year_new):
    mask_old = dataset["Jahr"] == year_old
    mask_new = dataset["Jahr"] == year_new
    dataset_old = dataset[mask_old].drop(columns="Jahr")
    dataset_new = dataset[mask_new].drop(columns="Jahr")
    subset_old = dataset_old[
        (dataset_old['Ergebnisse'] == 'Gewählte') &
        (dataset_old['Partei'] == 'Parteien - Total') &
        (dataset_old['Geschlecht'] == gender)]
    subset_new = dataset_new[
        (dataset_new['Ergebnisse'] == 'Gewählte') &
        (dataset_new['Partei'] == 'Parteien - Total') &
        (dataset_new['Geschlecht'] == gender)]

    data_old = pd.to_numeric(subset_old["DATA"], errors='coerce')
    data_old = data_old.fillna(0).astype(int)
    data_old=np.array(data_old)
    data_new = pd.to_numeric(subset_new["DATA"], errors='coerce')
    data_new= data_new.fillna(0).astype(int)
    data_new = np.array(data_new)
    data_com = data_new-data_old

    subset_com=pd.DataFrame(subset_old)

    subset_com["DATA"]=data_com
    subset_com["Kanton"] = transormation_vo_French(subset_com["Kanton"])
    switzerland = creat_geoswitz('mapSwiss.geojson')
    switzerland_data = fusion_data_map(switzerland, subset_com)
    if gender == "Mann":
        n1="Evolution de la représentation masculine"
    else:
        n1="Evolution de la représentation femminine"
    name = n1 + " entre " + year_old + " et " + year_new
    fig=plot_num(switzerland_data,0,name)
    return fig
def plot_best_party(dataset,year):
    mask = dataset["Jahr"] == year
    dataset = dataset[mask].drop(columns="Jahr")
    subset = dataset[
        (dataset['Ergebnisse'] == 'Gewählte') &
        (dataset['Partei'] != 'Parteien - Total') &
        (dataset['Kanton'] != 'Schweiz') &
        (dataset['Geschlecht'] == 'Geschlecht - Total')]



    grouped = subset.groupby('Kanton')
    mini_tables = [group for _, group in grouped]


    for i, mini_table in enumerate(mini_tables):
        data = pd.to_numeric(mini_table["DATA"], errors='coerce')
        data = data.fillna(0).astype(int)
        indice_max = data.idxmax()
        mini_tables[i] = mini_table.loc[indice_max]

    df_best_Partei_by_kanton=pd.DataFrame(mini_tables)

    df_best_Partei_by_kanton["Kanton"] = transormation_vo_French(df_best_Partei_by_kanton["Kanton"])

    switzerland = creat_geoswitz('mapSwiss.geojson')
    switzerland_data = fusion_data_map(switzerland, df_best_Partei_by_kanton,1)
    trad_german_to_french = {v: k for k, v in french_to_german_party.items()}
    switzerland_data["Partis"] = switzerland_data["Partei"].map(trad_german_to_french)
    switzerland_data["Couleur"] = switzerland_data["Partis"].map(colors_from_french_party)
    name =  "Meilleur partie par canton en " + year
    fig=plot_obj(switzerland_data,"Partis",name)
    return fig
