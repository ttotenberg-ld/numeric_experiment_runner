import json
from PyQt5.QtWidgets import QFileDialog

def load_clicked(self):
    loaded_file = QFileDialog.getOpenFileName(self, filter='JSON (*.json)')
    if not loaded_file[0] == '':
        filename = open(str(loaded_file[0]), 'r')
        f = json.load(filename)
        filename.close

        f_sdk = str(f['sdk_key'])
        f_api = str(f['api_key'])
        f_proj = str(f['proj_key'])
        f_flag = str(f['flag_key'])
        f_metric = str(f['metric_key'])
        f_iterations = str(f['iterations'])

        self.sdk_key.setText(f_sdk)
        self.api_key.setText(f_api)
        self.proj_key.setText(f_proj)
        self.flag_key.setText(f_flag)
        self.metric_key.setText(f_metric)
        self.iterations.setText(f_iterations)