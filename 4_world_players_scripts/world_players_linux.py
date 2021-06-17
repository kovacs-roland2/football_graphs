#%%
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import itertools
from networkx.algorithms import community
import operator
from itertools import islice
import glob
import os

#using players' values csv 
df = pd.read_excel('/home/kovacs/world/df.xlsx', engine='openpyxl')
print(df)
#%%
#check if there are players with the same name and birthdate
most_man = df[['ID', 'Age']].groupby('ID').nunique()
print(most_man.sort_values("ID", ascending = False))
#%%
#create df with the necessary columns only
players = df.groupby(['ID', 'Year', 'Team']).size().reset_index()
edge_list = []

#%%
#creating the edge list
num = 0

for i, r in players.iterrows():
    num += 1
    player_df = df[(df.Year == r['Year']) & (df.Team == r['Team'])]
    arr = np.array(player_df['ID'])

    for y in range(len(arr)):
        try:
            if r['ID'] != arr[y]:
                edge_list.append([r['ID'], arr[y]])
        except: 
            print('e')
            pass
    print(f'{num} / {len(players)} ready')


#%%
#create graph from the edge list
G = nx.Graph()
G.add_edges_from(edge_list)
print('Basic information about the graph:')
print(nx.info(G))

#%%
#players with the most and the fewest degrees
degrees = [(node, val) for (node, val) in G.degree()]
degree_table = pd.DataFrame(degrees, columns=['Team','Degree'])
degree_table.sort_values(by=['Degree'], inplace = True, ascending = False)
degree_table.reset_index(drop=True, inplace=True)
degree_table.index += 1
print('Players with the most connections:')
print(degree_table[:50])
print()
print('Players with the fewest connections:')
print(degree_table[-50:])

# %%
#degree distribution
degree = [G.degree(n) for n in G.nodes()]
degree = pd.DataFrame(degree)
plt.style.use("bmh")
fig, ax = plt.subplots(figsize = (7,4))
degree.plot(ax = ax, kind = 'hist', density = True, alpha = 0.65, bins = 15)
degree.plot(ax = ax, kind = 'kde')
ax.grid(False)
ax.set_xlabel('Number of degrees')
ax.set_xlim(0,850)
ax.set_ylabel('Frequency')
ax.set_yticks([])
ax.get_legend().remove()
ax.set_title('Degree distribution follows power-law', size = 15)

out_png = '/home/kovacs/world/out_file.png'
plt.savefig(out_png, dpi=150)


# %%
#Average shortest path length
spl = nx.average_shortest_path_length(G)
print("Average shortest path length:", spl)
# %%
#Network density
density = nx.density(G)
print("Network density:", density)

# %%
#Diameter
print("Diameter:", nx.diameter(G))
# %%
#Triadic closure / clustering coefficient
triadic_closure = nx.transitivity(G)
print("Triadic closure:", triadic_closure)
# %%
#eigenvectors
eigenvector_dict = nx.eigenvector_centrality(G)
eigenvector_table = pd.DataFrame(eigenvector_dict.items())
eigenvector_table.sort_values(by=[1], inplace = True, ascending = False)
eigenvector_table.reset_index(drop=True, inplace=True)
eigenvector_table.index += 1
print('The most important players according to the eigenvectors:')
print(eigenvector_table[:30])

# %%
#betweenness
betweenness_dict = nx.betweenness_centrality(G)
betweenness_table = pd.DataFrame(betweenness_dict.items())
betweenness_table.sort_values(by=[1], inplace = True, ascending = False)
betweenness_table.reset_index(drop=True, inplace=True)
betweenness_table.index += 1
print('The most important players according to betweenness:')
print(betweenness_table[:30])

#%%
#teammates
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def CountFrequency(my_list): 
  
    # Creating an empty dictionary  
    freq = {} 
    for item in my_list: 
        to_check = str([item[0], item[1]])
        if (to_check in freq):
            freq[to_check] += 1
        else:
            freq[to_check] = 1

    sorted_freq = dict( sorted(freq.items(), key=operator.itemgetter(1),reverse=True))
    n_items = take(200, sorted_freq.items())
    n_items = n_items[:100:2]
    n_items = pd.DataFrame(n_items, columns = ['Players', 'Weight'])
    n_items.reset_index(drop = True, inplace=True)
    n_items.index += 1
    print(n_items)

CountFrequency(edge_list)

# %%
#players at one club
print("Longest serving players at one club:")
print(df[['Name', 'Team']].value_counts()[:50])
# %%
#Players with the most clubs
print("Players with the most clubs:")
most_clubs = df[['Name', 'Team']].groupby("Name").nunique()
print(most_clubs.sort_values("Team",ascending = False)[:50])
# %%
#Players with the most clubs
print("Clubs with the most players:")
most_man = df[['Team', 'Name']].groupby('Team').nunique()
print(most_man.sort_values("Name", ascending = False)[:50])
# %%
