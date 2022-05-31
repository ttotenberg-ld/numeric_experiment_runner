import json
from ui_functions.variations import get_current_values, get_current_variations


'''
Construct a json dictionary of variation fields
'''
def construct_variations_list(self):
    current_variations = get_current_variations(self)
    current_values = get_current_values(self)
    if len(current_values) < len(current_variations):
        difference = len(current_variations) - len(current_values)
        for i in range(difference):
            current_values.append('')

    fields_list = dict(zip(current_variations, current_values))
    return fields_list


'''
When the save button is clicked, save the file as "flag_key-metric_key.json".
That json file contains all of the variables put into the fields
'''
def save_clicked(self):
    sdk_text = str(self.sdk_key.text())
    api_text = str(self.api_key.text())
    proj_text = str(self.proj_key.text())
    flag_text = str(self.flag_key.text())
    metric_text = str(self.metric_key.text())
    events_text = str(self.events.text())
    variations_list = construct_variations_list(self)

    field_list = ['sdk_key', 'api_key', 'proj_key', 'flag_key', 'metric_key', 'events', 'variations']
    field_text_list = [sdk_text, api_text, proj_text, flag_text, metric_text, events_text, variations_list]
    fields_dict = dict(zip(field_list, field_text_list))
    fields_json = json.dumps(fields_dict, indent=4)

    f = open(f'saves/{flag_text}-{metric_text}.json', 'w')
    f.write(str(fields_json))
    f.close

    d = open('saves/' + 'default.json', 'w')
    d.write(str(fields_json))
    d.close