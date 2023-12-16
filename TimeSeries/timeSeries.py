from pyaxis import pyaxis
import numpy as np
import matplotlib.pyplot as plt

#from info import dictionary_canton_to_french, colors_from_french_party,german_to_french_party,french_to_german_party
from TimeSeries.info import dictionary_canton_to_french, colors_from_french_party,german_to_french_party,french_to_german_party

party_list = ["PLR","PDC","PS","UDC","PVL","PES"]

party_list_complet = [
    "PLR", "PDC", "PS", "UDC", "PL", "AdI", "PEV",
    "PCS", "PVL", "PBD", "PST", "PSA", "POCH", "PES", "AVF", "Sol.",
    "Rép.", "DS", "UDF", "PSL", "Lega", "MCR", "Sép.", "Autres"
]

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

french_to_german_gender = {
    "Frau": "Femme",
    "Mann": "Homme"
}

def plot_party(data_df,selected_party, canton, year):
    # Data filtering
    elect = data_df[(data_df['Partei'].isin(selected_party)) & (data_df['Ergebnisse'] == 'Gewählte') & (data_df['Kanton'] == canton) & (data_df['Geschlecht'] == "Geschlecht - Total")]
    elect_filtered = elect
    elect_filtered['DATA'] = np.where(~elect_filtered['DATA'].str.contains(r'\d'), '0', elect_filtered['DATA']) # Filter empty values
    elect_filtered['DATA'] = elect_filtered['DATA'].astype(int)
    elect_filtered['Jahr'] = elect_filtered['Jahr'].astype(int)
    party_convert = elect_filtered['Partei'].replace(german_to_french_party)
    color_party = party_convert.replace(colors_from_french_party)
    elect_filtered['Partei'] = party_convert
    pivot_data = elect_filtered.pivot(index='Jahr', columns='Partei', values='DATA')
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_data.plot(kind='line', ax=ax, color=color_party)
    ax.axvline(x=int(year), color='red', linestyle='--')
    ax.set_title("Nombre d'élus par année " + 'pour ' + dictionary_canton_to_french[canton])
    ax.set_ylabel("Nombre d'élus")
    ax.set_xlabel('Années')
    ax.legend(title="Elus")
    
    return fig

def plot_gender(data_df, canton,year):
    # Data filtering
    elect = data_df[(data_df['Partei'] == 'Parteien - Total') & (data_df['Ergebnisse'] == 'Gewählte') & (data_df['Kanton'] == canton)]
    elect_filtered = elect[elect['Geschlecht'].isin(['Mann', 'Frau'])]
    elect_filtered['DATA'] = np.where(~elect_filtered['DATA'].str.contains(r'\d'), '0', elect_filtered['DATA']) # Filter empty values
    gender_convert = elect_filtered['Geschlecht'].replace(french_to_german_gender)
    elect_filtered['Geschlecht'] = gender_convert
    elect_filtered['DATA'] = elect_filtered['DATA'].astype(int)
    elect_filtered['Jahr'] = elect_filtered['Jahr'].astype(int)
    pivot_data = elect_filtered.pivot(index='Jahr', columns='Geschlecht', values='DATA')
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_data.plot(kind='line',color = ["red","blue"], ax=ax)
    ax.axvline(x=int(year), color='red', linestyle='--')
    ax.set_title("Nombre d'élus par année " + 'pour ' +  dictionary_canton_to_french[canton])
    ax.set_ylabel("Nombre d'élus")
    ax.set_xlabel('Années')
    ax.legend(title="Elus")
    
    return fig