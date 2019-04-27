import json
import string

with open('config/spells2.json','r') as spell_file:
    spells_in = json.load(spell_file)
with open('config/comdur.json','r') as desc_file:
    comdur = json.load(desc_file)
spells_out = dict()
translator = str.maketrans('','',string.punctuation)
for spell in spells_in:
    spell_name = spell.translate(translator)
    spell_name = spell_name.lower()
    spells_out[spell_name] = spells_in[spell]
    if spell_name in comdur:
        spells_out[spell_name]['components'] = comdur[spell_name]['Components']
        spells_out[spell_name]['duration'] = comdur[spell_name]['Duration']
    else:
        print(spell_name,"-NOT INCLUDED")

with open('config/spells3.json','w') as spell_file:
    json.dump(spells_out,spell_file)

