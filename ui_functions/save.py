import json

'''
When the save button is clicked, save the file as "flag_key.json".
That json file contains all of the variables put into the fields
'''
def save_clicked(self):
    sdk_text = str(self.sdk_key.text())
    api_text = str(self.api_key.text())
    proj_text = str(self.proj_key.text())
    flag_text = str(self.flag_key.text())
    metric_text = str(self.metric_key.text())
    iterations_text = str(self.iterations.text())

    field_list = ['sdk_key', 'api_key', 'proj_key', 'flag_key', 'metric_key', 'iterations']
    field_text_list = [sdk_text, api_text, proj_text, flag_text, metric_text, iterations_text]
    fields_dict = dict(zip(field_list, field_text_list))
    fields_json = json.dumps(fields_dict, indent=4)

    f = open(f'saves/{flag_text}-{metric_text}.json', 'w')
    f.write(str(fields_json))
    f.close

    d = open('saves/' + 'default.json', 'w')
    d.write(str(fields_json))
    d.close