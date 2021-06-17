#Delete the records from the players df with the unwanted teams

#%%
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

df_players = pd.read_excel('/Scripts/world/df.xlsx')
print(df_players)
df_teams = pd.read_excel('/Scripts/world/teams_to_use.xlsx')
df_teams = df_teams[['Name', 'League']]
print(df_teams)

#%%
#define teams of the players df
player_teams = df_players['Team'].unique()
player_teams = pd.Series(player_teams)
print(list(player_teams))

#%%
#define teams included in the teams df also
searchfor = df_teams['Name']
found = player_teams[player_teams.str.contains('|'.join(searchfor))]

print(found)
# %%
#save found teams to excel
found.to_excel('/Scripts/world/teams_to_use_2.xlsx', encoding = 'UTF-8')
# %%
#excluded the records with not found teams
df_final= df_players[df_players.Team.isin(found)]
print(df_final)
# %%
#save player df to excel
df_final.to_excel('/Scripts/world/df_final.xlsx', encoding = 'UTF-8')
# %%
