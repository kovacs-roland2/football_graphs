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

#create one df from the values csv-s
path = r'/PL_Players/Scripts/world/data'
all_files = glob.glob(os.path.join(path, "*.csv"))

df_from_each_file = (pd.read_csv(f) for f in all_files)
df   = pd.concat(df_from_each_file, ignore_index=True)
df['Age'] = df['Age'].apply(lambda x: x[:-5])
df['ID'] = df['Name'] + ' ' + df['Age']
#df = df[(df.Year == 2021) & (df.Team == 'Chelsea FC')]
print(df)

#%%
print(f"There are {len(df['Team'].unique())} different teams")

#%%
#define teams to exclude - included fewer than 5 seasons
teams_to_exlcude = df[['Team', 'Year']].groupby('Team').nunique().sort_values('Year', ascending = True)[:499]

to_exclude = teams_to_exlcude.index

#%%
#exclude teams
print(teams_to_exlcude)
df_new = df[~df.Team.isin(to_exclude)]
print(df_new)

print(f"There are {len(df_new['Team'].unique())} different teams")

#%%
#define teams to exclude with fewer players in a season than 20
teams_to_exclude = df_new[['Team', 'Year', 'Name']].groupby(['Team', 'Year']).nunique().sort_values('Name', ascending = True)[:55]

to_exclude = teams_to_exclude.index
teams_to_exlcude =  to_exclude.get_level_values('Team')
years_to_exclude = to_exclude.get_level_values('Year')

print(f"{len(teams_to_exlcude)} teams to exclude")
#%%
#exclude teams
for i in range(len(to_exclude)):
    df_new = df_new[~(df_new.Team.isin([teams_to_exlcude[i]]) & df_new.Year.isin([years_to_exclude[i]]))]

print(df_new)

#print(df_new)
# %%
#save df to excel
df_new.to_excel('/PL_Players/Scripts/world/df.xlsx', encoding = 'UTF-8')

# %%
