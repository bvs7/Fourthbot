import json
import urllib.request
from pprint import pprint
import re


websource = urllib.request.urlopen('https://www.dnd-spells.com/spells')
data = websource.read().decode()
sites = re.findall(r"(https://www.dnd-spells.com/spell/[\w-]*)",data)
sites = list(set(sites))
with open('config/nothing3.txt','w') as out_file:
    for site in sites:
        websource = urllib.request.urlopen(site)
        data = websource.read().decode()
        desc = re.search(r"Components:(.|\n)*?Duration:(.*)",data)
        try:
            print(site, desc.group(0),desc.group(1),file=out_file,flush=True)
        except:
            continue
        print(site)
    print("Done!",file=out_file,flush=True)



# href="(https://www.dnd-spells.com/spell/[\w-]*)">
 ##<p></p>\s*.*\n\s*([^<]*)