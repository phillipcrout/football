from elo_functions import *
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import linear_model

eta = 1500 ###starting elo
beta = 400 # +- on your opponents rating
kappa = 90

for kappa in [95]: #rejected 60 and 30 as non improvements
    for z in [0.85,0.9,0.95]: #also discard 0.1,0.3,0.5
    ## imports
        matches = pd.read_csv('data/french_l1.csv',index_col='id')
        t1 = matches.home_team_api_id.unique()
        elo = [eta]*len(t1)
        elo_df = pd.DataFrame({'team_id':t1, 'elo':elo},index=t1)
    ### run
        hyp = [eta,kappa,beta,z]
        full_elo_run(matches,elo_df,*hyp)
        matches['elo_diff'] = np.subtract(matches.elo_home,matches.elo_away)
    ### learn
        X = matches[['elo_home','elo_away','elo_diff']]
        Y = matches['D'] + 2*matches['AW'] #0 for HW, 1 for draw, 2 for AW
        X,Y = X[kappa:],Y[kappa:]        
        logreg = linear_model.LogisticRegression(C=1e5)
        logreg.fit(X, Y)
        print(logreg.score(X,Y))
    
    
""" 
Scores are 
0.481 and 0.486
+ elo diff
===> no change
### changing lengths of chunks does create problems
### so perhaps using 20 is the way? 0.47 and 0.48 seem to agree
### bug fix goes 0.485 vs 0.484
"""