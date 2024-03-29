import ldclient
from ldclient.config import Config
from ui_functions.preview import normal_distribution
from ui_functions.variations import get_current_variations, get_specific_value
from utils.create_context import *
import random
import threading

'''
Constructs a dictionary of variations and their metric distributions
'''
def construct_distribution_dict(self):
    events_text = int(self.events.text())
    dictionary = {}
    variations = get_current_variations(self)
    for i in range(len(variations)):
        center_number = int(get_specific_value(self, str(variations[i]), 'center'))
        spread_number = int(get_specific_value(self, str(variations[i]), 'spread'))
        distribution = normal_distribution(center_number, spread_number, events_text)
        dictionary[f'{variations[i]}'] = distribution
    return dictionary
        
'''
Function called when the run button is clicked.
Creates a thread to execute the calls, and displays progress
'''
def run_clicked(self):
    execute = threading.Thread(target=execute_track_call, args=[self])
    execute.start()

'''
Threaded function which executes the LD calls
'''
def execute_track_call(self):    
    sdk_text = str(self.sdk_key.text())
    proj_text = str(self.proj_key.text())
    flag_text = str(self.flag_key.text())
    metric_text = str(self.metric_key.text())
    events_text = int(self.events.text())
    default_variation = get_current_variations(self)[0]
    data = construct_distribution_dict(self)
 
    # Initialize the LD SDK
    ldclient.set_config(Config(sdk_text))

    for i in range(events_text):
        context = create_multi_context()
        flag_variation = str(ldclient.get().variation(flag_text, context, default_variation))
        print(f'flag variation is: {flag_variation}')       
        numeric_value = random.choice(data[f'{flag_variation}'])
        ldclient.get().track(metric_text, context, None, numeric_value)
        self.progress_label.setText(f"Progress: sending track event {i+1}/{events_text}")

    ldclient.get().close()