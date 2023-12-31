
# GUI translate

# with array: [0=german, 1=french]

parlement_title_in_year = ["Bundesrat im", "Conseil National en"]



# Party name translation

party_french_to_german = {
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

party_german_to_french = {v: k for k, v in party_french_to_german.items()}

# Groups
#  <https://www.bfs.admin.ch/asset/en/27285176> 


group_french_to_german = {
    "PLR": "FDP",
    "UDC": "SVP",
    "PS": "SP",
    "Les Verts": "Grüne",
    "Verts Libéraux": "Grünliberale",
    "Le Centre": "Die Mitte",
    "Divers Centre": "Kleine Mitteparteien",
    "Divers Gauche": "Kleine Linksparteien",
    "Divers Droite": "Kleine Rechtsparteien",
    "Autres": "Übrige"
}

group_german_to_french = {v: k for k, v in group_french_to_german.items()}
