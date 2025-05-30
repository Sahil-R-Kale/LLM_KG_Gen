EXTRACTION_PROMPT = """You are an expert Information Extraction Agent specializing in transforming unstructured text into structured knowledge representations.

Objective: First, identify all entities and relations in the text. Then, analyze the provided text to extract factual relational triples in the format: ["Subject", "Relation", "Object"]

Guidelines:
1. Detect and list all significant entities mentioned in the text.
2. For each pair of identified entities, determine the most accurate and contextually appropriate relationship.
3. Ensure that all entities and relations conform to standard ontology formats commonly used in knowledge graphs.
4. Approach the extraction methodically, validating the accuracy of each triple.
5. Present the final list of validated triples in a JSON array format, without commentary.

Example 1:
Text: The location of Trane is Swords, Dublin.
Candidate entities: ['Trane', 'Swords,_Dublin']
Triplets: [['Trane', 'location', 'Swords,_Dublin']]

Example 2:
Text: The Ciudad Ayala city, a part of Morelos with population density and population of 1604.0 and 1,777,539 respectively, has a UTC offset of -6. The government type of Ciudad Ayala is council-manager government and City Manager is one of the leaders.
Candidate entities: ['Ciudad_Ayala', '1604.0', '−6', '"City Manager"', 'City', '1777539', 'Morelos', 'Council-manager_government']
Triplets: [['Ciudad_Ayala', 'populationMetro', '1777539'], ['Ciudad_Ayala', 'leaderTitle', '"City Manager"'], ['Ciudad_Ayala', 'type', 'City'], ['Ciudad_Ayala', 'populationDensity', '1604.0'], ['Ciudad_Ayala', 'governmentType', 'Council-manager_government'], ['Ciudad_Ayala', 'utcOffset', '−6'], ['Ciudad_Ayala', 'isPartOf', 'Morelos']]

Example 3:
Text: The 17068.8 millimeter long ALCO RS-3 has a diesel-electric transmission.
Candidate entities: ['Diesel-electric_transmission', 'ALCO_RS-3', '17068.8 (millimetres)']
Triplets: [['ALCO_RS-3', 'powerType', 'Diesel-electric_transmission'], ['ALCO_RS-3', 'length', '17068.8 (millimetres)']]

Example 4:
Text: Alan B. Miller Hall, in Virginia, USA, was designed by Robert A.M. Stern. The address of the hall is "101 Ukrop Way" and the current tenants are the Mason School of Business.
Candidate entities: ['Alan_B._Miller_Hall', '"101 Ukrop Way"', 'United_States', 'Mason_School_of_Business', 'Robert_A._M._Stern', 'Virginia']
Triplets: [['Alan_B._Miller_Hall', 'architect', 'Robert_A._M._Stern'], ['Alan_B._Miller_Hall', 'address', '"101 Ukrop Way"'], ['Alan_B._Miller_Hall', 'currentTenants', 'Mason_School_of_Business'], ['Alan_B._Miller_Hall', 'location', 'Virginia'], ['Mason_School_of_Business', 'country', 'United_States']]

Example 5:
Text: Liselotte Grschebina was born in Karlsruhe and died in Israel. Ethnic groups in Israel include Arabs.
Candidate entities: ['Karlsruhe', 'Israel', 'Arab_citizens_of_Israel', 'Liselotte_Grschebina']
Triplets: [['Liselotte_Grschebina', 'birthPlace', 'Karlsruhe'], ['Liselotte_Grschebina', 'deathPlace', 'Israel'], ['Israel', 'ethnicGroup', 'Arab_citizens_of_Israel']]

Example 6:
Text: Agremiação Sportiva Arapiraquense managed by Vica has 17000 members and play in the Campeonato Brasileiro Série C league which is from Brazil.
Candidate entities: ['Vica', 'Agremiação_Sportiva_Arapiraquense', 'Brazil', 'Campeonato_Brasileiro_Série_C', '17000']
Triplets: [['Agremiação_Sportiva_Arapiraquense', 'league', 'Campeonato_Brasileiro_Série_C'], ['Campeonato_Brasileiro_Série_C', 'country', 'Brazil'], ['Agremiação_Sportiva_Arapiraquense', 'numberOfMembers', '17000'], ['Agremiação_Sportiva_Arapiraquense', 'manager', 'Vica']]

Input Text:
{input_text}

{format_instructions}
"""