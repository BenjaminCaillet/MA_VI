from pyaxis import pyaxis
import numpy as np
import matplotlib.pyplot as plt

partei_list = ["PLR","PDC","PS","UDC","PVL","PES"]

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

def plot_data(data_df,selected_partei, kanton):
    # Data filtering
    elect = data_df[(data_df['Partei'].isin(selected_partei)) & (data_df['Ergebnisse'] == 'Gewählte') & (data_df['Kanton'] == kanton) & (data_df['Geschlecht'] == "Geschlecht - Total")]
    elect_filtered = elect
    elect_filtered['DATA'] = np.where(~elect_filtered['DATA'].str.contains(r'\d'), '0', elect_filtered['DATA']) # Filter empty values
    elect_filtered['DATA'] = elect_filtered['DATA'].astype(int)
    pivot_data = elect_filtered.pivot(index='Jahr', columns='Partei', values='DATA')
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_data.plot(kind='line', ax=ax)
    ax.set_title('Elected Men and Women by Year ' + ' in ' + kanton)
    ax.set_ylabel('Number Elected')
    ax.set_xlabel('Year')
    ax.legend(title="Geschlecht")
    
    return fig