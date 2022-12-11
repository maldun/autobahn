# First step: Assemble list with
#grep -Rli militia . | sort >> "/home/maldun/.local/share/Paradox Interactive/Hearts of Iron IV/mod/autobahn_KX/.scripts/militia_hlp.txt"

import pandas as pd
df = pd.read_csv('KX_equipment.csv',index_col=0)
data_top = df.head()
with open('militia_hlp.txt') as fp:
    lines = fp.readlines()
    lines = [line[2:] for line in lines]
    tags = {line[:3] for line in lines}



for key in df.index:
    if key in tags:
      df.loc[key]['r56_militia_tech'] = 1.0
        
df.to_csv('KX_equipment.csv')


