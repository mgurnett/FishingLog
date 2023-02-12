from catches.models import *
from catches.views import *
import pandas as pd

LAKE = 103
WEEK = 5
TEMPERATURE = 14
LOG_L = 5; LOG_T = 5; LOG_W = 5; LOG_LW = 15; LOG_LT = 15; 
HATCH_L = 5; HATCH_T = 5; HATCH_W = 5; HATCH_LW = 15; HATCH_LT = 15; 

def get_array_p():
    df = pd.DataFrame(list(Fly.objects.all().order_by('id').values('id','name','bug')))
    # print (df.loc[1]['id'])

    logs_L = []; logs_W = []; logs_T = []; logs_LW = []; logs_LT = []
    for index, row in df.iterrows():
        fly_id = row.loc['id']
        logs_L.append (Log.objects.filter(lake = LAKE, fly = fly_id).count() )
        logs_T.append (Log.objects.filter(temp = TEMPERATURE, fly = fly_id).count() )
        logs_W.append (Log.objects.filter(week = WEEK, fly = fly_id).count() )
        logs_LW.append (Log.objects.filter(lake = LAKE, week = WEEK, fly = fly_id).count() )
        logs_LT.append (Log.objects.filter(lake = LAKE, temp = TEMPERATURE, fly = fly_id).count() )

    df['L'] = pd.DataFrame(list(logs_L))
    df['T'] = pd.DataFrame(list(logs_T))
    df['W'] = pd.DataFrame(list(logs_W))
    df['LT'] = pd.DataFrame(list(logs_LT))
    df['LW'] = pd.DataFrame(list(logs_LW))
    sumL = df['L'].sum()
    sumT = df['T'].sum()
    sumW = df['W'].sum()
    sumLT = df['LT'].sum()
    sumLW = df['LW'].sum()
    # print (sumL,sumT, sumW, sumLT, sumLW )

    logs_L = []; logs_W = []; logs_T = []; logs_LW = []; logs_LT = []; logs_total = []
    for index, row in df.iterrows():
        fly_id = row.loc['id']
        logs_L.append (row.loc['L']/sumL*LOG_L)
        logs_T.append (row.loc['T']/sumT*LOG_T )
        logs_W.append (row.loc['W']/sumW*LOG_W )
        logs_LW.append (row.loc['LW']/sumLW*LOG_LW)
        logs_LT.append (row.loc['LT']/sumLT*LOG_LT )
        logs_total.append (
            row.loc['L']/sumL*LOG_L +
            row.loc['LT']/sumLT*LOG_T +
            row.loc['W']/sumW*LOG_W  +
            row.loc['LW']/sumLW*LOG_LW +
            row.loc['LT']/sumLT*LOG_LT
            )

    df['LLW'] = pd.DataFrame(list(logs_L))
    df['LTW'] = pd.DataFrame(list(logs_T))
    df['LWW'] = pd.DataFrame(list(logs_W))
    df['LLTW'] = pd.DataFrame(list(logs_LT))
    df['LLWW'] = pd.DataFrame(list(logs_LW))
    df['log_total'] = pd.DataFrame(list(logs_total))

    #hatches
    hatchs_L = []; hatchs_W = []; hatchs_T = []; hatchs_LW = []; hatchs_LT = []
    for index, row in df.iterrows():
        bug_id = row.loc['bug']
        if pd.notna(bug_id):  
            # print (f'no nan and an id of {bug_id}')
            hatchs_L.append (Hatch.objects.filter(lake = LAKE, bug = bug_id).count() )
            hatchs_T.append (Hatch.objects.filter(temp = TEMPERATURE, bug = bug_id).count() )
            hatchs_W.append (Hatch.objects.filter(week = WEEK, bug = bug_id).count() )
            hatchs_LW.append (Hatch.objects.filter(lake = LAKE, week = WEEK, bug = bug_id).count() )
            hatchs_LT.append (Hatch.objects.filter(lake = LAKE, temp = TEMPERATURE, bug = bug_id).count() ) 
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

    hatchs_L = []; hatchs_W = []; hatchs_T = []; hatchs_LW = []; hatchs_LT = []; hatchs_total = []
    for index, row in df.iterrows():
        bug_id = row.loc['bug']
        if pd.notna(bug_id): 
            hatchs_L.append (row.loc['HL']/sumL*HATCH_L)
            hatchs_T.append (row.loc['HT']/sumT*HATCH_T )
            hatchs_W.append (row.loc['HW']/sumW*HATCH_W )
            hatchs_LW.append (row.loc['HLW']/sumLW*HATCH_LW)
            hatchs_LT.append (row.loc['HLT']/sumLT*HATCH_LT )
            hatchs_total.append (
                row.loc['HL']/sumL*HATCH_L +
                row.loc['HLT']/sumLT*HATCH_T +
                row.loc['HW']/sumW*HATCH_W  +
                row.loc['HLW']/sumLW*HATCH_LW +
                row.loc['HLT']/sumLT*HATCH_LT
                )
        else:
            hatchs_L.append (0)
            hatchs_T.append (0)
            hatchs_W.append (0)
            hatchs_LW.append (0)
            hatchs_LT.append (0)
            hatchs_total.append (0)


    df['HLW'] = pd.DataFrame(list(hatchs_L))
    df['HTW'] = pd.DataFrame(list(hatchs_T))
    df['HWW'] = pd.DataFrame(list(hatchs_W))
    df['HLTW'] = pd.DataFrame(list(hatchs_LT))
    df['HLWW'] = pd.DataFrame(list(hatchs_LW))
    df['hatch_total'] = pd.DataFrame(list(hatchs_total))


    final_total =[]
    for index, row in df.iterrows():
        final_total.append( int(row.loc['log_total']) + int(row.loc['hatch_total']) )
    df['final_total'] = pd.DataFrame(list(final_total))
    
    df_prune = df.loc[df["final_total"] > 1 ]

    df_sort = df_prune.sort_values(by=['final_total'], ascending=False)

    return df_sort

