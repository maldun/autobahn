fname = "/home/maldun/.local/share/Paradox Interactive/Hearts of Iron IV/mod/autobahn/localisation/english/KX_ideas_l_english.yml" 

with open(fname, 'r') as f:
   text = f.read()
   
with open(fname, 'w', encoding='utf-8-sig') as f:
   f.write(text)
