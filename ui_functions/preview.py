import matplotlib.pyplot as plt
import numpy as np
import random
from ui_functions.variations import get_current_values, get_current_variations

'''
Construct a dictionary of variations and values
'''
def construct_variations_list(self):
    current_variations = get_current_variations(self)
    current_values = get_current_values(self)

    if len(current_variations) == len(current_values):
        fields_list = dict(zip(current_variations, current_values))
    else:
        print("Please fill out all of the fields")

    return fields_list
    

'''
Returns a distribution of values given the following inputs:
CENTER: The mean of the distribution
SPREAD: The standard deviation or 'width' of the distribution. Edge values may be up to ~3x above/below the standard deviation
EVENTS: The number of values that will be returned
'''
def normal_distribution(center, spread, events):
    value_array = np.random.default_rng().normal(center, spread, events)
    return value_array

# Currently not implemented, could implement for alternate distributions later
def random_distribution(center, spread, events):
    low = int(center) - int(spread*3)
    high = int(center) + int(spread*3)
    value_array = []
    for i in range(events):
        value_array.append(random.randint(low, high))
    return value_array


def plot_histogram(data, variation):
    histogram = plt.hist(data, alpha=0.5, bins=100, label=str(variation))
    return histogram


'''
Deduplicate currently displayed list of fields
'''
def deduplicate_fields(dictionary):
    keys_list = list(dictionary.keys())
    deduped_list = []

    for item in keys_list:
        text = str(item)
        for r in (("_center", ""), ("_spread", "")):
            text = text.replace(*r)
        deduped_list.append(text)

    deduped_list = list(dict.fromkeys(deduped_list))
    return deduped_list
    

'''
Action called when the preview button is clicked
'''
def preview_clicked(self):
    self.figure.clear()

    events = str(self.events.text())
    fields_list = construct_variations_list(self)
    deduplicated_fields = deduplicate_fields(fields_list)

    values_list = list(fields_list.values())
    center_list = []
    spread_list = []

    for i in range(len(values_list)):
        if i%2:
            spread_list.append(values_list[i])
        else:
            center_list.append(values_list[i])

    for i in range(len(center_list)):
        center_number = int(center_list[i])
        spread_number = int(spread_list[i])
        distribution = normal_distribution(center_number, spread_number, int(events))
        plot_histogram(distribution, deduplicated_fields[i])

    plt.legend(loc='upper right')

    # refresh canvas
    self.canvas.draw()