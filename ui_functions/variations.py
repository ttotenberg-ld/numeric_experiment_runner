import json
from PyQt5.QtWidgets import (
    QLineEdit,
    QLabel
)
from PyQt5.QtGui import QFont
from utils.get_variation_list import variation_list


'''
Function used in load.py to populate variations fields from loaded file
'''
def load_variations(self, loaded_file):
    for i in reversed(range(self.bottomFormLayout.count())):
        if i != 0:
            self.bottomFormLayout.itemAt(i).widget().setParent(None)
    
    variations = loaded_file['variations']
    for key in variations:
        # Set variation labels
        var_label = QLabel()
        var_label.setText(key)
        font = QFont()
        font.setBold(True)
        font.setUnderline(True)
        var_label.setFont(font)
        self.bottomFormLayout.addWidget(var_label)

        # Set editable fields
        center_field = QLineEdit()
        spread_field = QLineEdit()
        center_field.setText(str(variations[key]['center']))
        spread_field.setText(str(variations[key]['spread']))
        self.bottomFormLayout.addRow('Center', center_field)
        self.bottomFormLayout.addRow('Spread', spread_field)


'''
Calls utils.get_variation_list to make an API call and return a list of variations for a flag
'''
def get_variation_list(self):
    api_text = str(self.api_key.text())
    proj_text = str(self.proj_key.text())
    flag_text = str(self.flag_key.text())
    
    try:
        variations = variation_list(proj_text, flag_text, api_text)
        return variations
    except Exception as err:
        print(err)
        pass


'''
Returns the currently loaded variataions
'''
def get_current_variations(self):
    loaded_variations = []
    substring_list = ['Center', 'Spread']
    for i in range(self.bottomFormLayout.count()):
        field = self.bottomFormLayout.itemAt(i).widget()
        if isinstance(field, QLabel):
            if any(substring in field.text() for substring in substring_list):
                pass
            else:
                loaded_variations.append(field.text())
    return loaded_variations


'''
Returns the currently loaded values
'''
def get_current_values(self):
    loaded_values = []
    for i in range(self.bottomFormLayout.count()):
        field = self.bottomFormLayout.itemAt(i).widget()
        if isinstance(field, QLineEdit):
            loaded_values.append(field.text())
    return loaded_values

'''
Returns a specific currently loaded value
VARIATION: the variation to pass in
CS: center or spread
'''
def get_specific_value(self, variation, cs):
    substring_list = ['Center', 'Spread']
    for i in range(self.bottomFormLayout.count()):
        field = self.bottomFormLayout.itemAt(i).widget()
        if any(substring in field.text() for substring in substring_list):
            pass
        else:
            if str(variation) == field.text():
                center_field = self.bottomFormLayout.itemAt(i+2).widget().text()
                spread_field = self.bottomFormLayout.itemAt(i+4).widget().text()
                if cs == 'center':
                    return center_field
                elif cs == 'spread':
                    return spread_field
                else:
                    print('Please enter center or spread')
            


'''
Populates a new variations list via an API call. Retains the currently loaded values
'''
def populate_variations(self, variations):
    # Construct list of field labels for both centers and spreads
    new_variations = {}
    for i in range(len(variations)):
        text = str(variations[i])
        new_variations[f'{text}'] = {}
        center_text = str(get_specific_value(self, str(variations[i]), 'center'))
        spread_text = str(get_specific_value(self, str(variations[i]), 'spread'))
        if center_text == 'None':
            center_text = ''
        if spread_text == 'None':
            spread_text = ''
        new_variations[f'{text}']['center'] = center_text
        new_variations[f'{text}']['spread'] = spread_text

    # Get the list of current values. Add blank values to match number of fields if needed.
    loaded_values = get_current_values(self)
    if len(loaded_values) < (len(new_variations)*2):
        difference = (len(new_variations)*2) - len(loaded_values)
        for i in range(difference):
            loaded_values.append('')

    # Clear the old fields
    for i in reversed(range(self.bottomFormLayout.count())):
        if i != 0:
            self.bottomFormLayout.itemAt(i).widget().setParent(None)

    # Builds the new fields
    for key in new_variations:
        # Set Labels
        var_label = QLabel()
        var_label.setText(key)
        font = QFont()
        font.setBold(True)
        font.setUnderline(True)
        var_label.setFont(font)
        self.bottomFormLayout.addWidget(var_label)

        # Set editable fields
        center_field = QLineEdit()
        spread_field = QLineEdit()
        center_field.setText(str(new_variations[key]['center']))
        spread_field.setText(str(new_variations[key]['spread']))
        self.bottomFormLayout.addRow('Center', center_field)
        self.bottomFormLayout.addRow('Spread', spread_field)


'''
Function that is called when the button is clicked.
Gets the most up to date list of variations via an API call, then creates fields with those variations
'''
def get_variations_clicked(self):
    variations = get_variation_list(self)
    populate_variations(self, variations)