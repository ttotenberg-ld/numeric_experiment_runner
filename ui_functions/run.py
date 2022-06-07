import ldclient
from ldclient.config import Config
from ui_functions.preview import normal_distribution
from ui_functions.variations import get_current_variations, get_specific_value
from utils.create_user import random_ld_user
from PyQt5.QtGui import QTextCursor
import random
import time

def output(self, text):
    added_text = text
    self.terminal.setText(self.terminal.toPlainText() + '\n' + added_text)
    self.terminal.moveCursor(QTextCursor.End)


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
        

def run_clicked(self):
    # output(self, 200)
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
        user = random_ld_user()
        flag_variation = str(ldclient.get().variation(flag_text, user, default_variation))
        
        numeric_value = random.choice(data[f'{flag_variation}'])
        message = f'Sending event {i+1}/{events_text}. Variation is: {flag_variation} and metric value is: {numeric_value}.'
        print(message)
        # output(self, message)
        ldclient.get().track(metric_text, user, None, numeric_value)
    
    ldclient.get().close()