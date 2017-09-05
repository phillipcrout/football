""" 
Three functions:
calculate_local_elo_change takes a result and applies Opponent +- beta in a new column
This output is fed into
elo_updator which averages all relevant updates and applies them with weighting z

These operation are combined into full_elo_run


"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings('ignore')


def calculate_local_elo_changes(matches,start,end,beta):
    mshort = matches.iloc[start:end]
    mshort['elo_home_change'] = np.where(mshort.HW == 1, mshort.elo_away+beta,mshort.elo_away-beta)
    mshort['elo_away_change'] = np.where(mshort.AW == 1, mshort.elo_home+beta,mshort.elo_home-beta)
    mshort['elo_home_change'][mshort.D==1] = mshort.elo_away
    mshort['elo_away_change'][mshort.D==1] = mshort.elo_home
    return mshort

def elo_updator(team_id,mshort,z,elo_df):
    elo_change = np.sum(mshort.elo_home_change[mshort.home_team_api_id==team_id])+np.sum(mshort.elo_away_change[mshort.away_team_api_id==team_id])
    count = np.sum(mshort.home_team_api_id==team_id)+np.sum(mshort.away_team_api_id==team_id)
    if elo_change != 0:    
        updated_value = (elo_change/count)*(1-z) + elo_df[elo_df.team_id==team_id].elo*z
        elo_df.set_value(team_id,'elo',updated_value)    

def full_elo_run(matches,elo_df,eta,kappa,beta,z): #leave eta,kappa,beta as global variables
    s = 0 #for start
    k = kappa 
    while (s) < matches.shape[0]:
        e = (s+k)        
        if e%380 < s%380: ## we've gone over a season limit
            e = int(380*np.floor(e/380))            
        for x in matches.home_team_api_id.unique():
            # READ            
            matches.elo_home.iloc[s:e][matches.home_team_api_id==x] = elo_df.loc[x].elo
            matches.elo_away.iloc[s:e][matches.away_team_api_id==x] = elo_df.loc[x].elo
        ## Update            
        mshort = calculate_local_elo_changes(matches,s,e,beta)
        #print(str(s+k) + ' and before read in')
        for x in matches.home_team_api_id.unique():
            # Write            
            elo_updator(x,mshort,z,elo_df)
            
        if e%380 == 0: ## converge for the new season
            ## hard wired for now
            start_mean = np.mean(elo_df.elo)
            for x in matches.home_team_api_id.unique():
                updated_value = 0.9*elo_df[elo_df.team_id==x].elo + 0.1*start_mean
                elo_df.set_value(x,'elo',updated_value)
            
        s += k
