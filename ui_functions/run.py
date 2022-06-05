import ldclient
from ldclient.config import Config
from ui_functions.preview import construct_variations_list, deduplicate_fields, normal_distribution
from PyQt5.QtGui import QTextCursor
import time

def output(self, number):
    for i in range(number):
        added_text = f"\nprinting {i}"
        self.terminal.setText(self.terminal.toPlainText() + added_text)
        self.terminal.moveCursor(QTextCursor.End)



def run_clicked(self):
    output(self, 200)
    # sdk_text = str(self.sdk_key.text())
    # proj_text = str(self.proj_key.text())
    # flag_text = str(self.flag_key.text())
    # metric_text = str(self.metric_key.text())
    # events_text = str(self.events.text())
    # fields_list = construct_variations_list(self)

    # # ldclient.set_config(Config(sdk_text))
    

    # values_list = list(fields_list.values())
    # center_list = []
    # spread_list = []
    # dist_dict = {}

    # for i in range(len(values_list)):
    #     if i%2:
    #         spread_list.append(values_list[i])
    #     else:
    #         center_list.append(values_list[i])

    # for i in range(len(center_list)):
    #     center_number = int(center_list[i])
    #     spread_number = int(spread_list[i])
    #     distribution = normal_distribution(center_number, spread_number, int(events))
        