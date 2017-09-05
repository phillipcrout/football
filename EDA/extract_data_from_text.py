import pandas as pd
import numpy as np
import re

fp = 'data/raw_percentage_data_v2.txt'
approx_start = 'Swansea City'

def find_occurances(string_target,string_whole):
    return [x.start() for x in re.finditer(string_target,string_whole)]
    
def odds_to_make_profit(prob):
    commission = 0.05
    required_win = (1-prob)/prob
    odds = 1 + (required_win)/(1-commission)
    return round(odds,2)

def convert_percentage_to_odd():
    for m in ['x','y','z']:
        solution[m] = solution[m].astype(float)
        solution[m] = solution[m].apply(lambda x : odds_to_make_profit(x/100))
    
with open(fp, 'r') as myfile:
    data=myfile.read().replace('\n', '')
    
### 3 occurances in the headline section then this week in the main bulk #1
start_point =find_occurances(approx_start,data)[4]-500

counter = 0
h,a,p = [],[],[]
while counter < 7:
    df = data[start_point:start_point+2500]
    pIdx = [m.start() for m in re.finditer('%',df)]
    end_point = pIdx[2]+1 
    df = df[:end_point] #only 3 percentages at a time, save sign though!
    pIdx = [m.start() for m in re.finditer('%',df)]
    p.append([df[i-2:i] for i in pIdx])
    print(str(sum([int(df[i-2:i]) for i in pIdx])))
    h.append(df[df.find('data-team1=')+12:df.find('data-team1')+20])
    a.append(df[df.find('data-team2=')+12:df.find('data-team2')+20])
    start_point += end_point    
    counter += 1

hp,dp,ap = [x[0] for x in p],[x[1] for x in p],[x[2] for x in p]

d = {'home win':h,'win away':a,'x':hp,'y':dp,'z':ap}
solution = pd.DataFrame(d)
convert_percentage_to_odd()
solution['sum_frac'] = (1/solution.x + 1/solution.y + 1/solution.z)
solution.sort_values('home win',inplace=True)
print(solution)