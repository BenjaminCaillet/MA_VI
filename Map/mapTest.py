import geopandas as gpd
import matplotlib.pyplot as plt
from pyaxis import pyaxis
import pandas as pd
import map as gc
#set file path (or URL)
fp = "Dataset/Dataset.px"
#parse contents of *.px file
px = pyaxis.parse(uri = fp , encoding = 'ANSI')

#store data as pandas dataframe
data_df = px['DATA']
data_df=pd.DataFrame(data_df)
masck_df_2019=data_df["Jahr"]=="2019"
data_df_2019=data_df[masck_df_2019].drop(columns="Jahr")
subset = data_df_2019[(data_df_2019['Ergebnisse'] == 'Kandidaturen') & (data_df_2019['Partei'] == 'Parteien - Total')&(data_df_2019['Geschlecht'] == 'Geschlecht - Total')]
subset["Kanton"]=gc.transormaton_VO_French(subset["Kanton"])
print(subset)
# Chargez les données géospatiales de la Suisse à partir d'un fichier (remplacez 'suisse.shp' par le chemin de votre fichier)
switzerland = gc.creat_geoswitz('Dataset/Swiss.geojson')
switzerland = gc.fussion_data_carte(switzerland,subset)
# Affichez la carte de la Suisse
gc.plot_num(switzerland)
