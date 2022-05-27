from PyQt5.QtWidgets import QLineEdit
from utils.get_variation_list import variation_list

def get_variations_clicked(self):
    project = str(self.proj_key.text())
    flag = str(self.flag_key.text())
    api = str(self.api_key.text())

    try:
        variations = variation_list(project, flag, api)
    except:
        pass

    length = len(variations)
    for i in range(length):
        text = str(variations[i])
        center = text + '_center'
        spread = text + '_spread'
        center_field = QLineEdit()
        spread_field = QLineEdit()
        self.bottomFormLayout.addRow(center, center_field)
        self.bottomFormLayout.addRow(spread, spread_field)