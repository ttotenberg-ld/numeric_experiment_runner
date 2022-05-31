import json
from PyQt5.QtWidgets import (
    QLineEdit,
    QLabel
)
from utils.get_variation_list import variation_list


'''
Function used in load.pyto populate variations fields from loaded file
'''
def load_variations(self, loaded_file):
    for i in reversed(range(self.bottomFormLayout.count())):
        if i != 0:
            self.bottomFormLayout.itemAt(i).widget().setParent(None)
    
    variations = loaded_file['variations'].items()
    for key, value in variations:
        new_field = QLineEdit()
        new_field.setText(str(value))
        self.bottomFormLayout.addRow(key, new_field)


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
    for i in range(self.bottomFormLayout.count()):
        field = self.bottomFormLayout.itemAt(i).widget()
        if isinstance(field, QLabel):
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
Populates a new variations list via an API call. Retains the currently loaded values
'''
def populate_variations(self, variations):
    # Construct list of field labels for both centers and spreads
    new_variations = []
    for i in range(len(variations)):
        text = str(variations[i])
        center = text + '_center'
        spread = text + '_spread'
        new_variations.append(center)
        new_variations.append(spread)

    # Get the list of current values. Add blank values to match number of fields if needed.
    loaded_values = get_current_values(self)
    if len(loaded_values) < len(new_variations):
        difference = len(new_variations) - len(loaded_values)
        for i in range(difference):
            loaded_values.append('')

    # Clear the old fields
    for i in reversed(range(self.bottomFormLayout.count())):
        if i != 0:
            self.bottomFormLayout.itemAt(i).widget().setParent(None)
    
    # Zip together the list of new field labels with existing values
    new_fields_dict = dict(zip(new_variations, loaded_values))
    field_items = new_fields_dict.items()

    # Construct the new fields
    for key, value in field_items:
        new_field = QLineEdit()
        new_field.setText(str(value))
        if key != '':
            self.bottomFormLayout.addRow(key, new_field)


'''
Function that is called when the button is clicked.
Gets the most up to date list of variations via an API call, then creates fields with those variations
'''
def get_variations_clicked(self):
    variations = get_variation_list(self)
    populate_variations(self, variations)