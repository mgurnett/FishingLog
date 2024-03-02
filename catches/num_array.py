from catches.models import *
from catches.views import *
import pandas as pd
import math

LAKE = 103
WEEK = 5
TEMPERATURE = 14
#weights that everyting gets multiplied by
LOG_L = 5;   LOG_T = 5;   LOG_W = 5;   LOG_LW = 15;   LOG_LT = 15;      #max = 45%
HATCH_L = 5; HATCH_T = 5; HATCH_W = 5; HATCH_LW = 15; HATCH_LT = 15;    #max = 45%
CATCH_WEIGHT = 2                                                        #max = 10%

def get_array(week, lake, temperature):
    if not week:
        week = WEEK
    if not lake:
        lake = LAKE
    if not temperature:
        temperature = TEMPERATURE
    df = pd.DataFrame(list(Fly.objects.all().order_by('id').values('id','name','bug')))
    # print (df.loc[1]['id'])

    logs_L = []; logs_W = []; logs_T = []; logs_LW = []; logs_LT = []
    for index, row in df.iterrows():  #lterate through all flys
        fly_id = row.loc['id']
        # print (f'fly_id =  {fly_id}')
        # print (f"fly name =  {row.loc['name']}/{row.loc['id']}/{row.loc['bug']}")
        logs_L.append (Log.objects.filter(lake = lake, fly = fly_id).count() )
        logs_T.append (Log.objects.filter(temp = temperature, fly = fly_id).count() )
        logs_W.append (Log.objects.filter(week = week, fly = fly_id).count() )
        logs_LW.append (Log.objects.filter(lake = lake, week = week, fly = fly_id).count() )
        logs_LT.append (Log.objects.filter(lake = lake, temp = temperature, fly = fly_id).count() )
    # print (f'logs_L - {logs_L} | logs_T - {logs_T} | logs_W - {logs_W} | logs_LW - {logs_LW} | logs_LT - {logs_LT}' )
    df['L'] = pd.DataFrame(list(logs_L))
    # print (f"df['L'] =  {df['L']}")
    df['T'] = pd.DataFrame(list(logs_T))
    df['W'] = pd.DataFrame(list(logs_W))
    df['LT'] = pd.DataFrame(list(logs_LT))
    df['LW'] = pd.DataFrame(list(logs_LW))
    sumL = df['L'].sum() + 1
    sumT = df['T'].sum() + 1
    sumW = df['W'].sum() + 1
    sumLT = df['LT'].sum() + 1
    sumLW = df['LW'].sum() + 1
    # print (f'sumL - {sumL} | sumT - {sumT} | sumW - {sumW} | sumLT - {sumLT} | sumLW - {sumLW}' )

    logs_L = []; logs_W = []; logs_T = []; logs_LW = []; logs_LT = []; logs_total = []
    for index, row in df.iterrows():  #lterate through all flys
        fly_id = row.loc['id']
        logs_L.append (math.ceil(row.loc['L']/sumL*LOG_L)) #this is how the weights are applied.
        logs_T.append (math.ceil(row.loc['T']/sumT*LOG_T ))  #count / sum * weight - for each fly
        logs_W.append (math.ceil(row.loc['W']/sumW*LOG_W ))
        logs_LW.append (math.ceil(row.loc['LW']/sumLW*LOG_LW))
        logs_LT.append (math.ceil(row.loc['LT']/sumLT*LOG_LT ))
        logs_total.append (int(
            math.ceil(row.loc['L']/sumL*LOG_L) +
            math.ceil(row.loc['LT']/sumLT*LOG_T) +
            math.ceil(row.loc['W']/sumW*LOG_W)  +
            math.ceil(row.loc['LW']/sumLW*LOG_LW) +
            math.ceil(row.loc['LW']/sumLW*LOG_LW) +
            row.loc['LT']/sumLT*LOG_LT
            ))
    # print (f'logs_L - {logs_L} | logs_T - {logs_T} | logs_W - {logs_W} | logs_LW - {logs_LW} | logs_LT - {logs_LT} | logs_total - {logs_total}' )
    df['LLW'] = pd.DataFrame(list(logs_L))
    df['LTW'] = pd.DataFrame(list(logs_T))
    df['LWW'] = pd.DataFrame(list(logs_W))
    df['LLTW'] = pd.DataFrame(list(logs_LT))
    df['LLWW'] = pd.DataFrame(list(logs_LW))
    df['log_total'] = pd.DataFrame(list(logs_total))
    # print (f"lake - {df['LLW']}\n |  temp - {df['LTW']}\n |  week - {df['LWW']}\n | lake&temp - {df['LLWW']}\n |  lake&week - {df['LLWW']}\n | total - {df['log_total']}\n")

    #hatches
    hatchs_L = []; hatchs_W = []; hatchs_T = []; hatchs_LW = []; hatchs_LT = []
    for index, row in df.iterrows():
        bug_id = row.loc['bug']
        if pd.notna(bug_id):  
            # print (f'no nan and an id of {bug_id}')
            hatchs_L.append (Hatch.objects.filter(lake = lake, bug = bug_id).count() )
            hatchs_T.append (Hatch.objects.filter(temp = temperature, bug = bug_id).count() )
            hatchs_W.append (Hatch.objects.filter(week = week, bug = bug_id).count() )
            hatchs_LW.append (Hatch.objects.filter(lake = lake, week = week, bug = bug_id).count() )
            hatchs_LT.append (Hatch.objects.filter(lake = lake, temp = temperature, bug = bug_id).count() ) 
        else:                          
            # print (f'nan and an id of {bug_id}')
            hatchs_L.append (0)
            hatchs_T.append (0)
            hatchs_W.append (0)
            hatchs_LW.append (0)
            hatchs_LT.append (0)

    df['HL'] = pd.DataFrame(list(hatchs_L))
    df['HT'] = pd.DataFrame(list(hatchs_T))
    df['HW'] = pd.DataFrame(list(hatchs_W))
    df['HLT'] = pd.DataFrame(list(hatchs_LT))
    df['HLW'] = pd.DataFrame(list(hatchs_LW))
    sumL = df['HL'].sum() +1
    sumT = df['HT'].sum() +1
    sumW = df['HW'].sum() +1
    sumLT = df['HLT'].sum() +1
    sumLW = df['HLW'].sum() +1
    # print (sumL,sumT, sumW, sumLT, sumLW )

    hatchs_L = []; hatchs_W = []; hatchs_T = []; hatchs_LW = []; hatchs_LT = []; hatchs_total = []; chart = []
    for index, row in df.iterrows():
        bug_id = row.loc['bug']
        # print (f"#2.1 and bug_id is {bug_id}")
        # The issue here is that there are bugs that are not in the chart.
        if ( pd.notna(bug_id) and (bug_id in [6,5,11,8,7,10,4,9,12])): # this is the bugs in the chart
            hatchs_L.append (row.loc['HL']/sumL*HATCH_L)
            hatchs_T.append (row.loc['HT']/sumT*HATCH_T )
            hatchs_W.append (row.loc['HW']/sumW*HATCH_W )
            hatchs_LW.append (row.loc['HLW']/sumLW*HATCH_LW)
            hatchs_LT.append (row.loc['HLT']/sumLT*HATCH_LT )
            hatchs_total.append (int(
                row.loc['HL']/sumL*HATCH_L +
                row.loc['HLT']/sumLT*HATCH_T +
                row.loc['HW']/sumW*HATCH_W  +
                row.loc['HLW']/sumLW*HATCH_LW +
                row.loc['HLT']/sumLT*HATCH_LT
                ))

            # print (f" week = {week} and bug = {bug_id}")
            chart.append ( int (Chart.objects.get(week = week, bug = bug_id).strength * CATCH_WEIGHT ))

        else:
            hatchs_L.append (0)
            hatchs_T.append (0)
            hatchs_W.append (0)
            hatchs_LW.append (0)
            hatchs_LT.append (0)
            hatchs_total.append (0)
            chart.append ( 0 )
 
    df['HLW'] = pd.DataFrame(list(hatchs_L))
    df['HTW'] = pd.DataFrame(list(hatchs_T))
    df['HWW'] = pd.DataFrame(list(hatchs_W))
    df['HLTW'] = pd.DataFrame(list(hatchs_LT))
    df['HLWW'] = pd.DataFrame(list(hatchs_LW))
    df['hatch_total'] = pd.DataFrame(list(hatchs_total))
    df['chart'] = pd.DataFrame(list(chart))

    final_total =[]
    for index, row in df.iterrows():
        final_total.append(
            int(row.loc['log_total']) + 
            int(row.loc['hatch_total']) +
            int(row.loc['chart'])
        )
        # print (row.loc['log_total'])
    df['final_total'] = pd.DataFrame(list(final_total))
    
    df_prune = df.loc[df["final_total"] > 5 ]

    df_sort = df_prune.sort_values(by=['final_total'], ascending=False)

    return df_sort

