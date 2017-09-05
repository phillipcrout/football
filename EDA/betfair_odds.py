import numpy as np

def bet365_fair_odds(H,D,A):
    t = 1/H + 1/D + 1/A
    fair = np.divide([H,D,A],t)
    commision_included = fair*1.05
    return commision_included