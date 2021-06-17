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

#create on df from the teams csv-s
path = r'/Scripts/world/Sofifa_teams'
all_files = glob.glob(os.path.join(path, "*.csv"))

df_from_each_file = (pd.read_csv(f) for f in all_files)
df   = pd.concat(df_from_each_file, ignore_index=True)

print(df)
# %%
#check leagues
print(df['League'].unique())
# %%
#define leagues to exclude
league_ex = [' Argentina Primera División \xa0(1)'
, ' Campeonato Brasileiro Série A (1)'
, ' Mexican Liga MX (1)'
,' Korean K League 1 (1)'
, ' USA Major League Soccer (1)'
, ' South African Premier Division (1)'
,' Campeonato Brasileiro Série B (2)'
, ' Australian Hyundai A-League (1)'
, ' Chilian Campeonato Nacional (1)'
,' Colombian Liga Postobón (1)'
,' Saudi Abdul L. Jameel League (1)'
,' Japanese J. League Division 1 (1)'
,' Argentinian Primera B Nacional (2)'
, ' Chinese Super League (1)'
, ' Paraguayan Primera División (1)'
,' Uruguayan Primera División (1)'
,' Ecuadorian Serie A (1)'
,' UAE Arabian Gulf League (1)'
,' Peruvian Primera División (1)'
,' Liga de Fútbol Profesional Boliviano (1)'
,' Venezuelan Primera División (1)'
,' International'
,' Italian Serie B (2)'
,' English League Championship (2)'
,' Spanish Segunda División (2)'
,' German 2. Bundesliga (2)'
,' French Ligue 2 (2)'
,' English League One (3)'
,' English League Two (4)'
,' Swiss Challenge League (2)'
,' Scottish League Two (4)'
,' German 3. Bundesliga (3)'
,' Polish I liga (2)'
,' Scottish League One (3)'
,' Scottish Championship (2)']

print(league_ex)
# %%
#exclude leages
df = df[~df.League.isin(league_ex)]
print(df)
print(df['League'].unique())
# %%
#delete duplicates
df.drop_duplicates()
print(df)
#%%
#check number of teams in the leagues
teams_ex = df[['Name', 'League']].groupby('League').nunique().sort_values('Name', ascending = True)
print(teams_ex)
# %%
#delete leagues with just a few teams
league_ex = [' Croatian Prva HNL (1)'
, ' Finnish Veikkausliiga (1)'
, '  Greek Super League (1)'
]
df = df[~df.League.isin(league_ex)]
print(df)
# %%
#save to excel
df.to_excel('/Scripts/world/teams_to_use.xlsx', encoding = 'UTF-8')
# %%
