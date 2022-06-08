import json
import os
from ui_functions.variations import get_current_values, get_current_variations, get_specific_value


'''
Construct a json dictionary of variation fields
'''
def construct_variations_list(self):
    current_variations = get_current_variations(self)

    var_dict = {}
    for i in range(len(current_variations)):
        variation = str(current_variations[i])
        var_dict[f'{variation}'] = {}
        var_dict[f'{variation}']['center'] = str(get_specific_value(self, variation, 'center'))
        var_dict[f'{variation}']['spread'] = str(get_specific_value(self, variation, 'spread'))

    return var_dict

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

    save_path = os.path.expanduser("~") + '/Documents/ExperimentRunner'

    f = open(f'{save_path}/{flag_text}-{metric_text}.json', 'w')
    f.write(str(fields_json))
    f.close

    d = open(f'{save_path}/default.json', 'w')
    d.write(str(fields_json))
    d.close