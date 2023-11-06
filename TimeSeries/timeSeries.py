from pyaxis import pyaxis
import numpy as np
import matplotlib.pyplot as plt

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

def plot_party(data_df,selected_party, canton):
    # Data filtering
    elect = data_df[(data_df['Partei'].isin(selected_party)) & (data_df['Ergebnisse'] == 'Gewählte') & (data_df['Kanton'] == canton) & (data_df['Geschlecht'] == "Geschlecht - Total")]
    elect_filtered = elect
    elect_filtered['DATA'] = np.where(~elect_filtered['DATA'].str.contains(r'\d'), '0', elect_filtered['DATA']) # Filter empty values
    elect_filtered['DATA'] = elect_filtered['DATA'].astype(int)
    pivot_data = elect_filtered.pivot(index='Jahr', columns='Partei', values='DATA')
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_data.plot(kind='line', ax=ax)
    ax.set_title("Nombre d'élus par année " + 'pour ' + canton)
    ax.set_ylabel("Nombre d'élus")
    ax.set_xlabel('Années')
    ax.legend(title="Elus")
    
    return fig

def plot_gender(data_df, canton):
    # Data filtering
    elect = data_df[(data_df['Partei'] == 'Parteien - Total') & (data_df['Ergebnisse'] == 'Gewählte') & (data_df['Kanton'] == canton)]
    elect_filtered = elect[elect['Geschlecht'].isin(['Mann', 'Frau'])]
    elect_filtered['DATA'] = np.where(~elect_filtered['DATA'].str.contains(r'\d'), '0', elect_filtered['DATA']) # Filter empty values
    elect_filtered['DATA'] = elect_filtered['DATA'].astype(int)
    pivot_data = elect_filtered.pivot(index='Jahr', columns='Geschlecht', values='DATA')
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_data.plot(kind='line', ax=ax)
    ax.set_title("Nombre d'élus par année " + 'pour ' +  canton)
    ax.set_ylabel("Nombre d'élus")
    ax.set_xlabel('Années')
    ax.legend(title="Elus")
    
    return fig