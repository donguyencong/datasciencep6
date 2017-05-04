#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 09:32:41 2017

@author: congdonguyen
"""
"""
Download the file describing state-to-state migration flows in the USA from the US Census Bureau (you can download it by hand). the goal of the project is to perform the network analysis of the flows.

Load the data from the file into a Pandas dataframe.
Hint: pd.read_excel('State_to_State_Migrations_Table_2015.xls',header=0,index_col=0,skiprows=6,skip_footer=8,na_values='N/A3') does a good job,
but there will be irrelevant rows and columns in the table.
Select the rows and columns whose names are valid US state names.
 You can download a Pythonized list of state names (and symbols) here.
Restrict the list to 50 states and DC (no territories).
Replace missing values with 0.
Replace each value in the dataframe with true or False, depending on whether or not it is greater than the median flow. Unstack the resulting dataframe (you will get a multiindex), drop missing values, and convert the index of the resulting series into a list with .tolist(). You will get a list of 2601 or so significant flows.
Let each flow represent an edge of an undirected graph. Create an empty Graph and add the edges to it (the nodes will be added automatically.) Remove self loops.
Make your program answer the following questions:
Which 5 states have the highest betweenness centrality?
Which 5 states have the highest closeness centrality?
How many connected components does the network have?
How many communities are in the network, what states belong to each community, and what is the modularity of the community structure?
Extra credit: Save the resulting network into a GraphML file, load into Gephi, apply ForceAtlas2 layout, calculate modularity, color nodes by modularity class, display labels (state names), and save the file as a PDF image.
"""
import pandas as pd
import networkx as nx
import community

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia ',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
#Convert json to series
states = pd.Series(states)

#Load and align data
data = pd.read_excel('data.xls',header=0,index_col=0,skiprows=6,skip_footer=8,na_values='N/A3')
data = data[states.tolist()].loc[states].fillna(0)
data = data > data.median()

#Unstack data
data = data.unstack()

#Flows data
flows = data[data == True].index.tolist()

#Create graph
graph = nx.Graph()

#Add edges
graph.add_edges_from(flows)

#Remove self loop edges
graph.remove_edges_from(graph.selfloop_edges())

#Betweeness centrality
bc = pd.Series(nx.betweenness_centrality(graph))

#Best 5 betweeness centrality
bestBC = bc.sort_values(ascending=False)[:5]

#Closeness centrality
cc = pd.Series(nx.closeness_centrality(graph))

#Best 5 closeness centrality
bestCC = cc.sort_values(ascending=False)[:5]

# Connected components
connectedComponents = len(list(nx.connected_components(graph)))
# Community
comm = pd.Series(community.best_partition(graph))

#how many?
comms = comm.unique()

#States belong to which community?
comm1 = comm[comm == 0]
comm2 = comm[comm == 1]
comm3 = comm[comm == 2]

#Modularity
modularity = community.modularity(community.best_partition(graph), graph)

#Write graph
nx.write_graphml(graph, open('stateGraph.graphml', 'wb'))

print('California, Texas, Florida, North Carolina and Illinois have the highest betweeness centrality.')
print('North Carolina, California, Texas, Florida and Colorado have the highest closeness centrality.')
print('The graph has 1 connected component.')
print('There are ' + str(len(comms)) + ' communities in the network.')
print('States belongs to 1st community are: ' + ', '.join([i for i in comm1.index]) + '.')
print('States belongs to 2nd community are: ' + ', '.join([i for i in comm2.index]) + '.')
print('States belongs to 3rd community are: ' + ', '.join([i for i in comm3.index]) + '.')
print('The modularity of the community structure is ' + str(modularity) + '.')
