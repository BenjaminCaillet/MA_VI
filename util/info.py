
# Party order

left_order_french = ["PST","Sol.","AVF","POCH","PSA","PS","PES"]
center_order_french = ["PCS","PDC","PBD","AdI","PEV","Sép.","Autres"]
right_order_french = ["PVL","PLR","PL","UDC","MCR","Rép.","DS","UDF","PSL","Lega"]
left_right_order_french_party = left_order_french + center_order_french + right_order_french


# Party colors
# Source 1: <https://en.wikipedia.org/wiki/List_of_political_parties_in_Switzerland#Names_in_the_national_languages>
# Source 2: <https://www.bfs.admin.ch/asset/en/27285176> 
colors_from_french_party = {
    "PLR": "#0174DF",   # PLR - Parti Libéral Radical (PL + PRD) -> Note: PRD = PLR, en allemand "FDP" dans les deux cas
    "PDC": "#FE9A2E",   # PDC - Parti Démocrate Chrétien - Maintenant 'Le Centre'
    "PS": "#992222",   # PS/PSS - Parti Socialiste
    "UDC": "#088a4b",   # UDC - Union Démocratique du Centre
    "PL": "#0174DF",  # Parti libéral suisse
    "AdI": "#999999", # Alliance des indépendants - Fondé par Duttweiler (Migros)... pardon?
    "PEV": "#ffd735", # Parti évangeliste
    "PCS": "#088A85",  # Parti Chrétien Social (et non pas Parti Communiste Suisse)
    "PVL": "#9AFE2E",   # Parti Vert Libéral
    "PBD": "fed755", #"#FE9A2E",  # Parti Bourgois Démocrate - aujourd'hui Le Centre avec PDC
    "PST": "#FF0921", # Parti Suisse du travail
    "PSA": "#330000", # Partito socialista autonomo (TI) (1970 - 1988). depuis 1992 : membre du PS suisse.
    "POCH": "#FF0921",  # "Organisation progresssistes de Suisse" - Aujourd'hui SolédiaritéS, PST/POP et 'La Gauche'
    "PES": "#01DF01",   #  "Parti Ecologiste Suisse" -> Les Verts
    "AVF": "#009900",   # Alternative socialiste verte et groupements féministes (étiquette commune, 1975 - 2010), Gauche alternative.
    "Sol.": "#FF0921", # SolidaritéS
    "Rép.": "#999999",  # Parti républicain
    "DS": "#009940", # Démocrates suisses
    "UDF": "#222222", # Union Démocratique Suisse
    "PSL": "#330000",  # Parti Suisse de la Liberté (nom temporaire PA Parti Suisse automobilistes)
    "Lega": "#0B3861", # Lega - Ligue du Tessin
    "MCR": "#fee801", # "Mouvement Citoyens Romands", mais principalement MCG (Genève)
    "Sép.": "#999999", # Séparatistes - principalement jura bernois
    "Autres": "#444444"
}



#
# Official groups
#

#  <https://www.bfs.admin.ch/asset/en/27285176> 
# Groupements de partis utilisés par l'OFS pour les représentations graphiques des élections 1991-2023 :

# Groupes de partis

#     Petits partis de gauche : PST, Sol.
#     Verts : PES, AVF, POCH
#     PS
#     PVL
#     Petits partis du centre : AdI, PEV, PCS
#     PBD (pour les élus avant 2021)
#     PDC (pour les élus avant 2021)
#     Le Centre (PDC, PBD)
#     PLR/PL : PLR.Les Libéraux y.c. PLS
#     UDC
#     Petits partis de droite : DS, UDF, PSL, Lega, MCR, Rép.
#     Autres, Groupes épars

today_french_groups_from_french_party = {
    "PLR": "PLR",   # PLR - Parti Libéral Radical (PL + PRD) -> Note: PRD = PLR, en allemand "FDP" dans les deux cas
    "PDC": "Le Centre",   # PDC - Parti Démocrate Chrétien - Maintenant 'Le Centre'
    "PS": "PS",   # PS/PSS - Parti Socialiste
    "UDC": "UDC",   # UDC - Union Démocratique du Centre
    "PL": "PLR",  # Parti libéral suisse
    "AdI": "Divers Centre", # Alliance des indépendants - Fondé par Duttweiler (Migros)... pardon?
    "PEV": "Divers Centre", # Parti évangeliste
    "PCS": "Divers Centre",  # Parti Chrétien Social (et non pas Parti Communiste Suisse)
    "PVL": "Verts Libéraux",   # Parti Vert Libéral
    "PBD": "Le Centre", #"#FE9A2E",  # Parti Bourgois Démocrate - aujourd'hui Le Centre avec PDC
    "PST": "Divers Gauche", # Parti Suisse du travail
    "PSA": "PS", # Partito socialista autonomo (TI) (1970 - 1988). depuis 1992 : membre du PS suisse.
    "POCH": "Divers Gauche",  # "Organisation progresssistes de Suisse" - Aujourd'hui SolédiaritéS, PST/POP et 'La Gauche'
    "PES": "Les Verts",   #  "Parti Ecologiste Suisse" -> Les Verts
    "AVF": "Divers Gauche",   # Alternative socialiste verte et groupements féministes (étiquette commune, 1975 - 2010), Gauche alternative.
    "Sol.": "Divers Gauche", # SolidaritéS
    "Rép.": "Divers Droite",  # Parti républicain
    "DS": "Divers Droite", # Démocrates suisses
    "UDF": "Divers Droite", # Union Démocratique Suisse
    "PSL": "Divers Droite",  # Parti Suisse de la Liberté (nom temporaire PA Parti Suisse automobilistes)
    "Lega": "Divers Droite", # Lega - Ligue du Tessin
    "MCR": "Divers Droite", # "Mouvement Citoyens Romands", mais principalement MCG (Genève)
    "Sép.": "Autres", # Séparatistes - principalement jura bernois
    "Autres": "Autres"
}

group_colors_from_today_french_groups = {
    "PLR": "#0174DF",
    "UDC": "#088a4b",
    "PS": "#992244",
    "Les Verts": "#01DF01",
    "Verts Libéraux": "#94FE2E",
    "Le Centre": "#FE9A2E",
    "Divers Centre": "#FED755",
    "Divers Gauche": "#FF0921",
    "Divers Droite": "#0B3861",
    "Autres": "#777777"
}

german_to_french_party = {
    "Parteien - Total": "Partis - Total",
    "FDP": "PLR",
    "CVP": "PDC",
    "SP": "PS",
    "SVP": "UDC",
    "LPS": "PL",
    "LdU": "AdI",
    "EVP": "PEV",
    "CSP": "PCS",
    "GLP": "PVL",
    "BDP": "PBD",
    "PdA": "PST",
    "PSA": "PSA",
    "POCH": "POCH",
    "GPS": "PES",
    "FGA": "AVF",
    "Sol.": "Sol.",
    "Rep.": "Rép.",
    "SD": "DS",
    "EDU": "UDF",
    "FPS": "PSL",
    "Lega": "Lega",
    "MCR": "MCR",
    "Sep.": "Sép.",
    "Übrige": "Autres"
}

