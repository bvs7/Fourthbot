import json
import string

with open('config/spells.json','r') as spell_file:
    spells_in = json.load(spell_file)
with open('config/nothing3.json','r') as desc_file:
    descriptions = json.load(desc_file)
spells_out = dict()
translator = str.maketrans('','',string.punctuation)
for spell in spells_in:
    spell_name = spell.translate(translator)
    spell_name = spell_name.lower()
    spells_out[spell_name] = spells_in[spell]
    if spell_name in descriptions:
        spells_out[spell_name]['description'] = descriptions[spell_name]
    print(spells_out[spell_name])

with open('config/spells2.json','w') as spell_file:
    json.dump(spells_out,spell_file)

