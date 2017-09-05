import numpy as np
import pandas as pd
import sqlite3

#load data (make sure you have downloaded database.sqlite)
# """
with sqlite3.connect('data/database.sqlite') as con:
    countries = pd.read_sql_query("SELECT * from Country", con)
    matches = pd.read_sql_query("SELECT * from Match", con)
    leagues = pd.read_sql_query("SELECT * from League", con)
    teams = pd.read_sql_query("SELECT * from Team", con)
    

selected_countries = ['France']
countries = countries[countries.name.isin(selected_countries)]
leagues = countries.merge(leagues,on='id',suffixes=('', '_y'))
matches = matches[matches.league_id.isin(leagues.id)]
matches = matches[['id','season', 'stage', 'date','match_api_id', 'home_team_api_id', 'away_team_api_id','home_team_goal', 'away_team_goal']]
matches.dropna(inplace=True)

matches['D'] = np.where(matches.home_team_goal == matches.away_team_goal,1,0)
matches['HW'] = np.where(matches.home_team_goal > matches.away_team_goal,1,0)
matches['AW'] = np.where(matches.home_team_goal < matches.away_team_goal,1,0)
del matches['home_team_goal']
del matches['away_team_goal']

matches = matches.merge(elo_df,how='left',left_on='home_team_api_id',right_on='team_id')
del matches['team_id']
matches.rename(columns={'elo': 'elo_home'}, inplace=True)
matches = matches.merge(elo_df,how='left',left_on='away_team_api_id',right_on='team_id')
del matches['team_id']
matches.rename(columns={'elo': 'elo_away'}, inplace=True)

matches.to_csv('data/french_l1.csv')

